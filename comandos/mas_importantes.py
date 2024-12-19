from auxiliar.constantes import NOMBRE_CANCION, ARTISTA
from auxiliar.estructuras import Pagerank

pr = Pagerank()
def calcular_pagerank():
    pagerank_canciones = pr.pagerank()
    return pagerank_canciones

def es_cancion(nodo):
    return isinstance(nodo, tuple) and len(nodo) == 2

def mas_importantes(n):
    pagerank_canciones = calcular_pagerank()
    canciones_importantes = [
        (nodo, valor) for nodo, valor in pagerank_canciones.items() if es_cancion(nodo)
    ]
    canciones_importantes.sort(key=lambda x: x[1], reverse=True)
    return "; ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion, _ in canciones_importantes[:n])