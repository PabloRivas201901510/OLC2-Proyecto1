from Instrucciones.SentenciaTransferencia import SentenciaTransferencia
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class Condicional(instruccion):
    def __init__(self, fila, columna, sentenicaIF, sentenciaElse):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.sentenciaIf = sentenicaIF
        self.sentenciaElse = sentenciaElse

    def interpretar(self, tree, table):
        if self.sentenciaElse == None:
            for i in self.sentenciaIf:
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, Error en la sentencia Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en la sentencia IF", self.fila, self.columna)
                value = i.condicion.interpretar(tree, table)
                if isinstance(value, Excepcion): 
                    tree.updateConsola("Error: Semantico, Se esperaba un valor booleano para la condicion Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.fila, self.columna)

                if value.valor:
                    tabla = TablaSimbolos(table)
                    tabla.setEntorno("Sentencia If")
                    tree.setTablaSimbolos(tabla)
                    for j in i.listaInstruccionesIF:
                        if isinstance(j, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return j

                        if isinstance(j, SentenciaTransferencia):
                            #print('TRANSFERENCIA -> ', result)
                            if j != None:
                                return j

                        result = j.interpretar(tree, tabla)
                        if isinstance(result, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return result

                        
                    return
        else:
            #--------------- IF ----------------------
            for i in self.sentenciaIf:
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, Error en la sentencia Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en la sentencia IF", self.fila, self.columna)
                value = i.condicion.interpretar(tree, table)
                if isinstance(value, Excepcion): 
                    tree.updateConsola("Error: Semantico, Se esperaba un valor booleano para la condicion Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.fila, self.columna)

                if value.valor:
                    tabla = TablaSimbolos(table)
                    tabla.setEntorno("Sentencia If")
                    tree.setTablaSimbolos(tabla)

                    for j in i.listaInstruccionesIF:
                        #print("1CONDICIONAL-IF -> ", j )
                        if isinstance(j, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return j

                        if isinstance(j, SentenciaTransferencia):
                            if j != None:
                                return j

                        result = j.interpretar(tree, tabla)
                        #print("2CONDICIONAL-IF -> ", result, '\n' )
                        if isinstance(result, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return result

                        
                    return
            
            #_------------------ ELSE -----------------
            value = self.sentenciaElse.interpretar(tree, table)
            tabla = TablaSimbolos(table)
            tabla.setEntorno("Sentencia Else")
            tree.setTablaSimbolos(tabla)
            for i in value.listaInstruccionesELSE:
                #print("CONDICIONAL-ELSE -> ", i.expresion )
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, Se esperaba un valor booleano para la condicion Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.fila, self.columna)
                
                if isinstance(i, SentenciaTransferencia):
                    if i != None:
                        return i
                

                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return result

                

    def getNodo(self):
        if self.sentenciaElse == None:
            nodo1 = NodoArbol("SENTENCIAS \n CONDICIONALES")
            nodo = nodo1
            contador = 0
            contador_nodos = len(self.sentenciaIf)
            for k in self.sentenciaIf:
                if len(self.sentenciaIf) == 1:
                    nodo3 = NodoArbol("SENTENCIA \n CONDICIONAL")
                    nodo3.addNodo(k.getNodo())
                    nodo1.addNodo(nodo3)
                else:
                    if contador != len(self.sentenciaIf) -1 :
                        nodo2 = NodoArbol("SENTENCIAS \n CONDICIONALES")
                        nodo1.addNodo(nodo2)
                        nodo3 = NodoArbol("SENTENCIA \n CONDICIONAL")
                        nodo3.addNodo(self.sentenciaIf[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)
                        nodo1 = nodo2
                    else:
                        nodo3 = NodoArbol("SENTENCIA \n CONDICIONAL")
                        nodo3.addNodo(self.sentenciaIf[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)

                    contador +=1
                    contador_nodos -=1

            nodo.addleaf("END")
            nodo.addleaf(";")
            return nodo
        else:
            nodo1 = NodoArbol("SENTENCIAS \n CONDICIONALES")
            nodo = nodo1
            contador = 0
            self.sentenciaIf.append(self.sentenciaElse)
            contador_nodos = len(self.sentenciaIf)
            for k in self.sentenciaIf:
                if len(self.sentenciaIf) == 1:
                    nodo3 = NodoArbol("SENTENCIA \n CONDICIONAL")
                    nodo3.addNodo(k.getNodo())
                    nodo1.addNodo(nodo3)
                else:
                    if contador != len(self.sentenciaIf) -1 :
                        nodo2 = NodoArbol("SENTENCIAS \n CONDICIONALES")
                        nodo1.addNodo(nodo2)
                        nodo3 = NodoArbol("SENTENCIA \n CONDICIONAL")
                        nodo3.addNodo(self.sentenciaIf[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)
                        nodo1 = nodo2
                    else:
                        nodo3 = NodoArbol("SENTENCIA \n CONDICIONAL")
                        nodo3.addNodo(self.sentenciaIf[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)

                    contador +=1
                    contador_nodos -=1

            nodo.addleaf("END")
            nodo.addleaf(";")
            return nodo