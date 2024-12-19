from auxiliar.biblioteca import dfs_ciclo_n
from auxiliar.estructuras import grafo_canciones
from auxiliar.constantes import NOMBRE_CANCION, ARTISTA

def buscar_ciclo_n(inicio, largo):
    visitados = [inicio]
    camino = [inicio]
    resultado = dfs_ciclo_n(grafo_canciones, inicio, visitados, camino, largo)
    if resultado is None:
        return "No se encontro recorrido"
    
    return " --> ".join(f"{cancion[NOMBRE_CANCION]} - {cancion[ARTISTA]}" for cancion in resultado)