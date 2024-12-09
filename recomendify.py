from grafos import Grafo
from heap import Heap
from pila import PilaDinamica
from biblioteca import camino_minimo_bfs


class Recomendify:
    def __init__(self):
        self.grafo_bipartito = Grafo(es_dirigido=False)
        self.grafo_playlists = Grafo(es_dirigido=False)
        self.diccionario = {} #dicionario con el nombre como clave y el valor es una tupla de cancion y playlist en la que aparece

    def cargar_diccionario (self, datos):
        for nombre, playlist, cancion in datos:
            if nombre not in self.diccionario:
                self.diccionario[nombre] = []
            self.diccionario[nombre].append(cancion, playlist)

    def cargar_grafo(self):
        for (user_id, nombre), canciones in self.diccionario.items():
            self.grafo_bipartito.agregar_vertice(nombre)
            for cancion,_ in canciones:
                if cancion not in self.grafo_bipartito.obtener_vertices(self.grafo_bipartito):
                    self.grafo_bipartito.agregar_vertice(cancion)
                self.grafo_bipartito.agregar_arista(user_id, cancion)

    def camino_minimo(self, cancion_origen, cancion_destino):
        padres, _ = camino_minimo_bfs(self.grafo_bipartito, cancion_origen)

        if cancion_destino not in padres:
            return "No se encontró recorrido"

        recorrido = []
        actual = cancion_destino
        while actual is not None:
            recorrido.append(actual)
            actual = padres[actual]

        recorrido.reverse()
        resultado = []
        for i in range(len(recorrido) - 1):
            origen = recorrido[i]
            destino = recorrido[i + 1]

            if origen in self.diccionario:
                playlist = next((p for c, p in self.diccionario[origen] if c == destino), None)
                resultado.append(f"{destino} --> aparece en playlist --> {playlist} --> de --> {origen}")
            elif destino in self.diccionario:
                playlist = next((p for c, p in self.diccionario[destino] if c == origen), None)
                resultado.append(f"{origen} --> aparece en playlist --> {playlist} --> de --> {destino}")
            else:
                resultado.append(f"{origen} --> donde aparece --> {destino}")

        return " --> ".join(resultado)

    def obtener_playlist(self, usuario, cancion):
        for c, playlist in self.diccionario[usuario]:
            if c == cancion:
                return playlist
            return None



