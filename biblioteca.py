import random
from collections import defaultdict
from grafos import Grafo
from heap import Heap
from cola import Cola

def camino_minimo_dijkstra(grafo, origen, destino):
    distancia, padres = {}
    for v in grafo:
        distancia[v] = float('inf')
    distancia[origen] = 0
    padres [origen] = None
    q = Heap()
    q.encolar(0, origen)
    while not q.esta_vacia():
        _, v = q.desencolar()
        if v == destino:
            return padres, distancia
        for w in grafo.obtener_adyacentes(v):
            if (distancia[v] + float(grafo.peso_arista(v, w)) < distancia[w]):
                distancia[w] = distancia[v] + float(grafo.peso_arista(v, w))
                padres[w] = v
                q.encolar(w, distancia[w])
            return padres, distancia


def camino_minimo_bfs(grafo, origen):
    distancia, padres, visitado = {}, {}, {}

    for v in grafo.obtener_vertices():
        distancia[v] = float('inf')
    distancia[origen] = 0
    padres[origen] = None
    visitado[origen] = False
    q = Cola()
    q.encolar(origen)

    while not q.esta_vacia():
        v = q.desencolar()
        for w in grafo.obtener_adyacentes(v):
            if w not in visitado:
                distancia[w] = distancia[v] + 1
                padres[w] = v
                visitado[w] = True
                q.encolar(w)

    return padres, distancia

def mst_prim(grafo, distancias):
    v = grafo.vertice_aleatorio()
    visitados = set()
    visitados.add(v)
    q = Heap()
    for w in grafo.obtener_adyacentes(v):
        q.encolar(grafo.peso_arista(v, w), w)
    arbol = Grafo(es_dirigido=False, vertices=grafo.obtener_vertices())
    while not q.esta_vacia():
        peso, w = q.desencolar()
        if w in visitados:
            continue
        arbol.agregar_arista(v, w, peso)
        visitados.add(w)
        for x in grafo.obtener_adyacentes(w):
            if x not in visitados:
                q.encolar(grafo.peso_arista(x, w), x)
    return arbol

def ordenar_vertices(grafo, distancias):
    vertices = grafo.obtener_vertices()
    vertices_ordenados = sorted(vertices, key=lambda v: distancias[v])
    return vertices_ordenados

def centralidad(grafo):
    cent = {}
    for v in grafo.obtener_vertices():
        cent[v] = 0
    for v in grafo.obtener_vertices():
        padre, distancias = camino_minimo_dijkstra(grafo, v)
        cent_aux = {}
        for w in grafo.obtener_vertices():
            cent_aux[w] = 0
        vertices_ordenados = ordenar_vertices(grafo, distancias)
        for w in vertices_ordenados:
            if padre[w] is None: continue
            cent_aux[padre[w]] += 1 + cent_aux[w]
        for w in grafo.obtener_vertices():
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent

def grados_entrada(grafo):
    entrada = {}
    for v in grafo.obtener_vertices():
        entrada[v] = 0
    for v in grafo.obtener_vertices():
        for w in grafo.obtener_adyacentes(v):
            entrada[w] += 1
    return entrada

def topologico_entrada(grafo):
    entrada = grados_entrada(grafo)
    q = Cola()
    for v in grafo.obtener_vertices():
        if entrada[v] == 0:
            q.encolar(v)
    resultado = []
    while not q.esta_vacia():
        v = q.desencolar()
        resultado.append(v)
        for w in grafo.obtener_adyacentes(v):
            entrada[w] -= 1
            if entrada[w] == 0:
                q.encolar(w)
    return resultado

def dfs_ciclo_n(grafo, actual, visitados, camino, largo):
    inicio = camino[0]
    if len(visitados) == largo and inicio == visitados[0]:
        camino.append(inicio)
        return camino

    for vecino in grafo.obtener_adyacentes(actual):
        if vecino not in visitados:
            visitados.append(vecino)
            camino.append(vecino)
            resultado = dfs_ciclo_n(grafo, vecino, visitados, camino, largo)
            if resultado:
                return resultado
            visitados.pop()
            camino.pop()
    return None

def bfs_distancias(grafo, origen, n):
    distancias = {}
    lista = []
    q = Cola()
    q.encolar(origen)
    distancias[origen] = 0

    while not q.esta_vacia():
        v = q.desencolar()
        if distancias[v] > n:
            return lista
        for w in grafo.obtener_adyacentes(v):
            if w not in distancias:
                distancias[w] = distancias[v] + 1
                q.encolar(w)
                if distancias[w] == n:
                    lista.append(w)
    return lista

def nodos_similares(grafo, nodos_interes, largo_recorrido=100, iteraciones=1000):
    visitas_acumuladas = random_walk_multiples(grafo, nodos_interes, largo_recorrido, iteraciones)
    similares = sorted(visitas_acumuladas.items(), key=lambda x: x[1], reverse=True)
    return similares

def random_walk_multiples(grafo, nodos_iniciales, largo_recorrido, iteraciones):
    visitas_acumuladas = defaultdict(float)

    for _ in range(iteraciones):
        nodo_inicial = random.choice(nodos_iniciales)
        visitas = random_walk(grafo, nodo_inicial, largo_recorrido)
        for nodo, valor in visitas.items():
            visitas_acumuladas[nodo] += valor

    return visitas_acumuladas

def random_walk(grafo, nodo_inicial, largo_recorrido):
    visitas = defaultdict(float)
    nodo_actual = nodo_inicial
    valor = 1.0

    for _ in range(largo_recorrido):
        visitas[nodo_actual] += valor
        adyacentes = grafo.obtener_adyacentes(nodo_actual)

        if not adyacentes:  # Nodo sin conexiones
            break

        grado_salida = len(adyacentes)
        valor /= grado_salida
        nodo_actual = random.choice(adyacentes)

    return visitas
