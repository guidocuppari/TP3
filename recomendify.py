#!/usr/bin/env python3
from grafo import Grafo
from biblioteca import camino_minimo_bfs, bfs_distancias, dfs_ciclo_n, random_walk_multiples
import argparse
import os
from informacion import leer_entrada, leer_archivo, efectuar_comandos

CANCIONES = "canciones"
USUARIOS = "usuarios"
NOMBRE_CANCION = 0
ARTISTA = 1

class Recomendify:
    def __init__(self):
        self.grafo_bipartito = Grafo()
        self.diccionario = {} #dicionario con el nombre como clave y el valor es una tupla de cancion y playlist en la que aparece
        self.grafo_canciones = Grafo()
        self.pagerank_cache = None

    def cargar_diccionario(self, datos):
        for usuario, cancion, playlist in datos:
            if usuario not in self.diccionario:
                self.diccionario[usuario] = {}
            self.diccionario[usuario][(cancion[NOMBRE_CANCION], cancion[ARTISTA])] = playlist

    def agregar_nuevo_vertice(self, grafo, vertice, agregados):
        if vertice not in agregados:
            grafo.agregar_vertice(vertice)
            agregados.add(vertice)
        
    def cargar_grafo(self):
        vertices_agregados = set()
        for usuario, canciones in self.diccionario.items():
            self.agregar_nuevo_vertice(self.grafo_bipartito, usuario, vertices_agregados)
            for cancion in canciones.keys():
                self.agregar_nuevo_vertice(self.grafo_bipartito, cancion, vertices_agregados)
                self.grafo_bipartito.agregar_arista(usuario, cancion)
        
    def mensaje_camino_usuario(self, resultado, origen, destino, playlist, visitados_usuarios):
        if origen in visitados_usuarios:
            resultado.append(f"tiene una playlist --> {playlist} --> donde aparece --> {destino[NOMBRE_CANCION]} - {destino[ARTISTA]}")
            return
        resultado.append(f"{destino[NOMBRE_CANCION]} - {destino[ARTISTA]} --> aparece en playlist --> {playlist} --> de --> {origen}")
    
    def mensaje_camino_cancion(self, resultado, origen, destino, playlist, visitados_canciones):
        if origen in visitados_canciones:
            resultado.append(f"aparece en playlist --> {playlist} --> de --> {destino}")
            return
        resultado.append(f"{origen[NOMBRE_CANCION]} - {origen[ARTISTA]} --> aparece en playlist --> {playlist} --> de --> {destino}")

    def armar_resultado_camino(self, recorrido, resultado):
        canciones_visitadas = set()
        usuarios_visitados = set()

        for i in range(len(recorrido) - 1):
            origen = recorrido[i]
            destino = recorrido[i + 1]
            if origen in self.diccionario:
                canciones_visitadas.add(destino)
                playlist = self.diccionario[origen].get(destino)
                self.mensaje_camino_usuario(resultado, origen, destino, playlist, usuarios_visitados)
            elif destino in self.diccionario:
                usuarios_visitados.add(destino)
                playlist = self.diccionario[destino].get(origen)
                self.mensaje_camino_cancion(resultado, origen, destino, playlist, canciones_visitadas)

    def error_existencia_vertice(self, vertice):
        return f"Error: {vertice} no está en el grafo"
    
    def restaurar_recorrido(self, vertice, recorrido, padres):
        actual = vertice
        while actual is not None:
            recorrido.append(actual)
            actual = padres.get(actual)
        recorrido.reverse()

    def camino_minimo(self, cancion_origen, cancion_destino):
        if cancion_origen not in self.grafo_bipartito.obtener_vertices():
            return self.error_existencia_vertice(cancion_origen)
        if cancion_destino not in self.grafo_bipartito.obtener_vertices():
            return self.error_existencia_vertice(cancion_destino)

        padres, _ = camino_minimo_bfs(self.grafo_bipartito, cancion_origen)
        if cancion_destino not in padres:
            return "No se encontro recorrido"

        recorrido = []
        self.restaurar_recorrido(cancion_destino, recorrido, padres)
        resultado = []
        self.armar_resultado_camino(recorrido, resultado)
        return " --> ".join(resultado)

    def pagerank(self, d=0.85, iteraciones=100, tolerancia=1e-6):
        if self.pagerank_cache is not None:
            return self.pagerank_cache

        vertices = self.grafo_bipartito.obtener_vertices()
        N = len(vertices)
        if N == 0:
            return {}

        grados_salida = {v: self.grafo_bipartito.grado_salida(v) or 1 for v in vertices}
        pagerank_actual = {v: 1 / N for v in vertices}
        for _ in range(iteraciones):
            cambio_total = 0
            pagerank_nuevo = {v: (1 - d) / N for v in vertices}
            for v in vertices:
                contribucion = d * pagerank_actual[v] / grados_salida[v]
                for u in self.grafo_bipartito.obtener_adyacentes(v):
                    pagerank_nuevo[u] += contribucion

            for v in vertices:
                cambio_total += abs(pagerank_nuevo[v] - pagerank_actual[v])
                pagerank_actual[v] = pagerank_nuevo[v]

            if cambio_total < tolerancia:
                break

        self.pagerank_cache = pagerank_actual
        return pagerank_actual

    def invalidar_pagerank(self):
        self.pagerank_cache = None

    def mas_importantes(self, n):
        pagerank = self.pagerank()
        canciones_importantes = [
            (nodo, valor) for nodo, valor in pagerank.items() if self.es_cancion(nodo)
        ]
        canciones_importantes.sort(key=lambda x: x[1], reverse=True)
        return "; ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion, _ in canciones_importantes[:n])

    def es_cancion(self, nodo):
        return isinstance(nodo, tuple) and len(nodo) == 2

    def cargar_grafo_de_canciones(self):
        visitados = set()
        for canciones in self.diccionario.values():
            for cancion in canciones.keys():
                self.agregar_nuevo_vertice(self.grafo_canciones, cancion, visitados)

        for canciones in self.diccionario.values():
            canciones_usuario = list(canciones.keys())
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
        if resultado is None:
            return "No se encontro recorrido"
        
        return " --> ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion in resultado)

    def recomendar(self, grafo, tipo, cantidad, canciones, largo=100, iteraciones=500):
        nodos_iniciales = [cancion for cancion in canciones]
        visitas_acumuladas = random_walk_multiples(grafo, nodos_iniciales, largo, iteraciones)
        if tipo == CANCIONES:
            recomendaciones = {
                nodo: valor
                for nodo, valor in visitas_acumuladas.items()
                if isinstance(nodo, tuple) and nodo not in canciones
            }
            recs_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
            return "; ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion, _ in recs_ordenadas[:cantidad])
        elif tipo == USUARIOS:
            recomendaciones = {
                nodo: valor
                for nodo, valor in visitas_acumuladas.items()
                if isinstance(nodo, str) and nodo not in nodos_iniciales
            }
            recs_ordenadas = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
            return "; ".join(f"{usuario}" for usuario, _ in recs_ordenadas[:cantidad])
        
        raise ValueError("Tipo debe ser 'canciones' o 'usuarios'.")

def cargar_estructuras(recomendify, datos):
    recomendify.cargar_diccionario(datos)
    recomendify.cargar_grafo()

archivo = ""  
def main():
    param = argparse.ArgumentParser(None)
    param.add_argument("ruta", type=str)
    archivo = param.parse_args()

    if not os.path.isfile(archivo.ruta):
        return "El archivo no existe"

if __name__ == "__main__":
    main()

imp = []
leer_archivo(archivo.ruta, imp)
recomendify = Recomendify()
cargar_estructuras(recomendify, imp)
entradas = []
leer_entrada(entradas)
efectuar_comandos(recomendify, entradas)