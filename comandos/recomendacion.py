from auxiliar.biblioteca import random_walk_multiples
from auxiliar.constantes import NOMBRE_CANCION, ARTISTA, CANCIONES, USUARIOS

def recomendar(grafo, tipo, cantidad, canciones, largo=100, iteraciones=500):
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