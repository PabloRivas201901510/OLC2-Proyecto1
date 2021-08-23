from server.Abstract.NodoArbol import NodoArbol
from server.TablaDeSimbolos.Simbolo import Simbolo
from server.Excepciones.Excepcion import Excepcion
from server.TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from server.TablaDeSimbolos.Tipo import Tipo, tipos
from server.Abstract.instruccion import instruccion

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