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
        self.identificador = identificador + "_funtion"
        self.lista_parametros = lista_parametros
        self.lista_instrucciones = lista_instrucciones

    def interpretar(self, tree, table):
        table.setVariable(Simbolo(Tipo(tipos.FUNCION), self.identificador, self.fila, self.columna, self))

    def getNodo(self):
        pass

    def getParametros(self):
        return self.lista_parametros

    def getInstrucciones(self):
        return self.lista_instrucciones