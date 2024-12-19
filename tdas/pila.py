class PilaDinamica:
    _FACTOR1 = 2
    _FACTOR2 = 4

    def __init__(self):
        self._datos = [None]
        self._cantidad = 0

    def esta_vacia(self):
        return self._cantidad == 0

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self._datos[self._cantidad - 1]

    def apilar(self, valor):
        if self._cantidad == len(self._datos):
            self._redimensionar(len(self._datos) * self._FACTOR1)
        self._datos[self._cantidad] = valor
        self._cantidad += 1

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        valor = self._datos[self._cantidad - 1]
        self._cantidad -= 1

        if self._cantidad > 0 and self._cantidad * self._FACTOR2 <= len(self._datos):
            self._redimensionar(len(self._datos) // self._FACTOR1)
        return valor

    def _redimensionar(self, nuevo_tam):
        nuevo_datos = [None] * nuevo_tam
        for i in range(self._cantidad):
            nuevo_datos[i] = self._datos[i]
        self._datos = nuevo_datos
