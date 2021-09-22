from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.SentenciaTransferencia import SentenciaTransferencia

class Parametros(instruccion):
    def __init__(self, tipo, fila, columna, identificador):
        super().__init__(tipo, fila, columna)
        self.identificador = identificador

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoArbol("PARAMETRO")
        nodo.addleaf(self.identificador)
        return nodo

    