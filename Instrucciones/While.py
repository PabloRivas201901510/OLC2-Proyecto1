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
        if isinstance(condicion, Excepcion): return condicion
        if self.condicion.tipo.getTipos() != tipos.BOOLEANO:
            tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
            return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.fila, self.columna)

        tabla = TablaSimbolos(table)
        tabla.setEntorno("WHILE")
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
                elif isinstance(result, SentenciaTransferencia):
                    if result.tipo.getTipos() == tipos.BREAK: return
                    elif result.tipo.getTipos() == tipos.CONTINUE: break
                    elif result.tipo.getTipos() == tipos.RETURN:  return result

            condicion = self.condicion.interpretar(tree, table)

    def getNodo(self):
        nodo = NodoArbol("LOOP WHILE")
        nodo.addleaf("while")
        nodo.addNodo(self.condicion.getNodo())

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