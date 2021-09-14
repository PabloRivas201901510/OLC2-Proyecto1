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
        self.Identificador = Identificador
        self.lista_parametros = lista_parametros
        self.tipo_struct = tipo_struct

    def interpretar(self, tree, table):
        table.setVariable(Simbolo(Tipo(tipos.STRUCT), self.Identificador, self.fila, self.columna, self))

    def getNodo(self):
        pass

    def getParametros(self):
        return self.lista_parametros

    def getIdentificador(self):
        return self.Identificador

class Tipo_Struct(Enum):
    MUTABLE = 1
    INMUTABLE = 2