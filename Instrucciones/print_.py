from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from Expresiones.Variable import Variable

class print_(instruccion):
    def __init__(self, expresion, fila, columna):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.expresion = expresion

    def interpretar(self, tree, table):
        lista_expresiones = ""
        for i in self.expresion:
            if isinstance(i , Variable): i = i.interpretar(tree, table)
            if isinstance( i, Excepcion): return i
            if table.getVariable(i):
                variable = table.getVariable(str(i))
                lista_expresiones += str(variable.getValor().valor)
                #tree.updateConsola(str(variable.getValor().valor)+"\n")
            else:
                value = i.interpretar(tree, table)
                if isinstance( value, Excepcion): return value
                lista_expresiones += str(value.valor)
                #tree.updateConsola(str(value.valor)+"\n")
        tree.updateConsola(str(lista_expresiones))

    def getNodo(self):
        nodo = NodoArbol("PRINT")
        nodo.addleaf("(")
        nodo.addNodo(self.expresion.getNodo())
        nodo.addleaf(")")
        return nodo