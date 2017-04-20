from corpus import *
import glob

class extract:


	def __init__(self):
		self.c = corpus()
		return

	def get_category(self, term):
		i = term.index('[')
		j = term.index(']')
		return term[i+1:j]

	def bipartite_graph(self, corpus_file):
		corpus = self.c.load_corpus(corpus_file)
		frequency = {}
		for group in corpus:
			for item in group:
				effects = [element for element in item[2] if self.get_category(element) == 'e']
				pairs = [(drug, effect) for drug in item[1] for effect in effects]
				pairs = ['->'.join(list(pair)) for pair in pairs]
				for pair in pairs:
					if not frequency.has_key(pair):
						frequency[pair] = 1
					else:
						frequency[pair] = frequency.get(pair) + 1
		return frequency

	def get_drug(self, corpus_file):
		corpus = self.c.load_corpus(corpus_file)
		freq = {}
		for group in corpus:
			for item in group:
				drugs = [drug for drug in item[1]]
				for drug in drugs:
					if not freq.has_key(drug):
						freq[drug] = 1
					else:
						freq[drug] = freq.get(drug) + 1
		return freq

	def get_effect(self, corpus_file):
		corpus = self.c.load_corpus(corpus_file)
		freq = {}
		for group in corpus:
			for item in group:
				effects = [effect for effect in item[2]]
				for effect in effects:
					if not freq.has_key(effect):
						freq[effect] = 1
					else:
						freq[effect] = freq.get(effect) + 1
		return freq




