from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class Declaracion(instruccion):
    def __init__(self, tipo, fila, columna, identificador, expresion):
        super().__init__(tipo, fila, columna)
        self.identificador = identificador
        self.expresion = expresion

    def interpretar(self, tree, table):
        id = self.identificador
        expresion = self.expresion
        

    def getNodo(self):
        pass