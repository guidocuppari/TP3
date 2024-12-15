import random

class Grafo:
    def __init__(self, es_dirigido, vertices = None):
        self.es_dirigido = es_dirigido
        self.vertices = {}
        if vertices is None:
            return
        else:
            for v in vertices:
                self.agregar_vertice(v)

    def agregar_vertice(self, v):
        if not v in self.vertices:
            self.vertices[v] = {}

    def borrar_vertice(self, v):
        if v not in self.vertices:
            raise AssertionError("El vertice no pertenece al grafo")
        if v in self.vertices:
            self.vertices.pop(v)
        for _, dato in self.vertices:
            if v in dato:
                dato.pop(v)

    def agregar_arista(self, v, w, peso = 1):
        if v not in self.vertices and w in self.vertices:
            raise AssertionError("Algun vertice no pertenece al grafo")
        dato_v = self.vertices[v]
        dato_v[w] = peso
        if not self.es_dirigido:
            dato_w = self.vertices[w]
            dato_w[w] = peso
    def borrar_arista(self, v, w):
        if v not in self.vertices and w in self.vertices:
            raise AssertionError("Algun vertice no pertenece al grafo")

        self.vertices[v].pop(w)
        if not self.es_dirigido:
            self.vertices[w].pop(v)
    def estan_unidos (self, v, w):
        if v not in self.vertices and w in self.vertices:
            raise AssertionError("Algun vertice no pertenece al grafo")
        if v in self.vertices[w]:
            return True
        else:
            return False

    def peso_arista(self, v, w):
        if v not in self.vertices and w in self.vertices:
            raise AssertionError("Algun vertice no pertenece al grafo")
        dato_v = self.vertices[v]
        return float(dato_v[w])

    def obtener_vertices(self):
        vertices = []
        for v in self.vertices:
            vertices.append(v)
        return vertices

    def adyacentes(self, v):
        if v not in self.vertices:
            raise AssertionError("El vertice no pertenece al grafo")
        vertices_adyacentes = []
        for w in self.vertices[v]:
            vertices_adyacentes.append(w)
        return vertices_adyacentes

    def vertice_aleatorio(self):
        if len(self.vertices) == 0:
            raise AssertionError("El grafo no tiene vertices")
        vertices = self.obtener_vertices()
        return vertices[random.randint(0, len(self.vertices))]

    def grado_salida(self, vertice):
        return len(self.adyacentes(vertice))