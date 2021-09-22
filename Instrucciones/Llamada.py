from Instrucciones.Declaracion import Declaracion
from Expresiones.Primitivo import Primitivo
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.SentenciaTransferencia import SentenciaTransferencia

class Llamada(instruccion):
    def __init__(self, fila, columna, identificador, lista_parametros):
        super().__init__(Tipo(tipos.ARREGLO), fila, columna)
        self.identificador = identificador 
        self.lista_parametros = lista_parametros

    def interpretar(self, tree, table):
        
        variable_function = table.getVariable(self.identificador+ "_funtion")
        if variable_function:
            Datos_Function = variable_function.getValor()

            #print('PARAMETROS -> ',Datos_Function.getParametros())

            if len(self.lista_parametros) != len(Datos_Function.getParametros()):
                tree.updateConsola("Error: Semantico, La cantidad de parametros no coinciden, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "Error La cantidad de parametros no coinciden", self.fila, self.columna)

            tabla = TablaSimbolos(table)
            tabla.setEntorno("function "+str(self.identificador))
            tree.setTablaSimbolos(tabla)

            #-----------LLENAMOS LOS PARAMETROS CON LAS EXPRESIONES DE ENTRADA -------
            if Datos_Function.getParametros():
                contador = 0
                for i in Datos_Function.getParametros():
                    i = i.interpretar(tree, table)
                    result = self.lista_parametros[contador].interpretar(tree, table)
                    tabla.setVariable(Simbolo(Tipo(tipos.NINGUNA), i.identificador , self.fila, self.columna, result))  
                    contador+=1

            for i in Datos_Function.getInstrucciones():
                #print('1INSTRUCCION -> ', i , ' ><<<<')
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, Error en la Llamada, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en la Llamada", self.fila, self.columna)
                

                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, Error en la Llamada, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en la Llamada", self.fila, self.columna)
                #print('2INSTRUCCION -> ', result)
                if isinstance(i, SentenciaTransferencia):
                    #print('SOY UNA TRANSFERENCIA ---')
                    if i.tipo.getTipos() == tipos.BREAK: return
                    elif i.tipo.getTipos() == tipos.CONTINUE: break
                    elif i.tipo.getTipos() == tipos.RETURN: 
                        return result.interpretar(tree, tabla)

                if isinstance(result, SentenciaTransferencia):
                    #print('SOY UNA TRANSFERENCIA ---')
                    if result.tipo.getTipos() == tipos.BREAK: return
                    elif result.tipo.getTipos() == tipos.CONTINUE: break
                    elif result.tipo.getTipos() == tipos.RETURN:  
                        result = result.interpretar(tree, tabla)
                        #print('LLAMADA REGRESA -> ', result)
                        return result

            #self.interpretar(tree, table) 
        else:
            variable_struct = table.getVariable(self.identificador+ "_Structs")
            if variable_struct:
                Primitivo_Struct = variable_struct.getValor()
                Datos_Struct = Primitivo_Struct.interpretar(tree, table).valor
                
                if len(Datos_Struct.getParametros()) != len(self.lista_parametros):
                    tree.updateConsola("Error: Semantico, La cantidad de valores ingresados no coinciden con la cantidad de parametros en el struct, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "La cantidad de valores ingresados no coinciden con la cantidad de parametros en el struct", self.fila, self.columna)

       

                contador = 0
                for i in Datos_Struct.getParametros():
                    i = i.interpretar(tree, table)
                    valor = self.lista_parametros[contador].interpretar(tree, table)
                    Datos_Struct.changeItem(i.identificador,  valor)
                    contador +=1
                


                return Primitivo(Tipo(tipos.STRUCT), self.fila, self.columna, Datos_Struct.diccionario_struct)

            else:
                tree.updateConsola("Error: Semantico, Error en la Llamada, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "Error en la Llamada", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoArbol("LLAMADA")
        nn1 = NodoArbol("IDENTIFICADOR")
        nn1.addleaf(self.identificador)
        nodo.addNodo(nn1)
        nodo.addleaf("(")

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
                    n1.addleaf(",")
                    n1.addNodo(self.lista_parametros[contador1_ns-1].getNodo()) 
                    n1 = n2
                else:
                    n1.addNodo(self.lista_parametros[contador1_ns-1].getNodo()) 

                contador1 +=1
                contador1_ns -=1


        nodo.addleaf(")")
        nodo.addleaf(";")
        return nodo
        