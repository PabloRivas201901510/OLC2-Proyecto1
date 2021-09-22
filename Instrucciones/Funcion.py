from TablaDeSimbolos.Arbol import Arbol
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.SentenciaTransferencia import SentenciaTransferencia

class Funcion(instruccion):
    def __init__(self, fila, columna, identificador, lista_parametros, lista_instrucciones):
        super().__init__(Tipo(tipos.FUNCION), fila, columna)
        self.identificador = identificador 
        self.lista_parametros = lista_parametros
        self.lista_instrucciones = lista_instrucciones

    def interpretar(self, tree, table):
        table.setVariable(Simbolo(Tipo(tipos.FUNCION), self.identificador+ "_funtion", self.fila, self.columna, self))

    def getNodo(self):
        nodo = NodoArbol("FUNCION")

        nodo.addleaf("function")

        nn1 = NodoArbol("IDENTIFICADOR")
        nn1.addleaf(self.identificador)
        nodo.addNodo(nn1)

        nodo.addleaf("(")

        if self.lista_parametros:
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

        nodo1 = NodoArbol("INSTRUCCIONES")
        nodo.addNodo(nodo1)
        contador = 0
        contador_nodos = len(self.lista_instrucciones)
        for k in self.lista_instrucciones:
            if len(self.lista_instrucciones) == 1:
                nodo3 = NodoArbol("INSTRUCCION")
                nodo3.addNodo(k.getNodo())
                nodo1.addNodo(nodo3)
            else:
                if contador != len(self.lista_instrucciones) -1 :
                    nodo2 = NodoArbol("INSTRUCCIONES")
                    nodo1.addNodo(nodo2)
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(self.lista_instrucciones[contador_nodos-1].getNodo()) 
                    nodo1.addNodo(nodo3)
                    nodo1 = nodo2
                else:
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(self.lista_instrucciones[contador_nodos-1].getNodo()) 
                    nodo1.addNodo(nodo3)

                contador +=1
                contador_nodos -=1

        nodo.addleaf("END")
        nodo.addleaf(";")
        return nodo

    def getParametros(self):
        return self.lista_parametros

    def getInstrucciones(self):
        return self.lista_instrucciones