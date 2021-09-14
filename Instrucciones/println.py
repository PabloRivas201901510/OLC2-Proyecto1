from Expresiones.Primitivo import Primitivo
from Expresiones.Variable import Variable
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from enum import Enum

class println(instruccion):
    def __init__(self, expresion, fila, columna, tipo_print):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.expresion = expresion
        self.tipo_print = tipo_print

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
                print('1VALOR IMPRIMIR -> ', i)
                value = i.interpretar(tree, table)
                if isinstance( value, Excepcion): return value
                print('2VALOR IMPRIMIR -> ', value)
                if value.tipo.getTipos() == tipos.ARREGLO:
                    value = self.Desgloce_Arreglos(value.valor, tree, table)
                else:
                    print('3VALOR IMPRIMIR -> ', value.tipo.getTipos())
                    value = value.valor
                lista_expresiones += str(value)
                
        tree.updateConsola(str(lista_expresiones))
        if Tipo_Print.SALTO == self.tipo_print:
            tree.updateConsola("\n")

    def getNodo(self):
        nodo = NodoArbol("PRINT")
        nodo.addleaf("(")
        nodo.addNodo(self.expresion.getNodo())
        nodo.addleaf(")")
        return nodo


    def Desgloce_Arreglos(self, vector, tree, table):
        #import pdb
        #pdb.set_trace()
        print('LLEGA-> ', vector )
        res = "["
        for i in vector:
            if(i == "[" or i == "]"):
                res += i
                continue
            tmp = i.interpretar(tree, table)
            if isinstance(tmp, Excepcion):
                tree.updateConsola("error "+"\n")
                return
            if tmp.tipo.getTipos() == tipos.ARREGLO:
                res += self.Desgloce_Arreglos( tmp.valor, tree, table) + ","
            else:
                res += str(tmp.valor)
                res += ","
        res = res[:-1]
        res += "]"
        return str(res)

class Tipo_Print(Enum):
    SALTO = 1
    LINEA = 2
        




    