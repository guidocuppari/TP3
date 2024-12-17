import random

def errores_vertice(self, vertice):
    if vertice not in self.obtener_vertices():
        return f"El vértice '{vertice}' no existe en el grafo."
    elif vertice not in self.adyacentes:
        return f"El vértice '{vertice}' no existe en el grafo."
    return None

def error_arista(self, v, w):
    if not self.estan_unidos(v, w):
        return f"No existe arista entre los vértices recibidos."
    return None
    
class Grafo:
    def __init__(self, es_dirigido=False, vertices_init=[]):
        self.dirigido = es_dirigido
        self.vertices_adyacentes = {self.agregar_vertice(v) for v in vertices_init}

    def agregar_vertice(self, v):
        if v not in self.adyacentes:
            self.adyacentes[v] = {}

    def borrar_vertice(self, v):
        mensaje_error = errores_vertice(self, v)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        if v in self.adyacentes:
            for w in list(self.adyacentes[v].keys()):
                self.borrar_arista(v, w)
            del self.adyacentes[v]

    def agregar_arista(self, v, w, peso=1):
        mensaje_error_v = errores_vertice(self, v)
        mensaje_error_w = errores_vertice(self, w)
        if mensaje_error_v is not None:
            raise ValueError(mensaje_error_v)
        if mensaje_error_w is not None:
            raise ValueError(mensaje_error_w)
        
        self.adyacentes[v][w] = peso
        if not self.dirigido:
            self.adyacentes[w][v] = peso

    def borrar_arista(self, v, w):
        mensaje_error = error_arista(self, v, w)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        if v in self.adyacentes and w in self.adyacentes[v]:
            del self.adyacentes[v][w]
        if not self.dirigido and w in self.adyacentes and v in self.adyacentes[w]:
            del self.adyacentes[w][v]

    def estan_unidos(self, v, w):
        mensaje_error_v = errores_vertice(self, v)
        mensaje_error_w = errores_vertice(self, w)
        if mensaje_error_v is not None:
            raise ValueError(mensaje_error_v)
        if mensaje_error_w is not None:
            raise ValueError(mensaje_error_w)
        
        return v in self.adyacentes and w in self.adyacentes[v]

    def peso_arista(self, v, w):
        mensaje_error = error_arista(self, v, w)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        return self.adyacentes[v][w]

    def obtener_vertices(self):
        return list(self.adyacentes.keys())

    def vertice_aleatorio(self):
        if not self.adyacentes:
            return None
        return random.choice(list(self.adyacentes.keys()))

    def obtener_adyacentes(self, v):
        mensaje_error = errores_vertice(self, v)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        if v in self.adyacentes:
            return list(self.adyacentes[v].keys())
        return []

    def _str_(self):
        resultado = []
        for v, ady in self.adyacentes.items():
            for w, peso in ady.items():
                if self.dirigido or (v <= w):
                    resultado.append(f"{v} <--> {w} (peso: {peso})")
        return "\n".join(resultado)

    def grado_salida(self, v):
        mensaje_error = errores_vertice(self, v)
        if mensaje_error is not None:
            raise ValueError(mensaje_error)
        
        return len(self.adyacentes[v])

