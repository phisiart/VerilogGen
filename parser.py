# -*- coding: utf-8 -*-

import ply.yacc as yacc

from lex import tokens

def p_program(p):
    'program : IDENTIFIER LBRACE INPUT COLON input_list OUTPUT COLON output_list RULES COLON rules_list RBRACE'
    p[0] = ('program', p[1], p[5], p[8], p[11])
    
def p_input_list(p):
    '''input_list : input_list input
                  | input'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
        
def p_dispatch_1(p):
    '''dispatch : IDENTIFIER LSQUARE NUMBER RSQUARE'''
    p[0] = (p[1], p[3])
    
def p_dispatch_2(p):
    '''dispatch : IDENTIFIER'''
    p[0] = (p[1], -1)
    
def p_input(p):
    '''input : dispatch SEMICOLON'''
    p[0] = p[1]
    
#def p_input_1(p):
#    '''input : IDENTIFIER LSQUARE NUMBER RSQUARE SEMICOLON'''
#    p[0] = (p[1], p[3])
#    
#def p_input_2(p):
#    '''input : IDENTIFIER SEMICOLON'''
#    p[0] = (p[1], 1)
    
def p_output_list(p):
    '''output_list : output_list output
                   | output'''
                   
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
        
#def p_output_1(p):
#    '''output : IDENTIFIER LSQUARE NUMBER RSQUARE SEMICOLON'''
#    p[0] = (p[1], p[3])
#    
#def p_output_2(p):
#    '''output : IDENTIFIER SEMICOLON'''
#    p[0] = (p[1], 1)
        
def p_output(p):
    '''output : dispatch SEMICOLON'''
    p[0] = p[1]
    
def p_rules_list(p):
    '''rules_list : rules_list rule
                  | rule'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
        
def p_rule(p):
    '''rule : spec ARROW spec SEMICOLON'''
    p[0] = (p[1], p[3])
    
def p_spec(p):
    '''spec : spec COMMA assign
            | assign'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_assign(p):
    '''assign : dispatch EQUAL NUMBER'''
    p[0] = (p[1], p[3])
    
def p_error(p):
    print('error!')

# Build parser.
parser = yacc.yacc()


if __name__ == '__main__':
    data = '''
    Test {
    input:
        A;
    output:
        B[2];
    rules:
        A = 0 -> B = 1;    
    }
    '''
    print(parser.parse(data))