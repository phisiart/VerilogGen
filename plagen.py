# -*- coding: utf-8 -*-

import sys, os
from parse import *

ast = parser.parse(data)
#print ast

plastr = ''

name = ast[1]
print('Module name = %s' % name)
print()

inputs = {}
plastr += '.ilb '
for t_inputvar in ast[2]:

    if t_inputvar[1] == -1:
        inputvar = (t_inputvar[0], 1)
        plastr += inputvar[0] + ' '
    else:
        inputvar = t_inputvar
        for offset in range(0, int(inputvar[1])):
            plastr += inputvar[0] + '[' + str(offset) + ']' + ' '

    if inputvar[0] in inputs:
        print('Error! Input \'%s\' has already been defined.' % inputvar[0])
        sys.exit(1)

    inputs[inputvar[0]] = int(inputvar[1])

print('Inputs are:')
for t_input in inputs:
    print('  %s[%d]' % (t_input, inputs[t_input]))
print()

outputs = {}
plastr += '\n.ob '
for t_outputvar in ast[3]:

    if t_outputvar[1] == -1:
        outputvar = (t_outputvar[0], 1)
        plastr += outputvar[0] + ' '
    else:
        outputvar = t_outputvar
        for offset in range(0, int(outputvar[1])):
            plastr += outputvar[0] + '[' + str(offset) + ']' + ' '

    if outputvar[0] in inputs:
        print('Error! Trying to add output \'%s\' but it has already been defined as input.' % outputvar[0])
        sys.exit(1)

    if outputvar[0] in outputs:
        print('Error! Output \'%s\' has already been defined.' % inputvar[0])
        sys.exit(1)

    outputs[outputvar[0]] = int(outputvar[1])

print('Outputs are:')
for t_output in outputs:
    print('  %s[%d]' % (t_output, outputs[t_output]))
print()

input2idx = {}
input_count = 0
for t_input in inputs:
    input2idx[t_input] = input_count
    input_count += inputs[t_input]

print('Input indices:')
for t_input in input2idx:
    print('  %s = %d' % (t_input, input2idx[t_input]))
print()
print('input_count = %d' % input_count)
print()

output2idx = {}
output_count = 0
for t_output in outputs:
    output2idx[t_output] = output_count
    output_count += outputs[t_output]

print('Output indices:')
for t_output in output2idx:
    print('  %s = %d' % (t_output, output2idx[t_output]))
print()
print('input_count = %d' % output_count)
print()

plastr = '.i ' + str(input_count) + '\n.o ' + str(output_count) + '\n.type fr\n' + plastr


class Rule:
    def __init__(self):
        self.inputs = {} # int : str
        self.outputs = {} # int : str

    def InputStr(self):
        ret = ''
        for idx in range(0, input_count):
            if idx in self.inputs:
                ret += str(self.inputs[idx])
            else:
                ret += '-'
        return ret

    def OutputStr(self):
        ret = ''
        for idx in range(0, output_count):
            if idx in self.outputs:
                ret += str(self.outputs[idx])
            else:
                ret += '-'
        return ret

rules = []

for t_rule in ast[4]:
    rule = Rule()

    input_specs = t_rule[0]
    print('Inputs:')
    for input_spec in input_specs:
        var, offset = input_spec[0]
        val = input_spec[1]
        print('  var = %s[%d], val = %s' % (var, offset, val))
        if offset == -1:
            print('    inputs[%s] = %d' % (var, inputs[var]))
            for off in range(0, inputs[var]):
                va = (int(val) & (1 << off)) >> off
                idx = input2idx[var] + off
                print('      idx = %d, var = %d' % (idx, va))
                rule.inputs[idx] = va
                # print(va)
            # print()
        else:
            idx = input2idx[var] + offset
            # val = (int(val) & (1 << offset)) >> offset
            val = int(val != 0)
            rule.inputs[idx] = val
            # print('  idx = %d, val = %d' % (idx, val))
            # print(rule.inputs)

    output_specs = t_rule[1]
    print('Outputs:')
    for output_spec in output_specs:
        var, offset = output_spec[0]
        val = output_spec[1]
        print('  var = %s[%d], val = %s' % (var, offset, val))
        if offset == -1:
            print('    outputs[%s] = %d' % (var, outputs[var]))
            for off in range(0, outputs[var]):
                va = (int(val) & (1 << off)) >> off
                idx = output2idx[var] + off
                print('      idx = %d, var = %d' % (idx, va))
                rule.outputs[idx] = va
                # print(va)
            # print()
        else:
            idx = output2idx[var] + offset
            val = int(val != 0)
            rule.outputs[idx] = val
            # print('  idx = %d, val = %d' % (idx, val))

    # print(rule.inputs)
    # print(rule.outputs)
    # print(rule)
    rules.append(rule)
    print()


print('--------------------------------------------')
for rule in rules:
    # print('Rule:')
    # print(rule.inputs)
    # print(rule.outputs)
    print('%s -> %s' % (rule.InputStr(), rule.OutputStr()))
    plastr += '\n' + rule.InputStr() + ' ' + rule.OutputStr()
    # print(rule)
    # print()

plastr += '\n.e'
print('pla:')
print(plastr)

plafile = open(name + '.in', 'w')
plafile.write(plastr)
plafile.close()

cmd = './espresso.linux -o eqntott ' + name + '.in >' + name + '.out'
os.system(cmd)

print('\nInput:')
print(data)

print('\nOutput:')
verilogfile = 'module ' + name + '(\n'
for inputvar in inputs:
    if inputs[inputvar] == 1:
        verilogfile += '    input wire ' + inputvar + ',\n'
    else:
        verilogfile += '    input wire [' + str(inputs[inputvar] - 1) + ':0] ' + inputvar + ',\n'

for outputvar in outputs:
    if outputs[outputvar] == 1:
        verilogfile += '    output wire ' + outputvar + ',\n'
    else:
        verilogfile += '    output wire [' + str(outputs[outputvar] - 1) + ':0] ' + outputvar + ',\n'

if (verilogfile[-2] == ','):
    verilogfile = verilogfile[:-2] + '\n);\n\n'
else:
    verilogfile += '\n);\n\n'



plafile = open(name + '.out', 'r')
need = True;
for line in plafile:
    line = line.replace('()', '1')
    line = line.replace('= ;', '= 0;')
    if line == '\n':
        # print(line, end='')
        need = True
        pass
    else:
        if need:
            verilogfile += '    assign ' + line
            need = False
        else:
            verilogfile += '              ' + line
        # print(line, end='')

# print('f')
#out = plafile.read()
#print(out)

verilogfile += '\nendmodule\n'
print(verilogfile)