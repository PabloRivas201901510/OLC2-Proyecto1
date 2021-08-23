
import os
import re
import sys
from server.Excepciones.Excepcion import Excepcion
from server.Expresiones.Primitivo import Primitivo
from server.TablaDeSimbolos.Tipo import Tipo, tipos
from server.TablaDeSimbolos.TablaSimbolos import TablaSimbolos
from server.TablaDeSimbolos.Arbol import Arbol
from server.Abstract.instruccion import instruccion

from server.Instrucciones.println import println
from server.Instrucciones.print_ import print_
from server.Expresiones.Aritmetica import Aritmetica, tipos_Aritmetica
from server.Expresiones.Nativas import Nativas, tipos_nativas

sys.setrecursionlimit(3000)
errores = []
tokens = [
    'RPRINTLN',
    'RPRINT',
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
    'PTCOMA',
    'CADENA',
    'LOGARITMO10',
    'LOGARITMO',
    'COMA',
    'SENO',
    'COSENO',
    'TANGENTE',
    'RAIZCUADRADA',
    'UPPERCASE',
    'LOWERCASE'
]

# Tokens
t_RPRINTLN = r'println'
t_RPRINT = r'print'
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_ELEVADO = r'\^'
t_MODULO = r'\%'
t_PTCOMA = r';'
t_LOGARITMO10 = r'log10'
t_LOGARITMO = r'log'
t_COMA = r'\,'
t_SENO = r'sin'
t_COSENO = r'cos'
t_TANGENTE = r'tan'
t_RAIZCUADRADA = r'sqrt'
t_UPPERCASE = r'uppercase'
t_LOWERCASE = r'lowercase'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
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

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t


# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex()
lex.lex(reflags=re.IGNORECASE)

# Asociación de operadores y precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'UMENOS'),
)


# Definición de la gramática
def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t):
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_lista1(t):
    'instrucciones    : instruccion '
    t[0] = []
    t[0].append(t[1])

#////////////////////////////////////// INSTRUCCIONES /////////////////////////////////7

def p_imprimirln(t) :
    'instruccion     : RPRINTLN PARIZQ expresion PARDER PTCOMA'
    t[0] = println(t[3], t.lineno(1), find_column(input, t.slice[1]))

def p_imprimir(t) :
    'instruccion     : RPRINT PARIZQ expresion PARDER PTCOMA'
    t[0] = print_(t[3], t.lineno(1), find_column(input, t.slice[1]))


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


def p_expresion_nativas_logaritmo(t):
    'expresion   : LOGARITMO PARIZQ expresion COMA expresion PARDER'
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

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = Aritmetica(t.lineno(1), find_column(input, t.slice[1]), t[2], None, tipos_Aritmetica.MENOSUNARIO)


def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_entero(t):
    'expresion    : ENTERO'
    t[0] = Primitivo(Tipo(tipos.ENTERO), t.lineno(1), find_column(input, t.slice[1]), int(t[1]))

def p_expresion_decimal(t):
    'expresion    : DECIMAL'
    t[0] = Primitivo(Tipo(tipos.DECIMAL), t.lineno(1), find_column(input, t.slice[1]), float(t[1]))

def p_expresion_cadena(t):
    'expresion    : CADENA'
    t[0] = Primitivo(Tipo(tipos.CADENA), t.lineno(1), find_column(input, t.slice[1]), str(t[1]) )


def p_error(t):
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc

parser = yacc.yacc()

f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)

ast = Arbol(parser.parse(input))
tabla = TablaSimbolos()
ast.setTablaSimbolos(tabla)
ast.setGlobal(tabla)
#print(str(ast.getInstrucciones()))

for i in ast.getInstrucciones()[0]:
    #print(str(i))
    i.interpretar(ast, tabla)


print("\nCONSOLA UPDATE:"+str(ast.getConsola()))



    

