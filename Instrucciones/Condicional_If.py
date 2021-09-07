from TablaDeSimbolos.Simbolo import Simbolo
from Excepciones.Excepcion import Excepcion
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Tipo import Tipo, tipos
from Abstract.instruccion import instruccion
from Abstract.NodoArbol import NodoArbol


class Condicional_If(instruccion):
    def __init__(self, fila, columna, condicion, listaInstruccionesIF, listaInstruccionesELSE, elseIF):
        super().__init__(Tipo(tipos.CADENA), fila, columna)
        self.condicion = condicion
        self.listaInstruccionesIF = listaInstruccionesIF
        self.listaInstruccionesELSE = listaInstruccionesELSE
        self.elseIF = elseIF

    def interpretar(self, tree, table):
        return self
        print("ENTRE EN CONDICIONAL_IF")
        condicion = None
        if self.condicion != None:
            value = self.condicion.interpretar(tree, table)
            if isinstance(value, Excepcion): return value

            if(self.condicion.tipo.getTipos() != tipos.BOOLEANO):
                tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.linea, self.columna)

            condicion = value.valor

        print("CONDICION")
        print(condicion)
        if condicion:
            print("ENTRE AL IF")
            tabla = TablaSimbolos(table)
            tabla.setEntorno("Sentencia If")
            tree.setTablaSimbolos(tabla)
            for i in self.listaInstruccionesIF:

                if isinstance(i, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.linea, self.columna)

                result = i.interpretar(tree, tabla)
                if isinstance(result, Excepcion): 
                    tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                    return result

                if result != None:
                    if result.getTipo().getTipos() == tipos.BREAK: return result
                    elif result.getTipo().getTipos() == tipos.CONTINUE: return result
                    elif result.getTipo().getTipos() == tipos.RETURN: return result
        else:
            if self.listaInstruccionesELSE != None:
                print("ENTRE AL ELSE")
                tabla = TablaSimbolos(table)
                tabla.setEntorno("Sentencia Elseif")
                tree.setTablaSimbolos(tabla)
                for i in self.listaInstruccionesELSE:
                    if isinstance(i, Excepcion): 
                        tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return Excepcion("Semantico", "Se esperaba un valor booleano para la condicion", self.linea, self.columna)

                    result = i.interpretar(tree, tabla)
                    if isinstance(result, Excepcion): 
                        tree.updateConsola("Error: Semantico, condicional Fila:"+str(self.fila)+" columna:"+str(self.columna)+"\n")
                        return result

                    if result != None:
                        if result.getTipo().getTipos() == tipos.BREAK: return result
                        elif result.getTipo().getTipos() == tipos.CONTINUE: return result
                        elif result.getTipo().getTipos() == tipos.RETURN: return result

            elif self.elseIF != None:
                print(self.elseIF)
                result = self.elseIF.interpretar(tree, table)
                return True

    def getNodo(self):
        pass