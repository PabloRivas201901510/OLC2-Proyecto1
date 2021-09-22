from Abstract.NodoArbol import NodoArbol
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Expresiones.Primitivo import Primitivo


class Variable(instruccion):
    def __init__(self,  fila, columna, identificador):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.identificador = identificador

    def interpretar(self, tree, table):
        variable = table.getVariable(self.identificador)
        if variable:
            self.tipo = variable.getTipo()
            return variable.getValor()
        else:
            return Excepcion("Semántico", "La variable "+str(self.identificador)+" no existe", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoArbol("IDENTIFICADOR")
        nodo.addleaf(self.identificador)
        return nodo