class InstrSeq:
	def __init__(self, needed=[], 
					modified=[], 
					statements=[]):
		self.needed = set(needed)
		self.modified = set(modified)
		self.statements = statements

	def needs(self, reg):
		return reg in self.needed

	def modifies(self, reg):
		return reg in self.modifies

	def tackOn(seq):
		if type(seq) == str:
			statements = [seq]
		elif isinstance(seq, InstrSeq):
			statements
		self.statements += statements


def appendInstrSeqs(*seqs):
	result = InstrSeq()
	for seq in seqs:
		result.needed.update(
			seq.needed.difference(
				result.modified))

		result.modified.update(seq.modified)

		result.statements += seq.statements
	return result

