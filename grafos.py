import random

class Grafo:
    def __init__(self, es_dirigido=False, vertices_init=[]):
        # Indica si el grafo es dirigido o no
        self.dirigido = es_dirigido
        # Diccionario para almacenar los vértices y sus adyacencias (con pesos de arista)
        self.adyacentes = {v: {} for v in vertices_init}

    def agregar_vertice(self, v):
        # Agrega un nuevo vértice al grafo si no existe
        if v not in self.adyacentes:
            self.adyacentes[v] = {}

    def borrar_vertice(self, v):
        # Elimina el vértice y sus aristas
        if v in self.adyacentes:
            # Elimina todas las aristas que apuntan al vértice en otros vértices
            for w in list(self.adyacentes[v].keys()):
                self.borrar_arista(v, w)
            del self.adyacentes[v]

    def agregar_arista(self, v, w, peso=1):
        # Asegurarse de que ambos vértices existan
        self.agregar_vertice(v)
        self.agregar_vertice(w)
        # Agrega arista con el peso indicado
        self.adyacentes[v][w] = peso
        if not self.dirigido:
            self.adyacentes[w][v] = peso

    def borrar_arista(self, v, w):
        # Elimina la arista de v a w (y de w a v si es no dirigido)
        if v in self.adyacentes and w in self.adyacentes[v]:
            del self.adyacentes[v][w]
        if not self.dirigido and w in self.adyacentes and v in self.adyacentes[w]:
            del self.adyacentes[w][v]

    def estan_unidos(self, v, w):
        # Verifica si hay una arista entre v y w
        return v in self.adyacentes and w in self.adyacentes[v]

    def peso_arista(self, v, w):
        # Devuelve el peso de la arista entre v y w si existe
        if self.estan_unidos(v, w):
            return self.adyacentes[v][w]
        return None

    def obtener_vertices(self):
        # Devuelve una lista con todos los vértices del grafo
        return list(self.adyacentes.keys())

    def vertice_aleatorio(self):
        # Devuelve un vértice aleatorio del grafo
        if not self.adyacentes:
            return None
        return random.choice(list(self.adyacentes.keys()))

    def obtener_adyacentes(self, v):
        # Devuelve los adyacentes al vértice v (como lista)
        if v in self.adyacentes:
            return list(self.adyacentes[v].keys())
        return []

    def _str_(self):
        # Representación en cadena del grafo
        resultado = []
        for v, ady in self.adyacentes.items():
            for w, peso in ady.items():
                if self.dirigido or (v <= w):  # Evita duplicados si el grafo no es dirigido
                    resultado.append(f"{v} <--> {w} (peso: {peso})")
        return "\n".join(resultado)

    def grado_salida(self, v):
        if v not in self.adyacentes:
            raise ValueError(f"El vértice '{v}' no existe en el grafo.")
        return len(self.adyacentes[v])
