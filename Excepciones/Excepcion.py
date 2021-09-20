from datetime import datetime

class Excepcion:
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        self.date = None
        self.Time = None
        self.getDate()

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

    def getFecha(self):
        return self.date

    def getHora(self):
        return self.Time

    def getDate(self):
        now = datetime.now()
        self.date = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        self.Time = str(now.hour)+":"+str(now.minute)+":"+str(now.second)