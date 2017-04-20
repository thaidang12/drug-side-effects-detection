from estimate import *
from sets import Set
import operator

class pruning:

	def __init__(self):
		self.p = estimate()
		return

	def prun(self, seqlist, prun_prop):
		score = {}
		for seq in seqlist:
			score[','.join(seq)] = self.p.obs_chain(seq, base=2)
		x = sorted(score.items(), key = operator.itemgetter(1))
		i = int(len(x) * prun_prop)
		x = x[i:]
		return [item[0].split(',') for item in x]


	def update(self, seq_list, elements, prun_prop = 0.95):
		result = []
		elements = [element.split('#') for element in elements]
		if seq_list is None:
			return elements
		else:
			for (seq, element) in [(seq, element) for seq in seq_list for element in elements]:
				result.append(seq + element)
			result = self.prun(result, prun_prop)
			return result


	def create_seq(self, elements):
		seq_list = None
		for item in elements:
			seq_list = self.update(seq_list, item)
		return seq_list


