from TablaDeSimbolos.Arbol import Arbol
from TablaDeSimbolos.Tipo import Tipo
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos

class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.leafs = []

    def setLeaf(self, leaf):
        self.leafs = leaf

    def addleaf(self, valor):
        self.leafs.append(NodoArbol(str(valor)))

    def addleafs(self, hijos):
        for i in hijos:
            self.leafs.append(i)

    def addNodo(self, hijo):
        if hijo: self.leafs.append(hijo)

    def getLeafs(self):
        return self.leafs

    def getValor(self):
        return self.valor
    