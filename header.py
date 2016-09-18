'''
makeLispincHeader produces a header file of compiled 
code ready for inclusion in the lispinc interpreter 
(github.com/nickdrozd/lispinc). It will write to the 
file comp_code.h, and will overwrite it if such a file 
already exists.
'''


from parse import parse
from compileDisp import compileDisp
from instructions import statements
from keywords import *
from labels import labels
from library import library


def makeLispincHeader(exprSeq):
	comp_code = open('comp_code.h', 'w')

	heading = (
'''/* 
	This code is compiler-generated! 
	It may be ugly, but it sure is fast!
	Can you figure out how it works?
	
	https://github.com/nickdrozd/Lisp-C-Compyler
*/

#ifndef COMP_CODE_GUARD
#define COMP_CODE_GUARD

#define COMPILED_CODE_BODY \\
''')

	comp_code.write(heading)
	for expr in exprSeq:
		parsed = parse(expr)
		compiled = compileDisp(parsed)
		code = statements(compiled)

		for line in code:
			comp_code.write(line + ' \\' + '\n')
	comp_code.write('goto DONE;')
	
	comp_code.write('\n\n')

	def isLastLabel(label):
		labelsLen = len(labels)
		labelIndex = labels.index(label)
		return labelIndex == labelsLen - 1

	comp_code.write('#define COMP_CONT(REG) \\' + '\n')
	for label in labels:
		lastLabel = isLastLabel(label)
		labelCheck = (
			'if (GETLABEL(REG) == _' + label + 
			') ' + 'goto ' + label + ';' +
			('' if lastLabel else ' \\' + '\n')
		)
		comp_code.write(labelCheck)

	comp_code.write('\n\n')

	comp_code.write('#define ALL_COMPILED_LABELS \\' + '\n')
	for label in labels:
		lastLabel = isLastLabel(label)
		listedLabel = (
			'_' + label + 
			('' if lastLabel else ', \\' + '\n')
		)
		comp_code.write(listedLabel)

	comp_code.write('\n\n' + '#endif' + '\n')




makeLispincHeader(library)
