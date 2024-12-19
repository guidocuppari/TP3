from biblioteca import dfs_ciclo_n
from estructuras import grafo_canciones
from funciones_auxiliares import NOMBRE_CANCION, ARTISTA

def buscar_ciclo_n(inicio, largo):
    visitados = [inicio]
    camino = [inicio]
    resultado = dfs_ciclo_n(grafo_canciones, inicio, visitados, camino, largo)
    if resultado is None:
        return "No se encontro recorrido"
    
    return " --> ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion in resultado)