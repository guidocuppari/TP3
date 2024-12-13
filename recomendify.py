from grafos import Grafo
from heap import Heap
from pila import PilaDinamica
from biblioteca import camino_minimo_bfs, dfs, bfs_distancias
import argparse
import os


class Recomendify:
    def __init__(self):
        self.grafo_bipartito = Grafo(es_dirigido=False)
        self.diccionario = {} #dicionario con el nombre como clave y el valor es una tupla de cancion y playlist en la que aparece

    def cargar_diccionario(self, datos):
        for nombre, cancion, playlist in datos:
            if nombre not in self.diccionario:
                self.diccionario[nombre] = []
            self.diccionario[nombre].append(cancion, playlist)

    def cargar_grafo(self):
        for (user_id, nombre), canciones in self.diccionario.items():
            self.grafo_bipartito.agregar_vertice(nombre)
            for cancion,_ in canciones:
                if cancion not in self.grafo_bipartito.obtener_vertices(self.grafo_bipartito):
                    self.grafo_bipartito.agregar_vertice(cancion)
                self.grafo_bipartito.agregar_arista(user_id, cancion)

    def camino_minimo(self, cancion_origen, cancion_destino):
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
        for i in range(len(recorrido) - 1):
            origen = recorrido[i]
            destino = recorrido[i + 1]

            if origen in self.diccionario:
                playlist = next((p for c, p in self.diccionario[origen] if c == destino), None)
                resultado.append(f"{destino} --> aparece en playlist --> {playlist} --> de --> {origen}")
            elif destino in self.diccionario:
                playlist = next((p for c, p in self.diccionario[destino] if c == origen), None)
                resultado.append(f"{origen} --> aparece en playlist --> {playlist} --> de --> {destino}")
            else:
                resultado.append(f"{origen} --> donde aparece --> {destino}")

        return " --> ".join(resultado)

    def calcular_page_rank(self, d = 0.85, iteraciones = 100):
        nodos = self.grafo_bipartito.obtener_vertices()
        n = len(nodos)
        pagerank = {nodo: 1 / n for nodo in nodos}

        for _ in range(iteraciones):
            nuevo_pagerank = {}
            for nodo in nodos:
                suma = 0
                for vecino in self.grafo_bipartito.adyacentes(nodo):
                    suma += pagerank[vecino] / self.grafo_bipartito.grado_salida(vecino)
                    nuevo_pagerank[nodo] = (1 - d) / n + d * suma
                pagerank = nuevo_pagerank

                return pagerank

    def es_cancion(self, nodo):
        return nodo not in self.diccionario

    def mas_importantes(self, n):
        pagerank = self.calcular_page_rank(self.grafo_bipartito)

        canciones = {
            nodo: valor for nodo, valor in pagerank.items() if self.es_cancion(nodo)
        }
        canciones_ordenadas = sorted(canciones, key=lambda x: x[1], reverse=True)

        return canciones_ordenadas[:n]

    def page_rank_personalizado(self, cancion, d = 0.85, iteraciones = 100):
        nodos = self.grafo_bipartito.obtener_vertices()
        n = len(nodos)
        pagerank = {nodo: 1 / n for nodo in nodos}

        probas = {nodo: (1 if nodo == cancion else 0) for nodo in nodos}
        probas = {nodo: valor/sum(probas.values()) for nodo, valor in probas.items()}

        for _ in range(iteraciones):
            nuevo_pagerank = {}
            for nodo in nodos:
                suma = 0
                for vecino in self.grafo_bipartito.adyacentes(nodo):
                    suma += pagerank[vecino] / self.grafo_bipartito.grado_salida(vecino)
                nuevo_pagerank[nodo] = (1 - d) * probas[nodo] + d * suma
            pagerank = nuevo_pagerank

        return pagerank

    def recomendar_canciones(self, n, canciones):
        recomendaciones = {}
        for cancion in canciones:
            pagerank_perso = self.page_rank_personalizado(self.grafo_bipartito, cancion)
            canciones = {
                nodo: valor for nodo, valor in pagerank_perso.items() if self.es_cancion(nodo)
            }
            canciones_ordenadas = sorted(canciones, key=lambda x: x[1], reverse=True)
            similares = [nodo for nodo, _ in canciones_ordenadas if nodo != cancion]
            recomendaciones[cancion] = similares

        return recomendaciones

    def recomendar_usuarios(self, n, canciones):
        recomendaciones = {}
        for cancion in canciones:
            pagerank_perso = self.page_rank_personalizado(self.grafo_bipartito, cancion)
            usuarios = {
                nodo: valor for nodo, valor in pagerank_perso.items() if not self.es_cancion(nodo)
            }
            usuarios_ordenados = sorted(usuarios, key=lambda x: x[1], reverse=True)
            similares = [nodo for nodo, _ in usuarios_ordenados]
            recomendaciones[cancion] = similares
        
        return recomendaciones

    def reconstruir_ciclo(padres, inicio, contador):
        v = inicio
        camino = []
        while contador > 0 or padres[v] != None:
            contador -= 1
            camino.append(v)
            v = padres[v]
        camino.append(v)
        return camino

    def ciclo_n_canciones(self, n, cancion):
        padres, _ = dfs(self.grafo_bipartito, cancion)
        cont = n
        ciclo = self.reconstruir_ciclo(padres, cancion, cont)
        if len(ciclo) != n:
            return "No se encontro recorrido"
        
        ciclo_unido = [f"{cancion} -->" for cancion in ciclo[:-1]] + [ciclo[-1]]
        return ciclo_unido

    def todas_en_rango(self, n, cancion):
        en_rango = bfs_distancias(self.grafo_bipartito, cancion, n)
        return len(en_rango)
        

def main():
    param = argparse.ArgumentParser(None)
    param.add_argument("ruta", type=str)
    archivo = param.parse_args()

    if not os.path.isfile(archivo.ruta):
        return "Error"
    
    with open(archivo.ruta, 'r') as arc:
        for linea in arc:
            info = linea.strip().split("\t")
            imp = []
            imp.append((info[1], info[2], info[5]))

    for datos in imp:
        Recomendify.cargar_diccionario(datos)
    
    Recomendify.cargar_grafo()
    


if __name__ == "__main__":
    main()

