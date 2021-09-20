from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Expresiones.Primitivo import Primitivo
from enum import Enum


class FuncionNativa(instruccion):
    def __init__(self,  fila, columna, izquierda, derecha, operador):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.operador = operador
        self.type = izquierda
        self.expresion = derecha

    def interpretar(self, tree, table):
        #print("funcion nativa")
        #print(self.expresion)
        expresion = self.expresion.interpretar(tree, table)
        #print(expresion)
        if isinstance(expresion, Excepcion): return expresion
        
        #------------- FUNCION PARSE --------------
        if self.operador == tipos_funcionnativa.PARSE:
            if self.type.getTipos() == tipos.ENTERO:
                self.tipo = Tipo(tipos.ENTERO)
                return Primitivo(self.tipo, self.fila, self.columna, int(expresion.valor))
            elif self.type.getTipos() == tipos.DECIMAL:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, float(expresion.valor))
            else:
                tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("sintactico", "Error en el parse", self.fila, self.columna)
        #------------- FUNCION TRUNC ------------
        elif self.operador == tipos_funcionnativa.TRUNC:
            if self.type.getTipos() == tipos.ENTERO:
                self.tipo = Tipo(tipos.ENTERO)
                return Primitivo(self.tipo, self.fila, self.columna, int(expresion.valor))
            else:
                tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("sintactico", "Error en el parse", self.fila, self.columna)
        #----------FUNCION FLOAT--------
        elif self.operador == tipos_funcionnativa.FLOAT:
            #print("floar-> "+str(expresion.getTipo()))
            if expresion.tipo.getTipos() == tipos.ENTERO:
                self.tipo = Tipo(tipos.DECIMAL)
                return Primitivo(self.tipo, self.fila, self.columna, float(expresion.valor))
            else:
                tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("sintactico", "Error en el float()", self.fila, self.columna)

        #----------FUNCION STRING--------
        elif self.operador == tipos_funcionnativa.STRING:
            self.tipo = Tipo(tipos.CADENA)
            return Primitivo(self.tipo, self.fila, self.columna, str(expresion.valor))

        #----------FUNCION TYPEOF--------
        elif self.operador == tipos_funcionnativa.TYPEOF:
            self.tipo = Tipo(tipos.CADENA)
            if expresion.tipo.getTipos() == tipos.ENTERO:
                return Primitivo(self.tipo, self.fila, self.columna, "Int64")
            elif expresion.tipo.getTipos() == tipos.DECIMAL:
                return Primitivo(self.tipo, self.fila, self.columna, "Float64")
            elif expresion.tipo.getTipos() == tipos.CADENA:
                return Primitivo(self.tipo, self.fila, self.columna, "String")
            elif expresion.tipo.getTipos() == tipos.BOOLEANO:
                return Primitivo(self.tipo, self.fila, self.columna, "Bool")
            elif expresion.tipo.getTipos() == tipos.CARACTER:
                return Primitivo(self.tipo, self.fila, self.columna, "Char")
            elif expresion.tipo.getTipo() == tipos.VECTOR:
                return Primitivo(self.tipo, self.fila, self.columna, "Arreglo")
            else:
                tree.updateConsola("Error: Semanticot, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("sintactico", "Error en el Typeof()", self.fila, self.columna)
        else:
                tree.updateConsola("Error: Semantico, Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("sintactico", "Error en las funciones nativas", self.fila, self.columna)

        

        

    def getNodo(self):
        pass

class tipos_funcionnativa(Enum):
    PARSE = 1
    TRUNC = 2
    FLOAT = 3
    STRING = 4
    TYPEOF = 5