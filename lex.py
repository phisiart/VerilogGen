# -*- coding: utf-8 -*-
import ply.lex as lex

reserved = {
    'input' : 'INPUT',
    'output' : 'OUTPUT',
    'rules' : 'RULES',
}
# List of token names.   This is always required
# token 列表的名字一定要叫 tokens
tokens = [
    'IDENTIFIER',   # Identifiers
    'LBRACE',       # {
    'RBRACE',       # }
    'LSQUARE',      # [
    'RSQUARE',      # ]
    'NUMBER',       # number
    'COMMA',        # ,
    'COLON',        # :
    'SEMICOLON',    # ;
    'EQUAL',        # =
    'ARROW',        # ->
] + list(reserved.values())

# Regular expression rules for simple tokens
# 这些定义一定要用 t_ 前缀加上之前定义的 token 名
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_EQUAL = r'\='
t_ARROW = r'\-\>'

# 有的 token 也可以被定义为函数，参数为识别出来的 token，返回值还是 token

def t_NUMBER(t):
    r'[0-9][0-9a-zA-Z]*'
    # t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()

data = '''
ALUControl {
input:
    alu_op;
    funct[6];
output:
    alu_ctrl[4];
rules:
    alu_op = 0 -> alu_ctrl = 3;
    alu_op = 1 -> alu_ctrl = 2;
    alu_op = 2, funct = 32 -> alu_ctrl = 2;
    alu_op = 2, funct = 34 -> alu_ctrl = 6;
    alu_op = 2, funct = 36 -> alu_ctrl = 0;
    alu_op = 2, funct = 37 -> alu_ctrl = 1;
    alu_op = 2, funct = 42 -> alu_ctrl = 7;
}
'''

data = '''
Decoder {
input:
    A[3];
output:
    D[8];
rules:
    A = 0 -> D = 1;
    A = 1 -> D = 2;
    A = 2 -> D = 4;
    A = 3 -> D = 8;
    A = 4 -> D = 16;
    A = 5 -> D = 32;
    A = 6 -> D = 64;
    A = 7 -> D = 128;
}
'''

data = '''
DigitalDisplay {
input:
    x[4];
output:
    y[7];
rules:
    x=0->y=1;
    x=1->y=79;
    x=2->y=18;
    x=3->y=6;
    x=4->y=76;
    x=5->y=36;
    x=6->y=32;
    x=7->y=15;
    x=8->y=0;
    x=9->y=4;
    x=10->y=8;
    x=11->y=96;
    x=12->y=49;
    x=13->y=66;
    x=14->y=48;
    x=15->y=56;
}
'''

# data = '''
# Adder {
# input:
#     A;
#     B;
# output:
#     CarryOut;
#     S;
# rules:
#     A = 0, B = 0 -> S = 0, CarryOut = 0;
#     A = 0, B = 1 -> S = 1, CarryOut = 0;
#     A = 1, B = 0 -> S = 1, CarryOut = 0;
#     A = 1, B = 1 -> S = 0, CarryOut = 1;
# }
# '''

# data = '''
# Test {
# input:
#     A;
# output:
#     B;
# rules:
#     A = 0 -> B = 1;    
# }
# '''

if __name__ == 'main':
    lexer.input(data)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        print((tok.type, tok.value))
        #print tok.value
