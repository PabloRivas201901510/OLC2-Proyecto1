
import os
import re
import sys

errores = []
sys.setrecursionlimit(3000)
reservadas = {
    'Int64'     :'RTINT',
    'Float64'   :'FLOAT64',
    'String'    :'STRING',
    'Bool'      :'BOOL',
    'Char'      :'CHAR',
    'print'     : 'RPRINT',
    'println'   : 'RPRINTLN',
    'log10'     :'LOGARITMO10',
    'log'       :'LOGARITMO',
    'sin'       :'SENO',
    'cos'       :'COSENO',
    'tan'       :'TANGENTE',
    'sqrt'      :'RAIZCUADRADA',
    'uppercase' :'UPPERCASE',
    'lowercase' :'LOWERCASE',
    'true'      :'RTRUE',
    'false'     :'RFALSE',
    'parse'     :'RPARSE',
    'trunc'     :'RTRUNC',
    'float'     :'RFLOAT',
    'string'    :'RSTRING',
    'typeof'    :'RTYPEOF',
    'if'        :'RIF',
    'elseif'    :'RELSEIF',
    'else'      :'RELSE',
    'end'       :'REND',
    'while'     :'RWHILE',
    'break'     :'RBREAK',
    'continue'  :'RCONTINUE',
    'return'    :'RRETURN',
    'for'       :'RFOR',
    'in'        :'RIN',
    'push'      :'RPUSH',
    'pop'       :'RPOP',
    'length'    :'RLENGTH',
}
tokens  = [
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'ELEVADO',
    'MODULO',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'PTCOMA',
    'DOBLEDOS',
    'DOSPUNTOS',
    'COMA',
    'OR',
    'AND',
    'NOT',
    'IGUAL',
    'MAYOR',
    'MENOR',
    'ID',
    'PUNTOS',
]+ list(reservadas.values())

# Tokens
t_PARIZQ    = r'\('
t_PARDER    = r'\)'
t_CORIZQ    = r'\['
t_CORDER    = r'\]'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_ELEVADO = r'\^'
t_MODULO = r'\%'
t_PTCOMA    = r';'
t_DOBLEDOS = r'::'
t_DOSPUNTOS = r':'
t_COMA    = r'\,'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'\!'
t_IGUAL = r'\='
t_MAYOR = r'\>'
t_MENOR = r'\<'
t_PUNTOS = r'\.'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value,'ID')
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CARACTER(t):
    r'(\'.*?\')'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'\#=(.|\n)=?=\#'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico: " + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

    
# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL', 'MENOR', 'MAYOR', 'NOT'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'ELEVADO', 'MODULO'),
    ('right', 'UMENOS'),
)

from Excepciones.Excepcion import Excepcion
from Expresiones.Primitivo import Primitivo
from TablaDeSimbolos.Tipo import Tipo, tipos
from TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from TablaDeSimbolos.Arbol import Arbol
from Abstract.instruccion import instruccion

from Instrucciones.println import println, Tipo_Print
from Expresiones.Aritmetica import Aritmetica, tipos_Aritmetica
from Expresiones.Nativas import Nativas, tipos_nativas
from Expresiones.Logica import Logica, tipos_logicos
from Expresiones.Relacional import Relacional, tipos_relacional
from Instrucciones.Declaracion import Declaracion
from Expresiones.Variable import Variable
from Expresiones.FuncionNativa import FuncionNativa, tipos_funcionnativa
from Instrucciones.Condicional_If import Condicional_If
from Instrucciones.Condicional import Condicional
from Instrucciones.While import While
from Instrucciones.For import For
from Instrucciones.SentenciaTransferencia import SentenciaTransferencia
from Instrucciones.DeclararArreglos import DeclararArreglos, Tipo_Declaracion_Arreglo, Declaracion_Arreglo


# Definición de la gramática
def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]
    
def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    if t[2] != None:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_instrucciones_lista1(t):
    'instrucciones    : instruccion '
    if t[1] != None:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = []


def p_instrucciones_(t):
    '''instruccion      : ins_condicional
                        | ins_println
                        | ins_print
                        | ins_while
                        | ins_sen_transferencia
                        | ins_asignacion
                        | asignacion_instr_dos  PTCOMA
                        | ins_for 
                        | ins_arreglos_dimensionales'''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error PTCOMA'
    print(t[1])
    errores.append(Excepcion("Sintáctico","Error Sintáctico:" + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
   

def p_instrucciones_IMPRIMIRLN(t):
    'ins_println : RPRINTLN PARIZQ expresiones PARDER PTCOMA'
    t[0] = println(t[3], t.lineno(1), find_column(input, t.slice[1]), Tipo_Print.SALTO)

def p_instrucciones_IMPRIMIR(t):
    'ins_print : RPRINT PARIZQ expresiones PARDER PTCOMA'
    t[0] = println(t[3], t.lineno(1), find_column(input, t.slice[1]), Tipo_Print.LINEA)

def p_expresiones_lista(t):
    'expresiones    : expresiones COMA expresion'
    if t[2] != None:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_expresion_lista1(t):
    'expresiones   : expresion '
    if t[1] != None:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = []

#--------------------- DECLARACIONES Y ASIGNACIONES -----------------
def p_instrucciones_DECLARACION(t):
    'ins_asignacion : ID IGUAL expresion PTCOMA'
    t[0] = Declaracion(Tipo(tipos.NINGUNA), t.lineno(1), find_column(input, t.slice[1]), t[1], t[3])

def p_instrucciones_DECLARACION_TIPO(t):
    '''asignacion_instr_dos : ID IGUAL expresion DOBLEDOS tipodatos '''
    t[0] = Declaracion(t[5], t.lineno(1), find_column(input, t.slice[1]), t[1], t[3])

def p_tipop(t):
    '''tipodatos        : RTINT
                        | FLOAT64
                        | STRING
                        | CHAR
                        | BOOL'''
    if t[1] == "Int64":
        t[0] = Tipo(tipos.ENTERO)
    elif t[1] == "Float64":
        t[0] = Tipo(tipos.DECIMAL)
    elif t[1] == "String":
        t[0] = Tipo(tipos.CADENA)
    elif t[1] == "Char":
        t[0] = Tipo(tipos.CARACTER)
    elif t[1] == "Bool":
        t[0] = Tipo(tipos.BOOLEANO)






#-------------------------- SENTENCIA CONDICIONALES --------------
def p_instrucciones_condicional_1(t):
    '''ins_condicional : sentecias_if sentencia_else  REND PTCOMA'''
    t[0] = Condicional(t.lineno(1), 1, t[1], t[2])

def p_instrucciones_condicional_2(t):
    '''ins_condicional : sentecias_if  REND PTCOMA'''
    t[0] = Condicional(t.lineno(1), 1, t[1], None)

def p_instrucciones_condicional_3(t):
    '''sentecias_if : sentecias_if  sentecia_elseif'''
    if t[1] != None:
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_condicional_4(t):
    '''sentecias_if : sentecia_if'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]
      

def p_instrucciones_CONDICIONAL_IF(t):
    '''sentecia_if : RIF expresion instrucciones'''
    t[0] = Condicional_If(t.lineno(1), find_column(input, t.slice[1]), t[2], t[3], None, None)

def p_instrucciones_CONDICIONAL_ELSEIF(t):
    '''sentecia_elseif : RELSEIF  expresion  instrucciones'''
    t[0] = Condicional_If(t.lineno(1), find_column(input, t.slice[1]), t[2], t[3],  None,  None)

def p_instrucciones_CONDICIONAL_ELSE(t):
    '''sentencia_else : RELSE instrucciones'''
    t[0] = Condicional_If(t.lineno(1), find_column(input, t.slice[1]), None, None, t[2],  None)

#--------------------- WHILE ---------------------------------
def p_instrucciones_WHILE(t):
    '''ins_while : RWHILE expresion instrucciones REND PTCOMA'''
    t[0] = While(t.lineno(1), find_column(input, t.slice[1]), t[2], t[3])

#--------------------- FOR ---------------------------------
def p_instrucciones_FOR1(t):
    '''ins_for : RFOR ID RIN expresion DOSPUNTOS expresion instrucciones REND PTCOMA'''
    t[0] = For(t.lineno(1), find_column(input, t.slice[1]), t[2], t[4], t[6], True, False, False, t[7])

def p_instrucciones_FOR2(t):
    '''ins_for : RFOR ID RIN expresion instrucciones REND PTCOMA'''
    t[0] = For(t.lineno(1), find_column(input, t.slice[1]), t[2], t[4], None , False, True, False, t[5])

#---------------- SENTENCIAS DE TRANSFERENCIA ----------------------
def p_instrucciones_Sentencia_Transferencia(t):
    '''ins_sen_transferencia :    RCONTINUE PTCOMA
                                | RBREAK PTCOMA
                                | RRETURN PTCOMA'''
    if t[1] == "continue":
        t[0] = SentenciaTransferencia(Tipo(tipos.CONTINUE),t.lineno(1), find_column(input, t.slice[1]), None)
    elif t[1] == "break":
        t[0] = SentenciaTransferencia(Tipo(tipos.BREAK),t.lineno(1), find_column(input, t.slice[1]), None)
    elif t[1] == "return":
        t[0] = SentenciaTransferencia(Tipo(tipos.RETURN),t.lineno(1), find_column(input, t.slice[1]), None)
        

def p_instrucciones_Sentencia_Transferencia2(t):
    '''ins_sen_transferencia :  RRETURN expresion PTCOMA'''
    t[0] = SentenciaTransferencia(Tipo(tipos.RETURN), t.lineno(1), find_column(input, t.slice[1]), t[2])

#---------------------ARREGLOS DIMENSIONALES---------------------------
def p_instrucciones_Arreglos_dimensionales(t):
    '''ins_arreglos_dimensionales :  ID arreglos_lista IGUAL expresion PTCOMA'''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[1], t[2], t[4], Tipo_Declaracion_Arreglo.DECLARACION, Declaracion_Arreglo.MAS)

def p_instrucciones_Arreglos_dimensionales_PUSH_MAS(t):
    '''ins_arreglos_dimensionales :  ID arreglos_lista PUNTOS RPUSH PARIZQ expresion PARDER PTCOMA'''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[1], t[2], t[6], Tipo_Declaracion_Arreglo.PUSH, Declaracion_Arreglo.MAS)


def p_Arreglos_dimensionales_list1(t):
    'arreglos_lista    : arreglos_lista CORIZQ expresion CORDER'
    if t[2] != None:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_Arreglos_dimensionales_list2(t):
    'arreglos_lista   : CORIZQ expresion CORDER '
    if t[1] != None:
        t[0] = []
        t[0].append(t[2])
    else:
        t[0] = []

def p_expresion_POP_MAS(t):
    '''expresion :  ID arreglos_lista PUNTOS RPOP PARIZQ PARDER '''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[1], t[2], None, Tipo_Declaracion_Arreglo.POP, Declaracion_Arreglo.MAS)

def p_expresion_LENGTH_MAS(t):
    '''expresion :  RLENGTH PARIZQ ID arreglos_lista PARDER '''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[3], t[4], None, Tipo_Declaracion_Arreglo.LENGTH, Declaracion_Arreglo.MAS)


def p_instrucciones_Arreglos_dimensionales_PUSH_SIMPLE(t):
    '''ins_arreglos_dimensionales :  ID PUNTOS RPUSH PARIZQ expresion PARDER PTCOMA'''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[1], None, t[5], Tipo_Declaracion_Arreglo.PUSH, Declaracion_Arreglo.SIMPLE)

def p_instrucciones_Arreglos_dimensionales_POP_SIMPLE(t):
    '''expresion :  ID PUNTOS RPOP PARIZQ  PARDER'''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[1], None, None, Tipo_Declaracion_Arreglo.POP, Declaracion_Arreglo.SIMPLE)

def p_instrucciones_Arreglos_dimensionales_LENGTH_SIMPLE(t):
    '''expresion :  RLENGTH PARIZQ ID PARDER'''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[3], None, None, Tipo_Declaracion_Arreglo.LENGTH, Declaracion_Arreglo.SIMPLE)

def p_instrucciones_Arreglos_dimensionales_ACCEDER(t):
    '''expresion :  ID arreglos_lista'''
    t[0] = DeclararArreglos(t.lineno(1), find_column(input, t.slice[1]), t[1], t[2], None, Tipo_Declaracion_Arreglo.ACCEDER, Declaracion_Arreglo.MAS)
#---------------------- EXPRESIONES ARITMETICAS --------------------
def p_expresion_aritmetica(t):
    '''expresion : expresion MAS expresion
                  | expresion MENOS expresion
                  | expresion POR expresion
                  | expresion DIVIDIDO expresion
                  | expresion ELEVADO expresion
                  | expresion MODULO expresion'''
    if t[2] == '+':
        t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_Aritmetica.SUMA)
    elif t[2] == '-':
        t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_Aritmetica.RESTA)
    elif t[2] == '*':
        t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_Aritmetica.MULTIPLICACION)
    elif t[2] == '/':
        t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_Aritmetica.DIVISION)
    elif t[2] == '^':
        t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_Aritmetica.POTENCIA)
    elif t[2] == '%':
        t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_Aritmetica.MODULO)

#------------- EXPRESIONES LOGICAS -------------------
def p_expresion_logica(t):
    '''expresion : expresion OR expresion
                  | expresion AND expresion
                  | NOT expresion'''
    if t[2] == '||':    
        t[0] = Logica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_logicos.OR)
    elif t[2] == '&&': 
        t[0] = Logica(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_logicos.AND)
    if t[1] == '!':
        t[0] = Logica(t.lineno(1), find_column(input, t.slice[1]), t[2], None, tipos_logicos.NOT)

#---------------EXPRESIONES RELACIONALES ----------------------
def p_expresion_relacional(t):
    '''expresion : expresion MENOR IGUAL expresion
                  | expresion MAYOR IGUAL expresion
                  | expresion IGUAL IGUAL expresion
                  | expresion NOT IGUAL expresion
                  | expresion MENOR expresion
                  | expresion MAYOR expresion'''
    if t[3] == '=':
        if t[2] == '<':
            t[0] = Relacional(t.lineno(1), find_column(input, t.slice[2]), t[1], t[4], tipos_relacional.MENORIGUAL)
        elif t[2] == '>':
            t[0] = Relacional(t.lineno(1), find_column(input, t.slice[2]), t[1], t[4], tipos_relacional.MAYORIGUAL)
        elif t[2] == '=':
            t[0] = Relacional(t.lineno(1), find_column(input, t.slice[2]), t[1], t[4], tipos_relacional.IGUALACION)
        elif t[2] == '!':
            t[0] = Relacional(t.lineno(1), find_column(input, t.slice[2]), t[1], t[4], tipos_relacional.DIFERENCIACION)
    elif t[2] == '<':
        t[0] = Relacional(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_relacional.MENORQUE)
    elif t[2] == '>':
        t[0] = Relacional(t.lineno(1), find_column(input, t.slice[2]), t[1], t[3], tipos_relacional.MAYORQUE)

def p_expresion_nativas_logaritmo(t):
    '''expresion   : LOGARITMO PARIZQ expresion COMA expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[5], t[3], tipos_nativas.LOGARITMO)

def p_expresion_nativas_logaritmo10(t):
    ''' expresion   : LOGARITMO10 PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.LOGARITMO10)

def p_expresion_nativas_seno(t):
    ''' expresion   : SENO PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.SENO)

def p_expresion_nativas_coseno(t):
    ''' expresion   : COSENO PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.COSENO)

def p_expresion_nativas_tangente(t):
    ''' expresion   : TANGENTE PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.TANGENTE)

def p_expresion_nativas_raizcuadrada(t):
    ''' expresion   : RAIZCUADRADA PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.RAIZCUADRADA)

def p_expresion_nativas_uppercase(t):
    ''' expresion   : UPPERCASE PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.UPPERCASE)

def p_expresion_nativas_lowercase(t):
    ''' expresion   : LOWERCASE PARIZQ expresion PARDER'''
    t[0] = Nativas(t.lineno(1), find_column(input, t.slice[1]), t[3], None, tipos_nativas.LOWERCASE)

def p_expresion_FUNCION_NATIVA(t):
    ''' expresion   : RPARSE PARIZQ tipodatos COMA expresion PARDER
                    | RTRUNC PARIZQ tipodatos COMA expresion PARDER
                    | RFLOAT PARIZQ expresion PARDER
                    | RSTRING PARIZQ expresion PARDER
                    | RTYPEOF PARIZQ expresion PARDER'''
    if t[1] == "parse":
        t[0] = FuncionNativa(t.lineno(1), find_column(input, t.slice[1]), t[3], t[5], tipos_funcionnativa.PARSE)
    elif t[1] == "trunc":
        t[0] = FuncionNativa(t.lineno(1), find_column(input, t.slice[1]), t[3], t[5], tipos_funcionnativa.TRUNC)
    elif t[1] == "float":
        t[0] = FuncionNativa(t.lineno(1), find_column(input, t.slice[1]), None, t[3], tipos_funcionnativa.FLOAT)
    elif t[1] == "string":
        t[0] = FuncionNativa(t.lineno(1), find_column(input, t.slice[1]), None, t[3], tipos_funcionnativa.STRING)
    elif t[1] == "typeof":
        t[0] = FuncionNativa(t.lineno(1), find_column(input, t.slice[1]), None, t[3], tipos_funcionnativa.TYPEOF)

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[1]), t[2], None, tipos_Aritmetica.MENOSUNARIO)

def p_expresion_PARENTESIS(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

#--------------- ARREGLOS ------------
def p_expresion_arreglo(t):
    'expresion : CORIZQ expresion_arreglo CORDER'
    t[0] = Primitivo(Tipo(tipos.ARREGLO), t.lineno(1), find_column(input, t.slice[1]), t[2])

def p_expresion_arreglo_lista(t):
    'expresion_arreglo    : expresion_arreglo COMA expresion'
    if t[2] != None:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_expresion_arreglo_lista1(t):
    'expresion_arreglo   : expresion '
    if t[1] != None:
        t[0] = []
        t[0].append(t[1])
    else:
        t[0] = []

#_--------------------------------

def p_expresion_entero(t):
    'expresion    : ENTERO'
    t[0] = Primitivo(Tipo(tipos.ENTERO), t.lineno(1), find_column(input, t.slice[1]), int(t[1]))

def p_expresion_decimal(t):
    'expresion    : DECIMAL'
    t[0] = Primitivo(Tipo(tipos.DECIMAL), t.lineno(1), find_column(input, t.slice[1]), float(t[1]))

def p_expresion_cadena(t):
    'expresion    : CADENA'
    t[0] = Primitivo(Tipo(tipos.CADENA), t.lineno(1), find_column(input, t.slice[1]), str(t[1]) )

def p_expresion_true(t):
    'expresion    : RTRUE'
    t[0] = Primitivo(Tipo(tipos.BOOLEANO), t.lineno(1), find_column(input, t.slice[1]), True )

def p_expresion_false(t):
    'expresion    : RFALSE'
    t[0] = Primitivo(Tipo(tipos.BOOLEANO), t.lineno(1), find_column(input, t.slice[1]), False )

def p_expresion_caracter(t):
    'expresion    : CARACTER'
    t[0] = Primitivo(Tipo(tipos.CARACTER), t.lineno(1), find_column(input, t.slice[1]), t[1] )

def p_expresion_ID(t):
    'expresion    : ID'
    t[0] = Variable(t.lineno(1), find_column(input, t.slice[1]), t[1])




import ply.yacc as yacc
parser = yacc.yacc()


'''f = open("entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)
ast = Arbol(parser.parse(input))
tabla = TablaSimbolos()
ast.setTablaSimbolos(tabla)
ast.setGlobal(tabla)
print(str(ast.getInstrucciones()))
if ast.getInstrucciones()[0][0] != None:
    for i in ast.getInstrucciones()[0]:
        print(str(i))
        i.interpretar(ast, tabla)


    print("\nCONSOLA UPDATE:"+str(ast.getConsola()))

'''


def parse(inp):
    global errores
    global lexer
    global parser
    global input
    input = inp
    ast = Arbol(parser.parse(input))
    tabla = TablaSimbolos()
    ast.setTablaSimbolos(tabla)
    ast.setGlobal(tabla)
    print("----contador--")
    print(str(ast.getInstrucciones()))
    if ast.getInstrucciones()[0] != None:
        for i in ast.getInstrucciones():
            #print(str(i))
            i.interpretar(ast, tabla)

        print("\nCONSOLA UPDATE:"+str(ast.getConsola()))

    return ast

