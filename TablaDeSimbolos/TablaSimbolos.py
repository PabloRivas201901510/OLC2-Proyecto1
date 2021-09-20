
from TablaDeSimbolos.Simbolo import Simbolo
from TablaDeSimbolos.Tipo import Tipo, tipos
from Excepciones.Excepcion import Excepcion

class TablaSimbolos:
    def __init__(self, anterior = None, entorno = None):
        self.tabla = {}
        self.anterior = anterior
        self.tipo = Tipo(tipos.ENTERO)
        self.entorno = entorno


    def setVariable(self, simbolo:Simbolo):
        if simbolo.id in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id] = simbolo
            return None


    def getVariable(self, identificador):
        tablaActual = self
        while tablaActual != None:
            
            if identificador in tablaActual.tabla :
                return tablaActual.tabla[identificador]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None


    def getTable(self):
        return self.tabla

    def setTable(self, table):
        self.tabla = table

    def getAnterior(self):
        return self.anterior

    def setAnterior(self, table):
        self.anterior = table

    def getEntorno(self):
        return self.entorno

    def setEntorno(self, entorno):
        self.entorno = entorno
    