from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.SentenciaTransferencia import SentenciaTransferencia

class While(instruccion):
    def __init__(self, fila, columna, condicion, listaInstrucciones):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.condicion = condicion
        self.listaInstrucciones = listaInstrucciones

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if self.condicion.tipo.getTipos() != tipos.BOOLEANO:
            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
            return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.fila, self.columna)

        tabla = TablaSimbolos(table)
        tabla.setEntorno("Sentencia Else")
        tree.setTablaSimbolos(tabla)
        while condicion.valor:

            for i in self.listaInstrucciones:
                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en el ciclo WHILE", self.fila, self.columna)
                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Error en el ciclo WHILE", self.fila, self.columna)
                elif isinstance(result, SentenciaTransferencia): return result

            condicion = self.condicion.interpretar(tree, table)

    def getNodo(self):
        pass