from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol

class SentenciaTransferencia(instruccion):
    def __init__(self, tipo, fila, columna, instrucciones):
        super().__init__(tipo, fila, columna)
        self.instrucciones = instrucciones

    def interpretar(self, tree, table):
        if self.instrucciones != None:
            return self.instrucciones
        else:
            return self


    def getNodo(self):
        return NodoArbol("Sentencia de \n Transferencia")

    def getTipo(self):
        pass