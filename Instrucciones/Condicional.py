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
                                print('METODO IF -> ', j, '\n')
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
                        print('METODO ELSE -> ', i, '\n')
                        return i
                

                result = i.interpretar(tree, tabla)
                #print("2CONDICIONAL-ELSE -> ", result, '\n' )
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return result

                

    

            

    def getNodo(self):
        pass