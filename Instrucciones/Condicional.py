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
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en la sentencia IF", self.linea, self.columna)
                value = i.condicion.interpretar(tree, table)
                if isinstance(value, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.linea, self.columna)

                if value.valor:
                    tabla = TablaSimbolos(table)
                    tabla.setEntorno("Sentencia If")
                    tree.setTablaSimbolos(tabla)
                    for j in i.listaInstruccionesIF:
                        if isinstance(j, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return j

                        result = j.interpretar(tree, tabla)
                        if isinstance(result, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return result

                        if isinstance(result, SentenciaTransferencia):
                            #print('TRANSFERENCIA -> ', result)
                            if result != None:
                                return result
                    return
        else:
            #--------------- IF ----------------------
            for i in self.sentenciaIf:
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en la sentencia IF", self.linea, self.columna)
                value = i.condicion.interpretar(tree, table)
                if isinstance(value, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.linea, self.columna)

                if value.valor:
                    tabla = TablaSimbolos(table)
                    tabla.setEntorno("Sentencia If")
                    tree.setTablaSimbolos(tabla)
                    for j in i.listaInstruccionesIF:
                        if isinstance(j, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return j

                        result = j.interpretar(tree, tabla)
                        if isinstance(result, Excepcion): 
                            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                            return result

                        if isinstance(result, SentenciaTransferencia):
                            if result != None:
                                return result
                    return
            
            #_------------------ ELSE -----------------
            #print(self.sentenciaElse)

            value = self.sentenciaElse.interpretar(tree, table)
            tabla = TablaSimbolos(table)
            tabla.setEntorno("Sentencia Else")
            tree.setTablaSimbolos(tabla)
            for i in value.listaInstruccionesELSE:
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.linea, self.columna)

                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return result

                if isinstance(result, SentenciaTransferencia):
                    if result != None:
                        if result.getTipo().getTipos() == tipos.BREAK: return result
                        elif result.getTipo().getTipos() == tipos.CONTINUE: return result
                        elif result.getTipo().getTipos() == tipos.RETURN: return result

    

            

    def getNodo(self):
        pass