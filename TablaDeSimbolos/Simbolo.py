
class Simbolo:
    def __init__(self, tipo, identificador, fila, columna, valor = None, esGlobal=None):
        self.tipo = tipo
        self.id = identificador
        self.fila = fila
        self.columna = columna
        self.valor = valor 
        self.esGlobal = esGlobal

    def getIdentificador(self):
        return self.id

    def setIdentificador(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo  

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getFila(self):
        return self.fila
    
    def getColumna(self):
        return self.columna