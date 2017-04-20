from io import *

class corpus:

	def __init__(self):
		self.io = io()
		self.effects = self.load_lex('effect.dict.txt', '[e]')
		self.diseases = self.load_lex('disease.dict.txt', '[d]')
		return

	def load_lex(self, lex_file, suffix):
		lines = self.io.read_lines(lex_file)
		lines = [line + suffix for line in lines]
		return Set(lines)

	def inlex(self, terms):
		return [term for term in terms if term in self.effects or term in self.diseases]


	def checklex(self, data):
		for i in range(len(data)):
			data[i] = [(data[i][j][0], data[i][j][1], self.inlex(data[i][j][2])) for j in range (len(data[i]))]
		return data

	def not_empty(self, inputlist):
		inputlist = [item for item in inputlist if item != '']
		return len(inputlist) > 0

	def get_tuple(self, lines):
		tuples = [(line.split('-/-')[0], line.split('-/-')[1].split(','), line.split('-/-')[2].split(',')) for line in lines]
		tuples = [item for item in tuples if self.not_empty(item[1]) is True and self.not_empty(item[2]) is True]
		return tuples

	def load_corpus(self, corpus_file):
		lines = self.io.read_lines(corpus_file)
		begins = [i for i in range(len(lines)) if '<begin>' in lines[i]]
		ends = [i for i in range(len(lines)) if '<end>' in lines[i]]

		corpus = [lines[i+1: j] for i, j in zip(begins, ends)]
		corpus = [self.get_tuple(group) for group in corpus]
		corpus = self.checklex(corpus)
		return corpus

