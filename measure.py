from io import *

class association:

	def __init__(self):
		self.io = io()
		self.drug2obs = self.load_data('data/drug2obs.txt')
		self.drug = self.load_data('data/drug.txt')
		self.obs = self.load_data('data/obs.txt')
		return


	def load_data(self, infile):
		data = {}
		lines = self.io.read_lines(infile)
		lines = [line.split(',') for line in lines]
		lines = [(item[0], int(item[1])) for item in lines]
		for item in lines:
			data[item[0]] = item[1] * 1.0/10808
		return data

	def rr(self, drug, effect):
		a = self.drug2obs.get(drug + '->' + effect)
		b = self.drug.get(drug)
		c = self.obs.get(effect)
		if a is None:
			return 0.0
		elif b is None or c is None:
			return -99999
		else:
			return a * 1.0/(b * c)

	def conf(self, drug, effect):
		a = self.drug2obs.get(drug + '->' + effect)
		b = self.drug.get(drug)
		if a is None:
			return 0.0
		elif b is None:
			return -99999
		else:
			return a * 1.0/b

	def lev(self, drug, effect):
		a = self.drug2obs.get(drug + '->' + effect)
		b = self.drug.get(drug)
		c = self.obs.get(effect)
		if a is None or b is None or c is None:
			return None
		else:
			return a - b * c


