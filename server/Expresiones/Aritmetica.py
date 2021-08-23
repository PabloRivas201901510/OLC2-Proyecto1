from server.Abstract.NodoArbol import NodoArbol
from server.TablaDeSimbolos.Simbolo import Simbolo
from server.Excepciones.Excepcion import Excepcion
from server.TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from server.TablaDeSimbolos.Tipo import Tipo, tipos
from server.Abstract.instruccion import instruccion
from server.Expresiones.Primitivo import Primitivo
from enum import Enum

class Aritmetica(instruccion):
    def __init__(self, fila, columna, izquierda, derecha, operador):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.operador = operador
        if derecha == None:
            self.opU = izquierda
        else:
            self.izquierda = izquierda
            self.derecha = derecha
            self.opU = None

    def interpretar(self, tree, table):
        izquierdo = None
        derecho = None
        unario = None

        if self.opU == None:
            izquierdo = self.izquierda.interpretar(tree, table)
            if isinstance(izquierdo, Excepcion): return izquierdo

            derecho = self.derecha.interpretar(tree, table)
            if isinstance(derecho, Excepcion): return derecho
        else:
            unario = self.opU.interpretar(tree, table)
            if isinstance(unario, Excepcion): return unario

        # ---------------MENOS UNARIO---------------
        if self.operador == tipos_Aritmetica.MENOSUNARIO:
            # -------------ENTERO-------------
            if unario.tipo.getTipos() == tipos.ENTERO:
                self.tipo = Tipo(tipos.ENTERO)
                return Primitivo(self.tipo, self.fila, self.columna, int(unario.valor) * (-1))
            # -------------DECIMAL-------------
            elif unario.tipo.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, float(unario.valor) * (-1))
            else:
                return Excepcion("sintactico", "Operandos invalidos -u", self.fila, self.columna)

        #---------------SUMA---------------
        elif self.operador == tipos_Aritmetica.SUMA:
            #-------------ENTERO-------------
            if izquierdo.tipo.getTipos() == tipos.ENTERO:
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.ENTERO)
                    return Primitivo(self.tipo, self.fila, self.columna, int(izquierdo.valor) + int(derecho.valor))
                elif derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) + float(derecho.valor))
                    # -------------CARACTER-------------
                elif derecho.tipo.getTipos() == tipos.CADENA or derecho.tipo.getTipos() == tipos.CADENA:
                    self.tipo = Tipo(tipos.CADENA)
                    return Primitivo(self.tipo, self.fila, self.columna, str(izquierdo.valor) + str(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos +", self.fila, self.columna)
            #-------------DECIMAL-------------
            elif izquierdo.tipo.getTipos() == tipos.DECIMAL:
                #----------ENTERO OR DECIMAL----------
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) + float(derecho.valor))
                # -------------CARACTER-------------
                elif derecho.tipo.getTipos() == tipos.CADENA or derecho.tipo.getTipos() == tipos.CADENA:
                    self.tipo = Tipo(tipos.CADENA)
                    return Primitivo(self.tipo, self.fila, self.columna, str(izquierdo.valor) + str(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos +", self.fila, self.columna)
            # -------------CARACTER-------------
            elif izquierdo.tipo.getTipos() == tipos.CADENA:
                # ----------ENTERO OR DECIMAL OR CADENA----------
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL or derecho.tipo.getTipos() == tipos.CADENA:
                    self.tipo = Tipo(tipos.CADENA)
                    return Primitivo(self.tipo, self.fila, self.columna, str(izquierdo.valor) + str(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos +", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Operandos invalidos +", self.fila, self.columna)

        # ---------------RESTA---------------
        elif self.operador == tipos_Aritmetica.RESTA:
            # ----------- ENTERO -------------
            if izquierdo.tipo.getTipos() == tipos.ENTERO:
                #----------- ENTERO -------------
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.ENTERO)
                    return Primitivo(self.tipo, self.fila, self.columna, int(izquierdo.valor) - int(derecho.valor))
                #----------- DECIMAL ------------
                elif derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) - float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos -", self.fila, self.columna)
            # ----------- DECIMAL -------------
            elif izquierdo.tipo.getTipos() == tipos.DECIMAL:
                # ----------- ENTERO or DECIMAL -------------
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) - float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos -", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Operandos invalidos -", self.fila, self.columna)

        # ---------------MULTIPLICACION---------------
        elif self.operador == tipos_Aritmetica.MULTIPLICACION:
            # ----------- ENTERO -------------
            if izquierdo.tipo.getTipos() == tipos.ENTERO:
                # ----------- ENTERO -------------
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.ENTERO)
                    return Primitivo(self.tipo, self.fila, self.columna, int(izquierdo.valor) * int(derecho.valor))
                # ----------- DECIMAL ------------
                elif derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) * float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos *", self.fila, self.columna)
            # ----------- DECIMAL -------------
            elif izquierdo.tipo.getTipos() == tipos.DECIMAL:
                # ----------- ENTERO or DECIMAL -------------
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) * float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos *", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Operandos invalidos *", self.fila, self.columna)

        # ---------------DIVISION---------------
        elif self.operador == tipos_Aritmetica.DIVISION:
            # ---------------ENTERO---------------
            if izquierdo.tipo.getTipos() == tipos.ENTERO or izquierdo.tipo.getTipos() == tipos.DECIMAL:
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) / float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos /", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Operandos invalidos /", self.fila, self.columna)

        # ---------------POTENCIA---------------
        elif self.operador == tipos_Aritmetica.POTENCIA:
            # ---------------ENTERO---------------
            if izquierdo.tipo.getTipos() == tipos.ENTERO:
                # ---------------ENTERO---------------
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.ENTERO)
                    return Primitivo(self.tipo, self.fila, self.columna, int(izquierdo.valor) ** int(derecho.valor))
                # ---------------DECIMAL---------------
                elif derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) ** float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos ^", self.fila, self.columna)
            # ---------------DECIMAL---------------
            elif izquierdo.tipo.getTipos() == tipos.DECIMAL:
                # ---------------ENTERO---------------
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) ** float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos ^", self.fila, self.columna)
            # ---------------CADENA---------------
            elif izquierdo.tipo.getTipos() == tipos.CADENA:
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.CADENA)
                    contador = 0;
                    cadena = ""
                    while contador < int(derecho.valor):
                        cadena += izquierdo.valor
                        contador += 1
                    return Primitivo(self.tipo, self.fila, self.columna, cadena)
                else:
                    return Excepcion("sintactico", "Operandos invalidos ^", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Operandos invalidos ^", self.fila, self.columna)

        # ---------------MODULO---------------
        elif self.operador == tipos_Aritmetica.MODULO:
            # ---------------ENTERO---------------
            if izquierdo.tipo.getTipos() == tipos.ENTERO:
                # ---------------ENTERO---------------
                if derecho.tipo.getTipos() == tipos.ENTERO:
                    self.tipo = Tipo(tipos.ENTERO)
                    return Primitivo(self.tipo, self.fila, self.columna, int(izquierdo.valor) % int(derecho.valor))
                # ---------------DECIMAL---------------
                elif derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna,
                                     float(izquierdo.valor) ** float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos %", self.fila, self.columna)
            # ---------------DECIMAL---------------
            elif izquierdo.tipo.getTipos() == tipos.DECIMAL:
                # ---------------ENTERO---------------
                if derecho.tipo.getTipos() == tipos.ENTERO or derecho.tipo.getTipos() == tipos.DECIMAL:
                    self.tipo = Tipo(tipos.DECIMAL)
                    return Primitivo(self.tipo, self.fila, self.columna, float(izquierdo.valor) % float(derecho.valor))
                else:
                    return Excepcion("sintactico", "Operandos invalidos %", self.fila, self.columna)
            else:
                return Excepcion("sintactico", "Operandos invalidos %", self.fila, self.columna)
        else:
            return Excepcion("sintactico", "Operandos invalidos +-*/^%", self.fila, self.columna)


    def getNodo(self):
        pass

class tipos_Aritmetica(Enum):
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3
    DIVISION = 4
    MENOSUNARIO = 5
    POTENCIA = 6
    MODULO = 7