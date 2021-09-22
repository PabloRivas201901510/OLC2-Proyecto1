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
                value = i.interpretar(tree, table)
                if isinstance( value, Excepcion): return value
                if value.tipo.getTipos() == tipos.ARREGLO:
                    value = self.Desgloce_Arreglos(value.valor, tree, table)
                else:
                    value = value.interpretar(tree, table)
                    value = value.valor
                lista_expresiones += str(value)
                
        tree.updateConsola(str(lista_expresiones))
        if Tipo_Print.SALTO == self.tipo_print:
            tree.updateConsola("\n")

    def getNodo(self):
        if self.tipo == Tipo_Print.LINEA:
            n = "PRINT"
        else:
            n = "PRINTLN"
        nodo = NodoArbol(n)
        nodo.addleaf("(")
        nodo1 = NodoArbol("EXPRESIONES")
        nodo.addNodo(nodo1)
        contador = 0
        contador_nodos = len(self.expresion)
        for i in self.expresion:
            if len(self.expresion) == 1:
                nodo3 = NodoArbol("EXPRESION")
                nodo3.addNodo(i.getNodo()) 
                nodo1.addNodo(nodo3)
            else:
                if contador != len(self.expresion) -1 :
                    nodo2 = NodoArbol("EXPRESIONES")
                    nodo1.addNodo(nodo2)
                    nodo1.addleaf(',')
                    nodo3 = NodoArbol("EXPRESION")
                    nodo3.addNodo(self.expresion[contador_nodos-1].getNodo()) 
                    nodo1.addNodo(nodo3)
                    
                    nodo1 = nodo2
                else:
                    nodo3 = NodoArbol("EXPRESION")
                    nodo3.addNodo(self.expresion[contador_nodos-1].getNodo()) 
                    nodo1.addNodo(nodo3)

                contador +=1
                contador_nodos -=1
        
        nodo.addleaf(")")
        return nodo




    def Desgloce_Arreglos(self, vector, tree, table):
        res = "["
        for i in vector:
            if(i == "[" or i == "]"):
                res += i
                continue
            tmp = i.interpretar(tree, table)
            if isinstance(tmp, Excepcion):
                tree.updateConsola("El arreglo tiene un error en sus parametros"+"\n")
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
        




    