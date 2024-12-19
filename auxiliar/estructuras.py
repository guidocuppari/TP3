from tdas.grafo import Grafo
from auxiliar.constantes import NOMBRE_CANCION, ARTISTA

grafo_bipartito = Grafo()
diccionario = {} #dicionario con el nombre como clave y el valor es una tupla de cancion y playlist en la que aparece
grafo_canciones = Grafo()

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