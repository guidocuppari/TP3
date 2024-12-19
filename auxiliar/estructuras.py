from tdas.grafo import Grafo
from auxiliar.constantes import NOMBRE_CANCION, ARTISTA

grafo_bipartito = Grafo()
diccionario = {} #dicionario con el nombre como clave y el valor es una tupla de cancion y playlist en la que aparece
grafo_canciones = Grafo()

class Pagerank:
    def __init__(self):
        self.pagerank_cache = None
    
    def pagerank(self, d=0.85, iteraciones=100, tolerancia=1e-6):
        if self.pagerank_cache is not None:
            return self.pagerank_cache

        vertices = grafo_bipartito.obtener_vertices()
        N = len(vertices)
        if N == 0:
            return {}

        grados_salida = {v: grafo_bipartito.grado_salida(v) or 1 for v in vertices}
        pagerank_actual = {v: 1 / N for v in vertices}
        for _ in range(iteraciones):
            cambio_total = 0
            pagerank_nuevo = {v: (1 - d) / N for v in vertices}
            for v in vertices:
                contribucion = d * pagerank_actual[v] / grados_salida[v]
                for u in grafo_bipartito.obtener_adyacentes(v):
                    pagerank_nuevo[u] += contribucion

            for v in vertices:
                cambio_total += abs(pagerank_nuevo[v] - pagerank_actual[v])
                pagerank_actual[v] = pagerank_nuevo[v]

            if cambio_total < tolerancia:
                break

        self.pagerank_cache = pagerank_actual
        return pagerank_actual

def cargar_diccionario(datos):
    for usuario, cancion, playlist in datos:
        if usuario not in diccionario:
            diccionario[usuario] = {}
        diccionario[usuario][(cancion[NOMBRE_CANCION], cancion[ARTISTA])] = playlist

def agregar_nuevo_vertice(grafo, vertice, agregados):
    if vertice not in agregados:
        grafo.agregar_vertice(vertice)
        agregados.add(vertice)
    
def cargar_grafo():
    vertices_agregados = set()
    for usuario, canciones in diccionario.items():
        agregar_nuevo_vertice(grafo_bipartito, usuario, vertices_agregados)
        for cancion in canciones.keys():
            agregar_nuevo_vertice(grafo_bipartito, cancion, vertices_agregados)
            grafo_bipartito.agregar_arista(usuario, cancion)

def cargar_grafo_de_canciones():
    visitados = set()
    for canciones in diccionario.values():
        for cancion in canciones.keys():
            agregar_nuevo_vertice(grafo_canciones, cancion, visitados)

    for canciones in diccionario.values():
        canciones_usuario = list(canciones.keys())
        for i in range(len(canciones_usuario)):
            for j in range(i + 1, len(canciones_usuario)):
                grafo_canciones.agregar_arista(canciones_usuario[i], canciones_usuario[j])