from biblioteca import camino_minimo_bfs
from estructuras import diccionario, grafo_bipartito
from funciones_auxiliares import NOMBRE_CANCION, ARTISTA

def mensaje_camino_usuario(resultado, origen, destino, playlist, visitados_usuarios):
    if origen in visitados_usuarios:
        resultado.append(f"tiene una playlist --> {playlist} --> donde aparece --> {destino[NOMBRE_CANCION]} - {destino[ARTISTA]}")
        return
    resultado.append(f"{destino[NOMBRE_CANCION]} - {destino[ARTISTA]} --> aparece en playlist --> {playlist} --> de --> {origen}")
    
def mensaje_camino_cancion(resultado, origen, destino, playlist, visitados_canciones):
    if origen in visitados_canciones:
        resultado.append(f"aparece en playlist --> {playlist} --> de --> {destino}")
        return
    resultado.append(f"{origen[NOMBRE_CANCION]} - {origen[ARTISTA]} --> aparece en playlist --> {playlist} --> de --> {destino}")

def armar_resultado_camino(recorrido, resultado):
    canciones_visitadas = set()
    usuarios_visitados = set()

    for i in range(len(recorrido) - 1):
        origen = recorrido[i]
        destino = recorrido[i + 1]
        if origen in diccionario:
            canciones_visitadas.add(destino)
            playlist = diccionario[origen].get(destino)
            mensaje_camino_usuario(resultado, origen, destino, playlist, usuarios_visitados)
        elif destino in diccionario:
            usuarios_visitados.add(destino)
            playlist = diccionario[destino].get(origen)
            mensaje_camino_cancion(resultado, origen, destino, playlist, canciones_visitadas)

def error_existencia_vertice(vertice):
    return f"Error: {vertice} no está en el grafo"
    
def restaurar_recorrido(vertice, recorrido, padres):
    actual = vertice
    while actual is not None:
        recorrido.append(actual)
        actual = padres.get(actual)
    recorrido.reverse()

def camino_minimo(cancion_origen, cancion_destino):
    if cancion_origen not in grafo_bipartito.obtener_vertices():
        return error_existencia_vertice(cancion_origen)
    if cancion_destino not in grafo_bipartito.obtener_vertices():
        return error_existencia_vertice(cancion_destino)

    padres, _ = camino_minimo_bfs(grafo_bipartito, cancion_origen)
    if cancion_destino not in padres:
        return "No se encontro recorrido"

    recorrido = []
    restaurar_recorrido(cancion_destino, recorrido, padres)
    resultado = []
    armar_resultado_camino(recorrido, resultado)
    return " --> ".join(resultado)
