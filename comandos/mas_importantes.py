from auxiliar.estructuras import grafo_bipartito
from auxiliar.constantes import NOMBRE_CANCION, ARTISTA

def es_cancion(nodo):
    return isinstance(nodo, tuple) and len(nodo) == 2

def pagerank(pagerank_cache, d=0.85, iteraciones=100, tolerancia=1e-6):
    if pagerank_cache is not None:
        return pagerank_cache

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

    pagerank_cache = pagerank_actual
    return pagerank_actual

def mas_importantes(n, pagerank_cache):
    pagerank_canciones = pagerank(pagerank_cache)
    canciones_importantes = [
        (nodo, valor) for nodo, valor in pagerank_canciones.items() if es_cancion(nodo)
    ]
    canciones_importantes.sort(key=lambda x: x[1], reverse=True)
    return "; ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion, _ in canciones_importantes[:n])