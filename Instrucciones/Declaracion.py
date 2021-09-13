from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class Declaracion(instruccion):
    def __init__(self, tipo, fila, columna, identificador, expresion):
        super().__init__(tipo, fila, columna)
        self.identificador = identificador
        self.expresion = expresion

    def interpretar(self, tree, table):
        
        expresion = self.expresion.interpretar(tree, table)
        if isinstance(expresion, Excepcion): return expresion
        #print('EXPRESION -> ', expresion.valor)


        #CUANDO SE INGRESA UNA VARIABLE PARA ASIGNAR A OTRA SE BUSCA
        tablaActual = table
        while tablaActual != None:
            if self.identificador in tablaActual.tabla :
                variable = tablaActual.tabla[self.identificador]
                variable.setValor(expresion)
                return
                if variable.getTipo().getTipos() == tipos.NINGUNA:
                    variable.setValor(expresion)
                else:
                    if expresion.tipo.getTipos() == variable.getTipo().getTipos():
                        #print("variable ya ")
                        variable.setValor(expresion)
                        return
                    else:
                        tree.updateConsola("\n"+"Error: Semantico, Los tipos de las variables no son iguales.  fila:"+str(self.fila)+", columna:"+str(self.columna)+"\n")
                        return Excepcion("Semantico", "Los tipos de las variables no son iguales", self.fila, self.columna)
                
                return  
            else:
                tablaActual = tablaActual.anterior
        
        # SI NO EXISTE LA VARIABLE SE CREA
        if self.tipo.getTipos() == tipos.NINGUNA:
            table.setVariable(Simbolo(self.tipo, self.identificador, self.fila, self.columna, expresion))
        else:
            if expresion.tipo.getTipos() == self.tipo.getTipos():
                #print('CON TIPO -> ',self.tipo.getTipos())
                table.setVariable(Simbolo(Tipo(expresion.tipo.getTipos()), self.identificador, self.fila, self.columna, expresion))
            else:
                tree.updateConsola("\n"+"Error: Semantico, Los tipos de las variables no son iguales fila:"+str(self.fila)+", columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "Los tipos de las variables no son iguales", self.fila, self.columna)
        return None
        

    def getNodo(self):
        pass