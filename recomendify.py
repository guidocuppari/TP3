from grafos import Grafo
from biblioteca import camino_minimo_bfs, bfs_distancias, dfs_ciclo_n, random_walk_multiples
import argparse
import os

CANCIONES = "canciones"
USUARIOS = "usuarios"
CAMINO = "camino"
IMPORTANTES = "mas_importantes"
RECOMENDACION = "recomendacion"
CICLO = "ciclo"

class Recomendify:
    def __init__(self):
        self.grafo_bipartito = Grafo()
        self.diccionario = {} #dicionario con el nombre como clave y el valor es una tupla de cancion y playlist en la que aparece
        self.grafo_canciones = Grafo()

    def cargar_diccionario(self, datos):
        for nombre_user, cancion, playlist in datos: #cancion es una tupla (nombre_cancion, artista)
            if nombre_user not in self.diccionario:
                self.diccionario[nombre_user] = []
            self.diccionario[nombre_user].append((cancion, playlist))

    def cargar_grafo(self):
        for nombre_user, canciones in self.diccionario.items():
            self.grafo_bipartito.agregar_vertice(nombre_user)
            for (cancion, _) in canciones:
                if cancion not in self.grafo_bipartito.obtener_vertices():
                    self.grafo_bipartito.agregar_vertice(cancion)
                self.grafo_bipartito.agregar_arista(nombre_user, cancion)

    def armar_resultado_camino(self, recorrido, usuarios, canciones, resultado):
        for i in range(len(recorrido) - 1):
            origen = recorrido[i]
            destino = recorrido[i + 1]
            if origen in self.diccionario:
                canciones.add(destino)
                playlist = next((p for c, p in self.diccionario[origen] if c == destino), None)
                if origen in usuarios:
                    resultado.append(f"tiene una playlist --> {playlist} --> donde aparece --> {destino[0]} - {destino[1]}")
                    continue
                resultado.append(f"{destino[0]} - {destino[1]} --> aparece en playlist --> {playlist} --> de --> {origen}")
            elif destino in self.diccionario:
                usuarios.add(destino)
                playlist = next((p for c, p in self.diccionario[destino] if c == origen), None)
                if origen in canciones:
                    resultado.append(f"aparece en playlist --> {playlist} --> de --> {destino}")
                    continue
                resultado.append(f"{origen[0]} - {origen[1]} --> aparece en playlist --> {playlist} --> de --> {destino}")

    def camino_minimo(self, cancion_origen, cancion_destino):
        if cancion_origen not in self.grafo_bipartito.obtener_vertices():
            return f"Error: {cancion_origen} no está en el grafo"
        if cancion_destino not in self.grafo_bipartito.obtener_vertices():
            return f"Error: {cancion_destino} no está en el grafo"

        padres, _ = camino_minimo_bfs(self.grafo_bipartito, cancion_origen)
        if cancion_destino not in padres:
            return "No se encontro recorrido"

        recorrido = []
        actual = cancion_destino
        while actual is not None:
            recorrido.append(actual)
            actual = padres[actual]

        recorrido.reverse()
        resultado = []
        usuarios_visitados = set()
        canciones_visitadas = set()
        self.armar_resultado_camino(recorrido, usuarios_visitados, canciones_visitadas, resultado)
        return " --> ".join(resultado)

    def pagerank(self, grafo, d=0.85, iteraciones=100, tolerancia=1e-6):
        vertices = grafo.obtener_vertices()
        N = len(vertices)  # Número total de vértices
        if N == 0:
            return {}

        pagerank_actual = {v: 1 / N for v in vertices}
        for _ in range(iteraciones):
            pagerank_nuevo = {v: (1 - d) / N for v in vertices}
            for v in vertices:
                for u in grafo.obtener_adyacentes(v):  # u -> v (aristas entrantes a v)
                    pagerank_nuevo[v] += d * pagerank_actual[u] / grafo.grado_salida(u)

            suma_total = sum(pagerank_nuevo.values())
            pagerank_nuevo = {v: pr / suma_total for v, pr in pagerank_nuevo.items()}
            cambio_total = sum(abs(pagerank_nuevo[v] - pagerank_actual[v]) for v in vertices)
            pagerank_actual = pagerank_nuevo
            if cambio_total < tolerancia:
                break

        return pagerank_actual

    def mas_importantes(self, n):
        pagerank = self.pagerank(self.grafo_bipartito)

        canciones = {nodo: pagerank[nodo] for nodo in pagerank if self.es_cancion(nodo)}
        canciones_importantes = sorted(canciones.items(), key=lambda item: item[1], reverse=True)
        top_canciones = canciones_importantes[:n]
        return "; ".join(f"{cancion[0]} - {cancion[1]}" for cancion, _ in top_canciones)

    def es_cancion(self, nodo):
        return isinstance(nodo, tuple) and len(nodo) == 2

    def cargar_grafo_de_canciones(self):
        for _, canciones in self.diccionario.items():
            canciones_usuario = set(cancion for (cancion, _) in canciones)
            canciones_usuario = list(canciones_usuario)

            for i in range(len(canciones_usuario)):
                for j in range(i + 1, len(canciones_usuario)):
                    self.grafo_canciones.agregar_arista(canciones_usuario[i], canciones_usuario[j])

    def rango(self, n, cancion_inicio):
        if cancion_inicio not in self.grafo_canciones.obtener_vertices():
            return 0

        canciones_a_n_saltos = bfs_distancias(self.grafo_canciones, cancion_inicio, n)
        return len(canciones_a_n_saltos)

    def buscar_ciclo_n(self, inicio, largo):
        visitados = [inicio]
        camino = [inicio]
        resultado = dfs_ciclo_n(self.grafo_canciones, inicio, visitados, camino, largo)
        return " --> ".join(f"{cancion[0]} - {cancion[1]}" for cancion in resultado)

    def recomendar(self, grafo, tipo, cantidad, canciones, largo=100, iteraciones=500):
        nodos_iniciales = [cancion for cancion in canciones]
        visitas_acumuladas = random_walk_multiples(grafo, nodos_iniciales, largo, iteraciones)
        recs_ordenadas = []
        if tipo == CANCIONES:
            recomendaciones = {
                nodo: valor
                for nodo, valor in visitas_acumuladas.items()
                if isinstance(nodo, tuple) and nodo not in canciones
            }
            recs_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
            return "; ".join(f"{cancion[0]} - {cancion[1]}" for cancion, _ in recs_ordenadas[:cantidad])
        elif tipo == USUARIOS:
            recomendaciones = {
                nodo: valor
                for nodo, valor in visitas_acumuladas.items()
                if isinstance(nodo, str) and nodo not in nodos_iniciales
            }
            recs_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
            return "; ".join(f"{usuario}" for usuario, _ in recs_ordenadas[:cantidad])
        
        raise ValueError("Tipo debe ser 'canciones' o 'usuarios'.")

def leer_entrada(entradas):
    while True:
        linea = input()
        if linea == "":
            break
        entradas.append(linea)

def cargar_estructuras(recomendify, datos):
    recomendify.cargar_diccionario(datos)
    recomendify.cargar_grafo()
    recomendify.cargar_grafo_de_canciones()

def leer_archivo(ruta, datos):
    with open(ruta, 'r') as arc:
        next(arc)
        for linea in arc:
            info = linea.strip().split("\t")
            user = info[1]
            nombre_cancion = info[2]
            artista = info[3]
            nombre_playlist = info[5]
            datos.append((user, (nombre_cancion, artista), nombre_playlist))

def separar_datos(info):
    mas_datos = info.split(" ", 1)
    if len(mas_datos) < 2:
        return None, None
    largo = int(mas_datos[0])
    cancion = mas_datos[1].split(" - ", 1)
    inicio = (cancion[0], cancion[1])
    return largo, inicio

def guardar_canciones(divididas, canciones):
    for cancion in divididas:
        actual = cancion.split(" - ", 1)
        canciones.append((actual[0], actual[1]))

def main():
    param = argparse.ArgumentParser(None)
    param.add_argument("ruta", type=str)
    archivo = param.parse_args()

    if not os.path.isfile(archivo.ruta):
        return "El archivo no existe"

    imp = []
    leer_archivo(archivo.ruta, imp)
    recomendify = Recomendify()
    cargar_estructuras(recomendify, imp)
    entradas = []
    leer_entrada(entradas)

    for entrada in entradas:
        datos = entrada.split(" ", 1)
        comando = datos[0]
        resto = datos[1] if len(datos) > 1 else ""
        if comando == CAMINO:
            canciones = resto.split(" >>>> ")
            if len(canciones) < 2:
                print("Error: formato de camino incorrecto.")
                continue
            primer_cancion = canciones[0].split(" - ", 1)
            segunda_cancion = canciones[1].split(" - ", 1)
            if len(primer_cancion) < 2 or len(segunda_cancion) < 2:
                print("Tanto el origen como el destino deben ser canciones")
                continue
            camino = recomendify.camino_minimo((primer_cancion[0], primer_cancion[1]), (segunda_cancion[0], segunda_cancion[1]))
            print(camino)
        elif comando == IMPORTANTES:
            resto = int(resto)
            canciones = recomendify.mas_importantes(resto)
            print(canciones)
        elif comando == RECOMENDACION:
            info = resto.split(" ", 2)
            tipo = info[0]
            cantidad = int(info[1]) if len(info) > 1 else 0
            canciones = info[2] if len(info) > 2 else ""
            divididas = canciones.split(" >>>> ")
            canciones = []
            guardar_canciones(divididas, canciones)
            recomendaciones = recomendify.recomendar(recomendify.grafo_bipartito, tipo, cantidad, canciones, 50, 5000)
            print(recomendaciones)
        elif comando == CICLO:
            largo, inicio = separar_datos(resto)
            if largo is None:
                print("Error: formato de ciclo incorrecto.")
                continue
            ciclo = recomendify.buscar_ciclo_n(inicio, largo)
            print(ciclo)
        else:
            saltos, tupla = separar_datos(resto)
            if saltos is None:
                print("Error: formato de salto incorrecto.")
                continue
            rango = recomendify.rango(saltos, tupla)
            print(rango)

if __name__ == "__main__":
    main()

