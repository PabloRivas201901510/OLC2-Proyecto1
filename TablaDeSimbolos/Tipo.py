from enum import Enum


class Tipo:
    def __init__(self, entrada):
        self.tipo = entrada
        
    def equeals(self, entrada):
        return self.tipo == entrada

    def getTipos(self):
        return self.tipo

    def setTipo(self, entrada):
        self.tipo = entrada



class tipos(Enum):
    ENTERO = 1
    CARACTER = 2
    BOOLEANO = 3
    DECIMAL = 4
    CADENA = 5
    BREAK = 6
    CONTINUE = 7
    RETURN = 8
    STRUCT = 9
    LISTA = 10
    FUNCION = 11
    NINGUNA = 12
    NONE = 13
    ARREGLO = 14
    GLOBAL = 15