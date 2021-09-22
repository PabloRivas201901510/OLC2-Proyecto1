from TablaDeSimbolos.Arbol import Arbol
from Expresiones.Primitivo import Primitivo
from Instrucciones.Declaracion import Declaracion
from enum import Enum
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol

class DeclararStructs(instruccion):
    def __init__(self,  fila, columna, Identificador, lista_parametros, tipo_struct):
        super().__init__(Tipo(tipos.STRUCT), fila, columna)
        self.Identificador = Identificador+"_Structs"
        self.lista_parametros = lista_parametros
        self.tipo_struct = tipo_struct
        self.diccionario_struct = {}

    def interpretar(self, tree, table):
        table.setVariable(Simbolo(Tipo(tipos.STRUCT), self.Identificador, self.fila, self.columna, Primitivo(Tipo(tipos.STRUCT), self.fila, self.columna, self) ))
        
    def getNodo(self):
        nodo = NodoArbol("DECLARACION \n STRUCT")
        nodo.addleaf(self.Identificador)

        n1 = NodoArbol("PARAMETROS")
        nodo.addNodo(n1)
        contador1 = 0
        contador1_ns = len(self.lista_parametros)
        for k in self.lista_parametros:
            if len(self.lista_parametros) == 1:
                n1.addNodo(k.getNodo())
            else:
                if contador1 != len(self.lista_parametros) -1 :
                    n2 = NodoArbol("PARAMETROS")
                    n1.addNodo(n2)
                    n1.addNodo(self.lista_parametros[contador1_ns-1].getNodo()) 
                    n1 = n2
                else:
                    n1.addNodo(self.lista_parametros[contador1_ns-1].getNodo()) 

                contador1 +=1
                contador1_ns -=1

        nodo.addleaf("END")
        nodo.addleaf(";")
        return nodo

    def getParametros(self):
        return self.lista_parametros

    def getIdentificador(self):
        return self.Identificador

    def changeItem(self, key, value):
        self.diccionario_struct[key] = value

    def find_Key(self, Key):
        for i, j in self.diccionario_struct.items():
            if i == Key:
                return j
        return False

    

  

class Tipo_Struct(Enum):
    MUTABLE = 1
    INMUTABLE = 2