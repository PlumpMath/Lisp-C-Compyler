from ctext import saveText, restoreText
from linkage import *

class InstrSeq:
	def __init__(self, needed=[], 
					modified=[], 
					statements=[]):
		self.needed = set(needed)
		self.modified = set(modified)
		self.statements = statements

	def __str__(self):
		return '\n'.join(self.statements)

	def needs(self, reg):
		return reg in self.needed

	def modifies(self, reg):
		return reg in self.modified

	# def addReg(regSet, reg):
	# 	try:
	# 		regSet.add(reg)
	# 	except:
	# 		regSet.update(reg)

	def addNeeded(self, reg):
		try:
			self.needed.add(reg)
		except:
			self.needed.update(reg)

	def addModified(self, reg):
		try:
			self.modified.add(reg)
		except:
			self.modified.update(reg)

	def removeModified(self, reg):
		self.modified.remove(reg)

	def addStatements(self, seq):
		statements = _statementsTypeCheck(seq)
		self.statements += statements

	def prependStatement(self, seq):
		statements = _statementsTypeCheck(seq)
		self.statements = statements + self.statements

	def append(self, *seqs):
		for seq in seqs:
			self.addNeeded(seq.needed.difference(self.modified))
			self.addModified(seq.modified)
			self.addStatements(seq.statements)

	def addStackInstrs(self, reg):
		self.statements = (
			[saveText(reg)] + 
			self.statements + 
			[restoreText(reg)]
		)

	def preserveReg(self, reg):
		self.addNeeded(reg)
		self.removeModified(reg)
		self.addStackInstrs(reg)

	def preserving(self, regs, seq):
		for reg in regs:
			if self.modifies(reg) and seq.needs(reg):
				self.preserveReg(reg)
		self.append(seq)


	def endWithLink(self, linkage):
		if linkage == ret:
			instr = [gotoContinueText]
		elif linkage == nex:
			instr = []
		else:
			instr = [gotoText(linkage)]

		needs = [cont] if linkage == ret else []

		instrSeq = InstrSeq(needs, [], instr)

		self.preserving([cont], instrSeq)





def parallelSeqs(*seqs):
	result = InstrSeq()
	for seq in seqs:
		result.addStatements(seq)
		try:
			result.addNeeded(seq.needed)
			result.addModified(seq.modified)
		except:
			pass
	# print(result.statements)
	# return result

def _statementsTypeCheck(seq):
	try:
		statements = seq.statements
	except:			
		if type(seq) == str:
			statements = [seq]
		else:
			statements = seq

	return statements

###

class SaveSeq(InstrSeq):
	def __init__(self, reg):
		super().__init__([reg], [], [saveText(reg)])

class RestoreSeq(InstrSeq):
	def __init__(self, reg):
		super().__init__([], [reg], [restoreText(reg)])

