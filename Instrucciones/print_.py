from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class print_(instruccion):
    def __init__(self, expresion, fila, columna):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.expresion = expresion

    def interpretar(self, tree, table):
        #print("LLEGUE AQUI -> "+str(self.expresion))
        if table.getVariable(str(self.expresion)):
            variable = table.getVariable(str(self.expresion))
            tree.updateConsola(str(variable.getValor().valor))
        else:
            value = self.expresion.interpretar(tree, table)
            if isinstance( value, Excepcion): return value
            tree.updateConsola(str(value.valor))

    def getNodo(self):
        nodo = NodoArbol("PRINT")
        nodo.addleaf("(")
        nodo.addNodo(self.expresion.getNodo())
        nodo.addleaf(")")
        return nodo