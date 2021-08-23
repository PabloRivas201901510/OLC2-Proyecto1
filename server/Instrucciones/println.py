from server.TablaDeSimbolos.Simbolo import Simbolo
from server.Excepciones.Excepcion import Excepcion
from server.TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from server.TablaDeSimbolos.Tipo import Tipo, tipos
from server.Abstract.instruccion import instruccion
from server.Abstract.NodoArbol import NodoArbol


class println(instruccion):
    def __init__(self, expresion, fila, columna):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.expresion = expresion

    def interpretar(self, tree, table):
        #print("LLEGUE AQUI -> "+str(self.expresion))
        if table.getVariable(str(self.expresion)):
            variable = table.getVariable(str(self.expresion))
            tree.updateConsola("\n"+str(variable.getValor().valor))
        else:
            value = self.expresion.interpretar(tree, table)
            if isinstance( value, Excepcion): return value
            tree.updateConsola("\n"+str(value.valor))

    def getNodo(self):
        nodo = NodoArbol("PRINT")
        nodo.addleaf("(")
        nodo.addNodo(self.expresion.getNodo())
        nodo.addleaf(")")
        return nodo