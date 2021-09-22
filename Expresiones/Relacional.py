from Expresiones.Logica import tipos_logicos
from Abstract.NodoArbol import NodoArbol
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Expresiones.Primitivo import Primitivo
from enum import Enum

class Relacional(instruccion):
    def __init__(self, fila, columna, izquierda, derecha, operador):
        super().__init__(Tipo(tipos.BOOLEANO), fila, columna)
        self.izquierda = izquierda
        self.derecha = derecha
        self.operador = operador

    def interpretar(self, tree, table):
        izquierdo = None
        derecho = None

        izquierdo = self.izquierda.interpretar(tree, table)
        if isinstance(izquierdo, Excepcion): return izquierdo
        derecho = self.derecha.interpretar(tree, table)
        if isinstance(derecho, Excepcion): return derecho
        #print("---> ", self.operador)
        #print("---> ", izquierdo.valor, " -- ", derecho.valor, " == ", izquierdo.valor == derecho.valor)
       



        #---------MENOR QUE -------
        if self.operador == tipos_relacional.MENORQUE:
            #print( " --- < ", izquierdo.valor < derecho.valor , "\n")
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor < derecho.valor)
        #---------MAYOR QUE -------
        elif self.operador == tipos_relacional.MAYORQUE:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor > derecho.valor)
        #---------MENOR IGUAL QUE -------
        elif self.operador == tipos_relacional.MENORIGUAL:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor <= derecho.valor)
        #---------MAYOR IGUAL QUE -------
        elif self.operador == tipos_relacional.MAYORIGUAL:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor >= derecho.valor)
        #---------IGUAL QUE -------
        elif self.operador == tipos_relacional.IGUALACION:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor == derecho.valor)
        #---------DIFERENTE -------
        elif self.operador == tipos_relacional.DIFERENCIACION:
            return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, izquierdo.valor != derecho.valor)
        else:
            tree.updateConsola("Error: Semantico, Operandos invalidos para RELACIONALES:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
            return Excepcion("sintactico", "Operandos invalidos para RELACIONALES", self.fila, self.columna) 



    def getNodo(self):
        nodo = NodoArbol("EXPRESIONES \n RELACIONALES")
        nodo.addNodo(self.izquierda.getNodo())

        nodo1 = NodoArbol("OPERADOR \n RELACIONAL")
        if self.operador == tipos_relacional.MAYORQUE:
            nodo1.addleaf(">")
        elif self.operador == tipos_relacional.MENORQUE:
            nodo1.addleaf("<")
        elif self.operador == tipos_relacional.MAYORIGUAL:
            nodo1.addleaf(">=")
        elif self.operador == tipos_relacional.MENORIGUAL:
            nodo1.addleaf("<=")
        elif self.operador == tipos_relacional.IGUALACION:
            nodo1.addleaf("==")
        elif self.operador == tipos_relacional.DIFERENCIACION:
            nodo1.addleaf("!=")
        nodo.addNodo(nodo1)
        nodo.addNodo(self.derecha.getNodo())
        return nodo


class tipos_relacional(Enum):
    MAYORQUE = 1
    MENORQUE = 2
    MAYORIGUAL = 3
    MENORIGUAL = 4
    IGUALACION = 5
    DIFERENCIACION = 6