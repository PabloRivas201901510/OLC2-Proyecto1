from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol

class SentenciaTransferencia(instruccion):
    def __init__(self, tipo, fila, columna, instrucciones):
        super().__init__(tipo, fila, columna)
        self.instrucciones = instrucciones

    def interpretar(self, tree, table):
        if self.instrucciones != None:
            val = self.instrucciones.interpretar(tree, table)
            #self.instrucciones = val
            return val
        else:
            return self


    def getNodo(self):
        nodo =  NodoArbol("Sentencia de \n Transferencia")
        if self.tipo.getTipos() == tipos.BREAK:
            nodo.addleaf("break")
            nodo.addleaf(";")
        elif self.tipo.getTipos() == tipos.CONTINUE:
            nodo.addleaf("continue")
            nodo.addleaf(";")
        elif self.tipo.getTipos() == tipos.RETURN:
            nodo.addleaf("return")
            if self.instrucciones != None:
                nodo.addNodo(self.instrucciones.getNodo())
            nodo.addleaf(";")
        return nodo

    def getTipo(self):
        pass