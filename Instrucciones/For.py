from Expresiones.Primitivo import Primitivo
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.Declaracion import Declaracion
from Instrucciones.SentenciaTransferencia import SentenciaTransferencia

class For(instruccion):
    def __init__(self,  fila, columna, iterador, valor1, valor2, caso1, caso2, caso3, listaInstrucciones):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.interador = iterador
        self.valor1 = valor1
        self.valor2 = valor2
        self.caso1 = caso1
        self.caso2 = caso2
        self.caso3 = caso3
        self.listaInstrucciones = listaInstrucciones

    def interpretar(self, tree, table):
        if(self.caso1): #for i in 1:4
            #------VALOR INICIAL
            value_start = self.valor1.interpretar(tree, table)
            if isinstance(value_start, Excepcion): 
                    tree.updateConsola("Error: Semantico, loop for Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return value_start
            if (value_start.tipo.getTipos() != tipos.ENTERO):
                tree.updateConsola("Error: Semantico, El valor de inicio no es un entero Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "El valor de inicio no es un entero", self.fila, self.columna)
            #-------VALOR FINAL
            value_end = self.valor2.interpretar(tree, table)
            if isinstance(value_end, Excepcion): 
                    tree.updateConsola("Error: Semantico, loop for Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return value_end
            if (value_end.tipo.getTipos() != tipos.ENTERO):
                tree.updateConsola("Error: Semantico, El valor final no es un entero Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "El valor final no es un entero", self.fila, self.columna)

            rango = range(value_start.valor, value_end.valor+1)
            tabla = TablaSimbolos(table)
            tabla.setEntorno("Loop For")
            tree.setTablaSimbolos(tabla)
            tabla.setVariable(Simbolo(Tipo(tipos.NINGUNA), self.interador, self.fila, self.columna, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0)))
            #Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0))
            for j in rango:
                it = Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, j ))
                it.interpretar(tree, tabla)
                for i in self.listaInstrucciones:
                    if isinstance(i, Excepcion): 
                        tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return Excepcion("Semantico", "Error en el ciclo FOR", self.linea, self.columna)
                    result = i.interpretar(tree, tabla)
                    if isinstance(result, Excepcion): 
                        tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return Excepcion("Semantico", "Error en el ciclo FOR", self.fila, self.columna)
                    elif isinstance(result, SentenciaTransferencia): return result


        elif(self.caso2): #for letra in “Hola Mundo!” o for animal in [“perro”, “gato”, “tortuga”]
            if self.valor1:
                cadena = self.valor1.interpretar(tree, table)    
                if isinstance(cadena, Excepcion): 
                    tree.updateConsola("Error: Semantico, loop for Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return cadena
                if (cadena.tipo.getTipos() != tipos.CADENA):
                    tree.updateConsola("Error: Semantico, El valor no es de tipo string. Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "El valor no es de tipo string", self.fila, self.columna)   

                tabla = TablaSimbolos(table)
                tabla.setEntorno("Loop For")
                tree.setTablaSimbolos(tabla)
                tabla.setVariable(Simbolo(Tipo(tipos.NINGUNA), self.interador, self.fila, self.columna, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0)))
                #Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0))
                for j in cadena.valor: #ES UN CARACTER?
                    print(str(j))
                    it = Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(tipos.CADENA), self.fila, self.columna, j ))
                    it.interpretar(tree, tabla)
                    for i in self.listaInstrucciones:
                        print(i)
                        if isinstance(i, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return Excepcion("Semantico", "Error en el ciclo FOR", self.linea, self.columna)
                        result = i.interpretar(tree, tabla)
                        if isinstance(result, Excepcion): 
                            tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return Excepcion("Semantico", "Error en el ciclo FOR", self.fila, self.columna)
                        elif isinstance(result, SentenciaTransferencia): return result
                

        elif(self.caso3): #for numero in arr[2:4]
            pass

    def getNodo(self):
        pass