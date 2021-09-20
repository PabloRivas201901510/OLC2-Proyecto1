from Instrucciones.SentenciaTransferencia import SentenciaTransferencia
from Instrucciones.println import println
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
    def __init__(self,  fila, columna, lista_identificadores , expresion, tipo_acceso_struct):
        super().__init__(Tipo(tipos.STRUCT), fila, columna)
        self.lista_identificadores = lista_identificadores
        self.expresion = expresion
        self.tipo_acceso_struct = tipo_acceso_struct

    def interpretar(self, tree, table):
            
            
            aux = self.lista_identificadores.copy()
            variable_struct = aux.pop(0)
            variable_principal = table.getVariable(variable_struct.identificador)
            if variable_principal:
                valor_variable = variable_principal.getValor()
                
                if self.tipo_acceso_struct == Tipo_Acesso_Struct.ACCESO:
                    #CUANDO LOS DOS DEMAS PARAMETROS SON STRUCTS
                    #i.identificador
                    for i in aux:
                        i = i.interpretar(tree, table)
                        if isinstance(i, Excepcion):return i
                        verificar = False

                        for key, value in valor_variable.valor.items():
                            #print(key, " == ", i.identificador)
                            if key == i.identificador:
                                valor_variable = value
                                verificar = True
                                break

                    if verificar:
                        print("\n")
                        return valor_variable
                    else:
                        tree.updateConsola("Error: Semantico, La variable "+str(i.identificador)+ " no existe, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return Excepcion("Semantico", "La variable "+str(i.identificador)+ " no existe", self.fila, self.columna)
                   
                    #print('DIC ACTUAL ret -> ',valor_variable)
                    
                    

                elif self.tipo_acceso_struct == Tipo_Acesso_Struct.ASIGNAR:
                    
                    for i in aux:
                        i = i.interpretar(tree, table)
                        if isinstance(i, Excepcion):return i
                        verificar = None
                        for key, value in valor_variable.valor.items():
                            if key == i.identificador:
                                Data = valor_variable
                                valor_variable = value
                                key_id = i.identificador
                                verificar = True

                        if verificar:
                            pass
                        else:
                            tree.updateConsola("Error: Semantico, La variable "+str(i.identificador)+ " no existe, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return Excepcion("Semantico", "La variable "+str(i.identificador)+ " no existe", self.fila, self.columna)
                    
                    expresion = self.expresion
                   #print('2 EXPRESION ACTUAL -> ', expresion)    
                    Data.valor[key_id]= expresion.interpretar(tree, table)
                    return 
                    
            else:
                tree.updateConsola("Error: Semantico, La variable no existe, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "La variable no existe", self.fila, self.columna)

            return Primitivo(Tipo(tipos.ENTERO), 0, 0, 0)
    

        

            

    def getNodo(self):
        pass

class Tipo_Acesso_Struct(Enum):
    ACCESO = 1
    ASIGNAR = 2