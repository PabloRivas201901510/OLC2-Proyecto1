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
        self.identificador = identificador + "_funtion"
        self.lista_parametros = lista_parametros

    def interpretar(self, tree, table):
        
        variable_function = table.getVariable(self.identificador)
        if variable_function:
            Datos_Function = variable_function.getValor()

            #print('PARAMETROS -> ',Datos_Function.getParametros())

            if len(self.lista_parametros) != len(Datos_Function.getParametros()):
                tree.updateConsola("Error: Semantico, La cantidad de parametros no coinciden, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "Error La cantidad de parametros no coinciden", self.fila, self.columna)

            tabla = TablaSimbolos(table)
            tabla.setEntorno("FUNCTION")
            tree.setTablaSimbolos(tabla)

            #-----------LLENAMOS LOS PARAMETROS CON LAS EXPRESIONES DE ENTRADA -------
            contador = 0
            for i in Datos_Function.getParametros():
                result = self.lista_parametros[contador].interpretar(tree, table)
                tabla.setVariable(Simbolo(Tipo(tipos.NINGUNA), i.identificador , self.fila, self.columna, result))  
                contador+=1

            for i in Datos_Function.getInstrucciones():
                #print('1INSTRUCCION -> ', i , ' ><<<<')
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en el ciclo WHILE", self.fila, self.columna)
                

                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en el ciclo WHILE", self.fila, self.columna)
                #print('2INSTRUCCION -> ', result)
                if isinstance(i, SentenciaTransferencia):
                    #print('SOY UNA TRANSFERENCIA ---')
                    if i.tipo.getTipos() == tipos.BREAK: return
                    elif i.tipo.getTipos() == tipos.CONTINUE: break
                    elif i.tipo.getTipos() == tipos.RETURN:  
                        result = i.interpretar(tree, tabla).interpretar(tree, tabla)
                        #print('LLAMADA REGRESA -> ', result)
                        return result
                if isinstance(result, SentenciaTransferencia):
                    #print('SOY UNA TRANSFERENCIA ---')
                    if result.tipo.getTipos() == tipos.BREAK: return
                    elif result.tipo.getTipos() == tipos.CONTINUE: break
                    elif result.tipo.getTipos() == tipos.RETURN:  
                        result = result.interpretar(tree, tabla).interpretar(tree, tabla)
                        #print('LLAMADA REGRESA -> ', result)
                        return result

        else:
            tree.updateConsola("Error: Semantico, La funncion no existe, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
            return Excepcion("Semantico", "Error la funncion no existe", self.fila, self.columna)

    def getNodo(self):
        pass