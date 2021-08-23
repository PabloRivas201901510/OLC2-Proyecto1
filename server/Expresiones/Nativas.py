from server.Excepciones.Excepcion import Excepcion
from server.TablaDeSimbolos.Tipo import Tipo, tipos
from server.Abstract.instruccion import instruccion
from server.Expresiones.Primitivo import Primitivo
from enum import Enum
from math import log, sin, cos, tan, sqrt


class Nativas(instruccion):
    def __init__(self, fila, columna, expresion, base,  nativa):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.nativa = nativa
        if base == None:
            self.expresion = expresion
            self.base = None
        else:
            self.expresion = expresion
            self.base = base

    def interpretar(self, tree, table):
        izquierdo = None
        derecho = None

        if self.base != None:
            izquierdo = self.expresion.interpretar(tree, table)
            if isinstance(izquierdo, Excepcion): return izquierdo
            derecho = self.base.interpretar(tree, table)
            if isinstance(derecho, Excepcion): return derecho
        else:
            izquierdo = self.expresion.interpretar(tree, table)
            if isinstance(izquierdo, Excepcion): return izquierdo

        #-----------LOGARITMO--------------
        if(self.nativa == tipos_nativas.LOGARITMO):
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, log(float(izquierdo.valor), int(derecho.valor)))
                else:
                    return Excepcion("sintactico", "Error en nativas con LOGARITMO", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Error en nativas con LOGARITMO", self.fila, self.columna)

        # -----------LOGARITMO10--------------
        elif (self.nativa == tipos_nativas.LOGARITMO10):
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, log(float(izquierdo.valor), 10))
            else:
                return Excepcion("sintactico", "Error en nativas con LOGARITMO BASE10", self.fila, self.columna)

        # -----------SENO--------------
        elif (self.nativa == tipos_nativas.SENO):
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, sin(izquierdo.valor))
            else:
                return Excepcion("sintactico", "Error en nativas con SENO", self.fila, self.columna)

        # -----------COSENO--------------
        elif (self.nativa == tipos_nativas.COSENO):
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, cos(izquierdo.valor))
            else:
                return Excepcion("sintactico", "Error en nativas con COSENO", self.fila, self.columna)

        # -----------TANGENTE--------------
        elif (self.nativa == tipos_nativas.TANGENTE):
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, tan(izquierdo.valor))
            else:
                return Excepcion("sintactico", "Error en nativas con TANGENTE", self.fila, self.columna)

        # -----------RAIZ CUADRADA--------------
        elif (self.nativa == tipos_nativas.RAIZCUADRADA):
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, sqrt(izquierdo.valor))
            else:
                return Excepcion("sintactico", "Error en nativas con RAIZ CUADRADA", self.fila, self.columna)

        # -----------UPPERCASE--------------
        elif (self.nativa == tipos_nativas.UPPERCASE):
            if izquierdo.tipo.getTipos() == tipos.CADENA:
                self.tipo = Tipo(tipos.CADENA)
                return Primitivo(self.tipo, self.fila, self.columna, str(izquierdo.valor).upper())
            else:
                return Excepcion("sintactico", "Error en nativas con UPPERCASE", self.fila, self.columna)

        # -----------LOWERCASE--------------
        elif (self.nativa == tipos_nativas.LOWERCASE):
            if izquierdo.tipo.getTipos() == tipos.CADENA:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, str(izquierdo.valor).lower())
            else:
                return Excepcion("sintactico", "Error en nativas con LOWERCASE", self.fila, self.columna)




    def getNodo(self):
        pass



class tipos_nativas(Enum):
    LOGARITMO10 = 1
    LOGARITMO = 2
    SENO = 3
    COSENO = 4
    TANGENTE = 5
    RAIZCUADRADA = 6
    PARSE = 7
    UPPERCASE = 8
    LOWERCASE = 9