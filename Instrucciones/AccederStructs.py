from Expresiones.Primitivo import Primitivo
from Instrucciones.Declaracion import Declaracion
from enum import Enum
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol

class AccesoStructs(instruccion):
    def __init__(self,  fila, columna, Identificador_Struct, lista_identificadores , expresion, tipo_acceso_struct):
        super().__init__(Tipo(tipos.STRUCT), fila, columna)
        self.lista_identificadores = lista_identificadores
        self.Identificador_Struct = Identificador_Struct
        self.expresion = expresion
        self.tipo_acceso_struct = tipo_acceso_struct

    def interpretar(self, tree, table):
        if self.tipo_acceso_struct == Tipo_Acesso_Struct.ACCESO:
            parametro_struct = self.lista_identificadores.pop(len(self.lista_identificadores)-1)
            for i in self.lista_identificadores:
                variable_tmp = table.getVariable(i)
                if variable_tmp:
                    pass

        elif self.tipo_acceso_struct == Tipo_Acesso_Struct.ASIGNAR:
            pass

            

    def getNodo(self):
        pass

class Tipo_Acesso_Struct(Enum):
    ACCESO = 1
    ASIGNAR = 2