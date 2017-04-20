from io import *


N = 10808
oo = -99999

class estimate:

	def __init__(self):
		self.io = io()
		print 'load data...'
		print 'data/obs.txt'
		self.effect_unigram = self.load_data('data/obs.txt')
		print 'data/obs.bigram.txt'
		self.effect_bigram = self.load_data('data/obs.bigram.txt')
		# print 'data/obs.trigram.txt'
		# self.effect_trigram = self.load_data('data/obs.trigram.txt')
		print 'data/history2drug.bigram.txt'
		self.effect2drug_bigram = self.load_data('data/history2drug.bigram.txt')
		# print 'data/history2drug.trigram.txt'
		# self.effect2drug_trigram = self.load_data('data/history2drug.trigram.txt')
		return

	def load_data(self, infile):
		lines = self.io.read_lines(infile)
		lines = [line.split(',') for line in lines]
		data = {}
		for item in lines:
			data[item[0]] = float(item[1])
		return data

	def prod(self, x):
		result = 1.0
		for item in x:
			result *= item
		return result


	def bigram(self, tokens, opt = 'obs_seq'):
		if len(tokens) == 2:
			if opt == 'obs_seq':
				a = self.effect_bigram.get('->'.join(tokens))
				b = self.effect_unigram.get(tokens[0])
				# print a, b
				if b is None:
					return oo
				elif a is None:
					return 0.0
				else:
					return a*1.0/b
			elif opt == 'his2drug':
				a = self.effect2drug_bigram.get('->'.join(tokens))
				b = self.effect_unigram.get(tokens[0])
				# print a, b
				if b is None:
					return oo
				elif a is None:
					return 0.0
				else:
					return a*1.0/b
		else:
			return None



	def trigram(self, tokens, opt='obs_seq'):
		if len(tokens) == 3:
			if opt == 'obs_seq':
				a = self.effect_trigram.get('->'.join(tokens))
				b = self.effect_bigram.get('->'.join(tokens[:2]))
				if b is None:
					return oo
				elif a is None:
					return 0.0
				else:
					return a * 1.0/b
			elif opt == 'his2drug':
				a = self.effect2drug_trigram.get('->'.join(tokens))
				b = self.effect_bigram.get('->'.join(tokens[:2]))
				if b is None:
					return oo
				elif a is None:
					return 0.0
				else:
					return a * 1.0 / b
		else:
			return None


	def obs_chain(self, x, base = 3):
		if base == 3:
			return self.prod([self.trigram([x[i], x[i+1], x[i+2]], opt = 'obs_seq') for i in range(len(x)) if i+2 < len(x)])
		elif base == 2:
			return self.prod([self.bigram([x[i], x[i+1]], opt = 'obs_seq') for i in range(len(x)) if i+1 < len(x)])
		else:
			return None


	def his2drug_chain(self, x, base = 3):
		l = len(x)
		if base == 3:
			return self.obs_chain(x[:l-1], base = 3) * self.trigram([x[l-3], x[l-2], x[l-1]], opt = 'his2drug')
		elif base == 2:
			return self.obs_chain(x[:l-1], base = 2) * self.bigram([x[l-2], x[l-1]], opt = 'his2drug')
		else:
			return None


