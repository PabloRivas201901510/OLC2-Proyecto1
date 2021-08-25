from Abstract.NodoArbol import NodoArbol
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Expresiones.Primitivo import Primitivo
from enum import Enum

class Logica(instruccion):
    def __init__(self, fila, columna, izquierda, derecha, operador):
        super().__init__(Tipo(tipos.BOOLEANO), fila, columna)
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha

    def interpretar(self, tree, table):
        izquierdo = None
        derecho = None

        if self.derecha != None:
            izquierdo = self.izquierda.interpretar(tree, table)
            if isinstance(izquierdo, Excepcion): return izquierdo
            derecho = self.derecha.interpretar(tree, table)
            if isinstance(derecho, Excepcion): return derecho
        else:
            izquierdo = self.izquierda.interpretar(tree, table)
            if isinstance(izquierdo, Excepcion): return izquierdo


        #----------- LOGICAS --------------
        #---------- OR -----------
        if self.operador == tipos_logicos.OR:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor or derecho.valor)
        #---------- AND -----------
        elif self.operador == tipos_logicos.AND:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor and derecho.valor)
        #---------- NOT -----------
        elif self.operador == tipos_logicos.NOT:
            print(not izquierdo.valor)
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, (not izquierdo.valor))   
        else:
                return Excepcion("sintactico", "Operandos invalidos para LOGICOS", self.fila, self.columna) 

        
    def getNodo(self):
        pass


class tipos_logicos(Enum):
    OR = 1
    AND = 2
    NOT = 3