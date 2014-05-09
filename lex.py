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
    alu_op = 1 -> alu_ctrl = 0b110;
    alu_op = 2, funct = 32 -> alu_ctrl = 2;
    alu_op = 2, funct = 34 -> alu_ctrl = 6;
    alu_op = 2, funct = 36 -> alu_ctrl = 0;
    alu_op = 2, funct = 37 -> alu_ctrl = 1;
    alu_op = 2, funct = 42 -> alu_ctrl = 7;
}
'''

if __name__ == 'main':
    lexer.input(data)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        print (tok.type, tok.value)
        #print tok.value
