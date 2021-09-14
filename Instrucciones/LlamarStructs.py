from Expresiones.Primitivo import Primitivo
from Instrucciones.Declaracion import Declaracion
from enum import Enum
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol

class LlamadaStructs(instruccion):
    def __init__(self,  fila, columna, Identificador_Struct, lista_parametros):
        super().__init__(Tipo(tipos.STRUCT), fila, columna)
        self.Identificador_Struct = Identificador_Struct
        self.lista_parametros = lista_parametros
        self.diccionario_struct = {}

    def interpretar(self, tree, table):
        variable_struct = table.getVariable(self.Identificador_Struct).getValor()
        
        if variable_struct:
            if len(variable_struct.getParametros()) != len(self.lista_parametros):
                tree.updateConsola("Error: Semantico, La cantidad de valores ingresados no coinciden con la cantidad de parametros en el struct, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "La cantidad de valores ingresados no coinciden con la cantidad de parametros en el struct", self.fila, self.columna)

            contador = 0
            for i in variable_struct.getParametros():
                i = i.interpretar(tree, table)
                valor = self.lista_parametros[contador].interpretar(tree, table)
                self.diccionario_struct[i.identificador] = valor
                contador +=1

            for j in self.diccionario_struct.items():
                print('STRUCT VAR -> ', j)

            return Primitivo(Tipo(tipos.STRUCT), self.fila, self.columna, self)

            

    def getNodo(self):
        pass

    def getParametros(self):
        return self.lista_parametros

    def getIdentificador(self):
        return self.Identificador

    def changeItem(self, key, value):
        self.diccionario_struct[key] = value
