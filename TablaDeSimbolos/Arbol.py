from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from Abstract.instruccion import instruccion


class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.consola = ""
        self.Global = TablaSimbolos()
        self.errores:Excepcion = []
        self.TablaSimbolos = []

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instruccion):
        self.instrucciones = instruccion

    def getConsola(self):
        return self.consola

    def updateConsola(self,cadena):
        self.consola += str(cadena)

    def getGlobal(self):
        return self.Global

    def setGlobal(self, Global):
        self.Global = Global

    def setTablaSimbolos(self, table):
        self.TablaSimbolos.append(table)

    def getTablaSimbolos(self):
        return self.TablaSimbolos

    