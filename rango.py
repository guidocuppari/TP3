from biblioteca import bfs_distancias

def rango(self, n, cancion_inicio):
    if cancion_inicio not in self.grafo_canciones.obtener_vertices():
        return 0

    canciones_a_n_saltos = bfs_distancias(self.grafo_canciones, cancion_inicio, n)
    return len(canciones_a_n_saltos)