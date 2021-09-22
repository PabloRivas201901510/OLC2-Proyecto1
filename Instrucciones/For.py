from Instrucciones.println import println
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
        super().__init__(Tipo(tipos.NINGUNA), fila, columna)
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
                    elif isinstance(result, SentenciaTransferencia): 
                        if result.tipo.getTipos() == tipos.CONTINUE: break
                        if result.tipo.getTipos() == tipos.BREAK: return
                        if result.tipo.getTipos() == tipos.RETURN: return result
                       


        elif(self.caso2): #for letra in “Hola Mundo!” o for animal in [“perro”, “gato”, “tortuga”]
            if self.valor1:
                cadena = self.valor1.interpretar(tree, table)
                if isinstance(cadena, Excepcion): 
                    tree.updateConsola("Error: Semantico, loop for Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return cadena

                valor_for = cadena.valor
                if (cadena.tipo.getTipos() == tipos.ARREGLO ):
                    #tree.updateConsola("Error: Semantico, El valor no es de tipo ARREGLO. Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    #return Excepcion("Semantico", "El valor no es de tipo ARREGLO", self.fila, self.columna)   


                    tabla = TablaSimbolos(table)
                    tabla.setEntorno("Loop For")
                    tree.setTablaSimbolos(tabla)
                    tabla.setVariable(Simbolo(Tipo(tipos.NINGUNA), self.interador, self.fila, self.columna, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0)))

                    contador = 0
                    while contador < len(valor_for): #ES UN CARACTER?
                        if isinstance(valor_for[contador], Primitivo):
                            it = Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(valor_for[contador].tipo.getTipos()), self.fila, self.columna, valor_for[contador].valor ))
                            it.interpretar(tree, tabla)
                        else:
                            try:
                                valor_for[contador] = valor_for[contador].interpretar(tree, tabla)
                            except:
                                pass
                            #print('ESTOY METIENDO EN EL FOR ESTO -> ', valor_for[contador])
                            it = Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, valor_for[contador] )
                            it.interpretar(tree, tabla)
                        
                            
                        for i in self.listaInstrucciones:
                            if isinstance(i, Excepcion): 
                                tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                                return Excepcion("Semantico", "Error en el ciclo FOR", self.linea, self.columna)
                            result = i.interpretar(tree, tabla)
                            if isinstance(result, Excepcion): 
                                tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                                return Excepcion("Semantico", "Error en el ciclo FOR", self.fila, self.columna)

                            elif isinstance(result, SentenciaTransferencia): 
                                if result.tipo.getTipos() == tipos.CONTINUE: break
                                if result.tipo.getTipos() == tipos.BREAK: return
                                if result.tipo.getTipos() == tipos.RETURN: return result
                        contador += 1

                elif (cadena.tipo.getTipos() == tipos.CADENA ):
                    #print('ENTRE A CADENAAAA')
                    tabla = TablaSimbolos(table)
                    tabla.setEntorno("Loop For")
                    tree.setTablaSimbolos(tabla)
                    tabla.setVariable(Simbolo(Tipo(tipos.NINGUNA), self.interador, self.fila, self.columna, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0)))
                    #Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(tipos.ENTERO), self.fila, self.columna, 0))
                    #print('FOR ==> ', cadena.tipo.getTipos(), ' ----> ', len(valor_for))
                    #self.tipo = cadena.tipo.getTipos()
         
                    for j in (valor_for): #ES UN CARACTER?
                        it = Declaracion(Tipo(tipos.NINGUNA), self.fila, self.columna, self.interador, Primitivo(Tipo(tipos.CADENA), self.fila, self.columna, j ))
                        it.interpretar(tree, tabla)
                        
 
                        for i in self.listaInstrucciones:
                            if isinstance(i, Excepcion): 
                                tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                                return Excepcion("Semantico", "Error en el ciclo FOR", self.linea, self.columna)
                            result = i.interpretar(tree, tabla)
                            if isinstance(result, Excepcion): 
                                tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                                return Excepcion("Semantico", "Error en el ciclo FOR", self.fila, self.columna)

                            elif isinstance(result, SentenciaTransferencia): 
                                if result.tipo.getTipos() == tipos.CONTINUE: break
                                if result.tipo.getTipos() == tipos.BREAK: return
                                if result.tipo.getTipos() == tipos.RETURN: return result
                     
                                
             

            elif self.valor2:
                '''arreglo = self.valor2.interpretar(tree, table)    
                if isinstance(arreglo, Excepcion): 
                    tree.updateConsola("Error: Semantico, loop for Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return arreglo
                if (arreglo.tipo.getTipos() != tipos.CADENA):
                    tree.updateConsola("Error: Semantico, El valor no es de tipo string. Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "El valor no es de tipo string", self.fila, self.columna)'''   
                

        elif(self.caso3): #for numero in arr[2:4]
            pass

    def getNodo(self):
        nodo = NodoArbol("LOOP FOR")
        nodo.addleaf("for")
        n = NodoArbol("IDENTIFICADOR")
        n.addleaf(str(self.interador))
        nodo.addNodo(n)

        if self.caso1:
            nodo.addNodo(self.valor1.getNodo())
            nodo.addleaf(":")
            nodo.addNodo(self.valor2.getNodo())
        else:
            nodo.addNodo(self.valor1.getNodo())

        nodo1 = NodoArbol("INSTRUCCIONES")
        nodo.addNodo(nodo1)
        contador = 0
        contador_nodos = len(self.listaInstrucciones)
        for k in self.listaInstrucciones:
            if len(self.listaInstrucciones) == 1:
                nodo3 = NodoArbol("INSTRUCCION")
                nodo3.addNodo(k.getNodo())
                nodo1.addNodo(nodo3)
            else:
                if contador != len(self.listaInstrucciones) -1 :
                    nodo2 = NodoArbol("INSTRUCCIONES")
                    nodo1.addNodo(nodo2)
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(self.listaInstrucciones[contador_nodos-1].getNodo()) 
                    nodo1.addNodo(nodo3)
                    nodo1 = nodo2
                else:
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(self.listaInstrucciones[contador_nodos-1].getNodo()) 
                    nodo1.addNodo(nodo3)

                contador +=1
                contador_nodos -=1

        nodo.addleaf("END")
        nodo.addleaf(";")
        return nodo


    
            
            
