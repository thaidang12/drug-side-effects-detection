from io import *


class chi_square:
	
	def __init__(self):
		self.io = io()
		self.drug2obs = self.load_data('data/drug2obs.txt')
		self.drug = self.load_data('data/drug.txt')
		self.obs = self.load_data('data/obs.txt')
		self.total_pt = 10808
		return

	def load_data(self, infile):
		data = {}
		lines = self.io.read_lines(infile)
		lines = [line.split(',') for line in lines]
		lines = [(item[0], int(item[1])) for item in lines]
		for item in lines:
			data[item[0]] = item[1]
		return data

	def chi(self, drug, effect):
		if self.drug2obs.get(drug + '->' + effect) is None or self.drug.get(drug) is None or self.obs.get(effect) is None:
			return None
		else:
			a = self.drug2obs.get(drug + '->' + effect)
			b = self.obs.get(effect) - a
			c = self.drug.get(drug) - a
			d = self.total_pt - a - b -c

			fa = (a + b) * (a + c) * 1.0 / self.total_pt
			fb = (a + b) * (b + d) * 1.0 / self.total_pt
			fc = (a + c) * (c + d) * 1.0 / self.total_pt
			fd = (d + c) * (d + b) * 1.0 / self.total_pt

			if fa == 0 or fb == 0 or fc == 0 or fd == 0:
				return -999999999
			else:
				return (a - fa)**2/fa + (b - fb)**2/fb + (c - fc)**2/fc + (d - fd)**2/fd


		
