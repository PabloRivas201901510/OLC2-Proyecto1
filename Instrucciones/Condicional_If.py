from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class Condicional_If(instruccion):
    def __init__(self, fila, columna, condicion, listaInstruccionesIF, listaInstruccionesELSE, elseIF):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.condicion = condicion
        self.listaInstruccionesIF = listaInstruccionesIF
        self.listaInstruccionesELSE = listaInstruccionesELSE
        self.elseIF = elseIF

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoArbol("CONDICIONAL")
        if self.elseIF == "if":
            nodo.addleaf("if")
            nodo.addNodo(self.condicion.getNodo())

            nodo1 = NodoArbol("INSTRUCCIONES")
            nodo.addNodo(nodo1)
            contador = 0
            contador_nodos = len(self.listaInstruccionesIF)
            for k in self.listaInstruccionesIF:
                if len(self.listaInstruccionesIF) == 1:
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(k.getNodo())
                    nodo1.addNodo(nodo3)
                else:
                    if contador != len(self.listaInstruccionesIF) -1 :
                        nodo2 = NodoArbol("INSTRUCCIONES")
                        nodo1.addNodo(nodo2)
                        nodo3 = NodoArbol("INSTRUCCION")
                        nodo3.addNodo(self.listaInstruccionesIF[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)
                        nodo1 = nodo2
                    else:
                        nodo3 = NodoArbol("INSTRUCCION")
                        nodo3.addNodo(self.listaInstruccionesIF[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)

                    contador +=1
                    contador_nodos -=1
            return nodo

        elif self.elseIF == "elseif":
            nodo.addleaf("elseif")
            nodo.addNodo(self.condicion.getNodo())

            nodo1 = NodoArbol("INSTRUCCIONES")
            nodo.addNodo(nodo1)
            contador = 0
            contador_nodos = len(self.listaInstruccionesIF)
            for k in self.listaInstruccionesIF:
                if len(self.listaInstruccionesIF) == 1:
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(k.getNodo())
                    nodo1.addNodo(nodo3)
                else:
                    if contador != len(self.listaInstruccionesIF) -1 :
                        nodo2 = NodoArbol("INSTRUCCIONES")
                        nodo1.addNodo(nodo2)
                        nodo3 = NodoArbol("INSTRUCCION")
                        nodo3.addNodo(self.listaInstruccionesIF[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)
                        nodo1 = nodo2
                    else:
                        nodo3 = NodoArbol("INSTRUCCION")
                        nodo3.addNodo(self.listaInstruccionesIF[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)

                    contador +=1
                    contador_nodos -=1
        else:
            nodo.addleaf("else")

            nodo1 = NodoArbol("INSTRUCCIONES")
            nodo.addNodo(nodo1)
            contador = 0
            contador_nodos = len(self.listaInstruccionesELSE)
            for k in self.listaInstruccionesELSE:
                if len(self.listaInstruccionesELSE) == 1:
                    nodo3 = NodoArbol("INSTRUCCION")
                    nodo3.addNodo(k.getNodo())
                    nodo1.addNodo(nodo3)
                else:
                    if contador != len(self.listaInstruccionesELSE) -1 :
                        nodo2 = NodoArbol("INSTRUCCIONES")
                        nodo1.addNodo(nodo2)
                        nodo3 = NodoArbol("INSTRUCCION")
                        nodo3.addNodo(self.listaInstruccionesELSE[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)
                        nodo1 = nodo2
                    else:
                        nodo3 = NodoArbol("INSTRUCCION")
                        nodo3.addNodo(self.listaInstruccionesELSE[contador_nodos-1].getNodo()) 
                        nodo1.addNodo(nodo3)

                    contador +=1
                    contador_nodos -=1
                    
        return nodo

 