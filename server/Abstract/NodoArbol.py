from server.TablaDeSimbolos.Arbol import Arbol
from server.TablaDeSimbolos.Tipo import Tipo
from server.TablaDeSimbolos.TablaSimbolos import TablaSimbolos

class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.leafs = {}

    def setLeaf(self, leaf):
        self.leafs = leaf

    def addleaf(self, valor):
        self.leafs.pop(NodoArbol(valor+""))

    def addleafs(self, hijos):
        for i in hijos:
            self.leafs.pop(i)

    def addNodo(self, hijo):
        if hijo: self.leafs.pop(hijo)

    def getLeafs(self):
        return self.leafs