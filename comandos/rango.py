from auxiliar.biblioteca import bfs_distancias
from auxiliar.estructuras import grafo_canciones

def rango(n, cancion_inicio):
    if cancion_inicio not in grafo_canciones.obtener_vertices():
        return 0

    canciones_a_n_saltos = bfs_distancias(grafo_canciones, cancion_inicio, n)
    return len(canciones_a_n_saltos)