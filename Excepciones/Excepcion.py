
class Excepcion:
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + self.fila + ", " + self.columna + "]"

    def imprimir(self):
        return self.toString()+" \n"

    def getTipo(self):
        return self.tipo

    def getDescripcion(self):
        return self.descripcion

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna