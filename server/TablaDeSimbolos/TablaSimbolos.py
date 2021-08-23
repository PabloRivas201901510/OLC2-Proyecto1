from server.TablaDeSimbolos.Simbolo import Simbolo
from server.TablaDeSimbolos.Tipo import Tipo, tipos


class TablaSimbolos:
    def __init__(self, anterior = None, entorno = None):
        self.tabla = {}
        self.anterior = anterior
        self.tipo = Tipo(tipos.ENTERO)
        self.entorno = entorno


    def setVariable(self, simbolo:Simbolo):
        tmp:TablaSimbolos = self
        contador = 0
        while tmp != None:
            encontro:Simbolo = tmp.getTable()[contador].simbolo.getIdentificador()
            if encontro != None:
                return "La variable con el identificador "+simbolo.getIdentificador()+" ya existe"
            tmp:TablaSimbolos = tmp.getAnterior()
            contador += 1
        self.tabla.insert(simbolo)
        return "La variable "+simbolo.getIdentificador()+" se creo exitosamente!"


    def getVariable(self, identificador):
        tmp:TablaSimbolos = self
        contador = 0
        while tmp != None:
            encontro:Simbolo = tmp.getTable().get(identificador)
            if encontro != None:
                return encontro
            tmp:TablaSimbolos = tmp.getAnterior()
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
    