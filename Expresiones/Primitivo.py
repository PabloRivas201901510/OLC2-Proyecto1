from Abstract.NodoArbol import NodoArbol
from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion

class Primitivo(instruccion):
    def __init__(self, tipo, fila, columna, valor):
        super().__init__(tipo, fila, columna)
        self.valor = valor
        self.Tree = None
        self.Table = None

    def interpretar(self, tree, table):
        self.Tree = tree
        self.Table = table
        return self

    def getNodo(self):
        nodo2 = NodoArbol("PRIMITIVO")
        if self.tipo.getTipos() == tipos.ARREGLO:
            nodo2.addleaf(self.Desgloce_Arreglos(self.valor, self.Tree, self.Table))
        else:
            nodo2.addleaf(self.valor)
        return nodo2

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getTipo(self):
        return self.tipo

    def Desgloce_Arreglos(self, vector, tree, table):
        res = "["
        for i in vector:
            if(i == "[" or i == "]"):
                res += i
                continue
            tmp = i.interpretar(tree, table)
            if isinstance(tmp, Excepcion):
                tree.updateConsola("El arreglo tiene un error en sus parametros"+"\n")
                return
            if tmp.tipo.getTipos() == tipos.ARREGLO:
                res += self.Desgloce_Arreglos( tmp.valor, tree, table) + ","
            else:
                res += str(tmp.valor)
                res += ","
        res = res[:-1]
        res += "]"
        return str(res)