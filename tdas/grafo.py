import random

def errores_vertice(self, vertice):
    if vertice not in self.vertices_adyacentes:
        return f"El vértice '{vertice}' no existe en el grafo."
    return None

def error_arista(self, v, w):
    if not self.estan_unidos(v, w):
        return f"No existe arista entre los vértices recibidos."
    return None
    
class Grafo:
    def __init__(self, es_dirigido=False, vertices_init=[]):
        self.dirigido = es_dirigido
        self.vertices_adyacentes = {}
        for v in vertices_init:
            self.agregar_vertice(v)

    def agregar_vertice(self, v):
        if v not in self.vertices_adyacentes:
            self.vertices_adyacentes[v] = {}

    def borrar_vertice(self, v):
        mensaje_error = errores_vertice(self, v)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        if v in self.vertices_adyacentes:
            for w in list(self.vertices_adyacentes[v].keys()):
                self.borrar_arista(v, w)
            del self.vertices_adyacentes[v]

    def agregar_arista(self, v, w, peso=1):
        mensaje_error_v = errores_vertice(self, v)
        mensaje_error_w = errores_vertice(self, w)
        if mensaje_error_v is not None:
            raise ValueError(mensaje_error_v)
        if mensaje_error_w is not None:
            raise ValueError(mensaje_error_w)
        
        self.vertices_adyacentes[v][w] = peso
        if not self.dirigido:
            self.vertices_adyacentes[w][v] = peso

    def borrar_arista(self, v, w):
        mensaje_error = error_arista(self, v, w)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        if v in self.vertices_adyacentes and w in self.vertices_adyacentes[v]:
            del self.vertices_adyacentes[v][w]
        if not self.dirigido and w in self.vertices_adyacentes and v in self.vertices_adyacentes[w]:
            del self.vertices_adyacentes[w][v]

    def estan_unidos(self, v, w):
        mensaje_error_v = errores_vertice(self, v)
        mensaje_error_w = errores_vertice(self, w)
        if mensaje_error_v is not None:
            raise ValueError(mensaje_error_v)
        if mensaje_error_w is not None:
            raise ValueError(mensaje_error_w)
        
        return v in self.vertices_adyacentes and w in self.vertices_adyacentes[v]

    def peso_arista(self, v, w):
        mensaje_error = error_arista(self, v, w)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        return self.vertices_adyacentes[v][w]

    def obtener_vertices(self):
        return list(self.vertices_adyacentes.keys())

    def vertice_aleatorio(self):
        if not self.vertices_adyacentes:
            return None
        return random.choice(list(self.vertices_adyacentes.keys()))

    def obtener_adyacentes(self, v):
        mensaje_error = errores_vertice(self, v)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        if v in self.vertices_adyacentes:
            return list(self.vertices_adyacentes[v].keys())
        return []

    def _str_(self):
        resultado = []
        for v, ady in self.vertices_adyacentes.items():
            for w, peso in ady.items():
                if self.dirigido or (v <= w):
                    resultado.append(f"{v} <--> {w} (peso: {peso})")
        return "\n".join(resultado)

    def grado_salida(self, v):
        mensaje_error = errores_vertice(self, v)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        return len(self.vertices_adyacentes[v])

