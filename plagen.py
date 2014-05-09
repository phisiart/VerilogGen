# -*- coding: utf-8 -*-

from parse import *

ast = parser.parse(data)
#print ast

name = ast[1]
print "Module name =", name

inputs = {}
for t_inputvar in ast[2]:
    if t_inputvar[1] == 0:
        inputvar = (t_inputvar[0], 1)
    else:
        inputvar = t_inputvar
    print "Input variable name =", inputvar[0], ", length =", inputvar[1]
    