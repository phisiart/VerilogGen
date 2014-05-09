# -*- coding: utf-8 -*-

import sys
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

    if inputvar[0] in inputs:
        print 'Error! Input \'%s\' has already been defined.' % inputvar[0]
        sys.exit(1)

    inputs[inputvar[0]] = int(inputvar[1])

print 'Inputs are:'
print inputs

outputs = {}
for t_outputvar in ast[3]:

    if t_outputvar[1] == 0:
        outputvar = (t_outputvar[0], 1)
    else:
        outputvar = t_outputvar

    if outputvar[0] in inputs:
        print 'Error! Trying to add output \'%s\' but it has already been defined as input.' % outputvar[0]
        sys.exit(1)

    if outputvar[0] in outputs:
        print 'Error! Output \'%s\' has already been defined.' % inputvar[0]
        sys.exit(1)

    outputs[outputvar[0]] = int(outputvar[1])

print 'Outputs are:'
print inputs

for rule in ast[4]:
    print rule
