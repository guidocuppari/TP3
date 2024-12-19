from collections import deque

class Cola:
    def __init__(self):
        self.datos = deque()

    def encolar(self, elemento):
        self.datos.append(elemento)

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.datos.popleft()

    def ver_primero(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.datos[0]

    def esta_vacia(self):
        return len(self.datos) == 0

    def tamanio(self):
        return len(self.datos)
