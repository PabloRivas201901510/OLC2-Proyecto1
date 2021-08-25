from Abstract.NodoArbol import NodoArbol
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion

class Primitivo(instruccion):
    def __init__(self, tipo, fila, columna, valor):
        super().__init__(tipo, fila, columna)
        self.valor = valor

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoArbol("PRIMITIVO")
        nodo.addleaf(self.valor)
        return nodo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getTipo(self):
        return self.tipo