from Expresiones.Primitivo import Primitivo
from Instrucciones.Declaracion import Declaracion
from enum import Enum
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class DeclararArreglos(instruccion):
    def __init__(self, fila, columna, identificador,  posiciones, expresion, tipo_declaracion, declaracion):
        super().__init__(Tipo(tipos.ARREGLO), fila, columna)
        self.expresion = expresion
        self.posiciones = posiciones
        self.identificador =identificador
        self.tipo_declaracion = tipo_declaracion
        self.declaracion = declaracion
        self.valor_retorno = None

    def interpretar(self, tree, table):

        

        #OBTENEMOS LA VARIABLE PARA COMPROBAR SI EXISTE
        variable = table.getVariable(self.identificador)
        
        if variable:
            #OBTENEMOS EL VALOR DE LA VARIABLE
            valor_variable = variable.getValor().interpretar(tree, table)
            if isinstance(valor_variable, Excepcion): 
                tree.updateConsola("Error: Semantico, Error en el ARREGLO, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return valor_variable
            valor_variable = valor_variable.valor
            
            valor_expresion = None
            #OBTENEMOS LA EXPRESION QUE VA A ACTUALIZAR
            if self.expresion != None:
                valor_expresion = self.expresion.interpretar(tree, table)
                if isinstance(valor_expresion, Excepcion): 
                    tree.updateConsola("Error: Semantico, Error en el ARREGLO, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return valor_expresion

            if self.declaracion == Declaracion_Arreglo.MAS:
                #COMIENZA LA BUSQUEDA DEL VALOR SEGUN LAS POSICIONES  
                pos = []
                for i in self.posiciones:
                    posicion = i.interpretar(tree, table)
                    if isinstance(posicion, Excepcion): 
                        tree.updateConsola("Error: Semantico, Error en las posiciones1,  Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return Excepcion("Semantico", "Error en las posiciones", self.fila, self.columna)
                    #print('POSICION DE ENTRADA -> ', posicion.valor)
                    if int(posicion.valor) < 1:
                        tree.updateConsola("Error: Semantico, Error en las posiciones2,  Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return Primitivo(Tipo(tipos.BOOLEANO), self.fila, self.columna, False)
                        
                    pos.append(posicion.valor-1)
                pos.reverse()  
                tmp1 = []
                for j in pos:
                    tmp1.append(j)

                if self.tipo_declaracion == Tipo_Declaracion_Arreglo.ACCEDER:
                    #print('ACCEDI BIEN AQUI---------------------')
                    valor = self.Accesso_Arreglos(tmp1, valor_variable, valor_expresion, tree, table)
                    valor = self.valor_retorno.interpretar(tree, table)
                    #print('TIENE QUE SER PRIMIRIVO -> ', valor)
                    return valor
                    
                valor = self.find_element(tmp1, valor_variable, valor_expresion, tree, table, 0)
                if isinstance(valor, Excepcion):return valor

                if self.tipo_declaracion == Tipo_Declaracion_Arreglo.POP:
                    valor = self.valor_retorno.interpretar(tree, table)
                    self.tipo = valor.tipo
                    return valor
                elif self.tipo_declaracion == Tipo_Declaracion_Arreglo.LENGTH:
                    return Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, self.valor_retorno)  
               
                return
            elif self.declaracion == Declaracion_Arreglo.SIMPLE:
                
                if self.tipo_declaracion == Tipo_Declaracion_Arreglo.PUSH:
                    valor_variable.append(self.expresion)
                elif self.tipo_declaracion == Tipo_Declaracion_Arreglo.POP:
                    return valor_variable.pop(len(valor_variable)-1)
                elif self.tipo_declaracion == Tipo_Declaracion_Arreglo.LENGTH:
                    return Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, len(valor_variable))  

                return



 
    def find_element(self, posiciones, lista, expresion, tree, table, valor_acc):
        #COMPROBAMOS SI LA POSICION NO SOBREPASA LA LISTA
        
        try:
            #CUANDO LA LISTA YA NO TENGA POSICIONES RETORNA
            if self.tipo_declaracion == Tipo_Declaracion_Arreglo.DECLARACION:
                if len(posiciones) == 0:
                    valor_w = self.expresion.interpretar(tree, table)
                    return [valor_w, 1]
            elif self.tipo_declaracion == Tipo_Declaracion_Arreglo.PUSH:
                if len(posiciones) == 0:
                    lista.append(self.expresion)
                    return [lista, 0]
            elif self.tipo_declaracion == Tipo_Declaracion_Arreglo.POP:
                if len(posiciones) == 0:
                    self.valor_retorno = lista.pop(len(lista)-1)
                    return [lista, 0]
            elif self.tipo_declaracion == Tipo_Declaracion_Arreglo.LENGTH:
                if len(posiciones) == 0:
                    self.valor_retorno = len(lista)
                    return [lista, 0]
        except:
            tree.updateConsola("Error: Semantico, La posicion ingresada no existe1, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
            return Excepcion("Semantico", "La posicion ingresada no existe", self.fila, self.columna)


        #OBTENEMOS LA POSICION
        #print(self.tipo_declaracion, ' POSICION_A -> ', posiciones)
        posicion = posiciones.pop()

        #COMPROBAMOS SI LA POSICION NO SOBREPASA LA LISTA
        try:
            
            if posicion >= len(lista):
                tree.updateConsola("Error: Semantico, La posicion ingresada no existe2, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "La posicion ingresada no existe", self.fila, self.columna)
        except:
            #print('ERROR2')
            tree.updateConsola("Error: Semantico, La posicion ingresada no existe3, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
            return Excepcion("Semantico", "La posicion ingresada no existe", self.fila, self.columna)

        #RECORREMOS LA LISTA Y COMPARAMOS
        for index, value in enumerate(lista):
            if isinstance(value, Primitivo): 
                valor_acceso = value.interpretar(tree, table)
            if index == posicion:
                valor_acceso = value.interpretar(tree, table)
                valor = self.find_element( posiciones, valor_acceso.valor , expresion, tree, table, valor_acceso)
                if isinstance(valor, Excepcion):return valor
                if valor[1]:
                    lista.pop(index)
                    lista.insert(index, valor[0])
               
                return [lista, 0]
            
    def Accesso_Arreglos(self, posiciones, lista, expresion, tree, table):
        copia = posiciones.copy()
        valor_copia = copia.pop()
        #RECORREMOS LA LISTA Y COMPARAMOS
        for index, value in enumerate(lista):
            
            #print(index, " == ", valor_copia)
            if index == valor_copia:
                valor_acceso = value.interpretar(tree, table)
                #print('E -> ', posiciones)
                posicion = posiciones.pop()
                #print('s -> ', posiciones)
                #COMPROBAMOS SI LA POSICION NO SOBREPASA LA LISTA

                if self.tipo_declaracion == Tipo_Declaracion_Arreglo.ACCEDER:
                    if len(posiciones) == 0:
                        #print('VALOR ACCESO -> ', str(valor_acceso))
                        self.valor_retorno = valor_acceso
                        return [lista, 0]

                valor = self.Accesso_Arreglos( posiciones, valor_acceso.valor , expresion, tree, table)
                if isinstance(valor, Excepcion):return valor
                if valor[1]:
                    lista.pop(index)
                    lista.insert(index, valor[0])
               
                return [lista, 0]

    def getNodo(self):
        pass

class Tipo_Declaracion_Arreglo(Enum):
    DECLARACION = 1
    PUSH = 2
    POP = 3
    LENGTH = 4
    ACCEDER = 5

class Declaracion_Arreglo(Enum):
    SIMPLE = 1
    MAS = 2