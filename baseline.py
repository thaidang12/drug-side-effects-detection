from corpus import *
from extract import *
from io import *
import glob
from sets import Set
from measure import *
from chi_square import *
import operator

class run_baseline:

	def __init__(self):
		self.io = io()
		self.c = corpus()
		self.ext = extract()
		self.assoc = association()
		self.chi_square = chi_square()

		self.tagdata = self.load_tagset('validation/*.txt')
		self.pairs = self.get_pairs('test_sample/*.txt')
		self.pairs = [item.split('->') for item in self.pairs]
		return

	def load_tagset(self, path):
		tag_data = {}
		files = glob.glob(path)
		for f in files:
			lines = self.io.read_lines(f)
			drug = lines[0].replace('<Drug>', '').replace('</Drug>', '')
			lines = [lines[i].split(' ') for i in range(1, len(lines))]
			lines = [' '.join(item[:len(item)-1]) + '[e]' for item in lines if item[len(item) - 1] == '1']
			tag_data[drug] = lines
		return tag_data


	def get_pairs(self, path):
		total_pairs = []
		files = glob.glob(path)
		for f in files:
			pairs = self.ext.bipartite_graph(f).keys()
			total_pairs += pairs
		return list(Set(total_pairs))


	def rank(self, effect_score, top = 10):
		x = {}
		for item in effect_score:
			x[item[0]] = item[1]
		sorted_x = sorted(x.items(), key=operator.itemgetter(1))
		l = len(sorted_x)
		return sorted_x[l-top:]


	def run(self, measure_type, top = 10):
		# get pairs of considering drugs
		consider = [item for item in self.pairs if self.tagdata.has_key(item[0])]
		# group by drugs
		groups = {}
		for item in consider:
			if not groups.has_key(item[0]):
				groups[item[0]] = item[1].split('#')
			else:
				exist = groups.get(item[0])
				exist.append(item[1])
				groups[item[0]] = exist

		# measure strength of rules
		if measure_type == 'rr':
			for drug in groups.keys():
				effects = groups.get(drug)
				effects = [(effect, self.assoc.rr(drug, effect)) for effect in effects]
				effects = self.rank(effects, top)
				groups[drug] = effects
			print 'RR accuracy: ', self.precision(groups)
			return self.precision(groups)
		elif measure_type == 'conf':
			for drug in groups.keys():
				effects = groups.get(drug)
				effects = [(effect, self.assoc.conf(drug, effect)) for effect in effects]
				effects = self.rank(effects, top)
				groups[drug] = effects
			print 'conf accuracy', self.precision(groups)
			return self.precision(groups)
		elif measure_type == 'lev':
			for drug in groups.keys():
				effects = groups.get(drug)
				effects = [(effect, self.assoc.lev(drug, effect)) for effect in effects]
				effects = self.rank(effects, top)
				groups[drug] = effects
			print 'lev accuracy', self.precision(groups)
			return self.precision(groups)
		elif measure_type == 'chi':
			for drug in groups.keys():
				effects = groups.get(drug)
				effects = [(effect, self.chi_square.chi(drug, effect)) for effect in effects]
				effects = self.rank(effects, top)
				groups[drug] = effects
			print 'chi square accuracy:', self.precision(groups)
			return self.precision(groups)
		return

	def topOfSelection(self, measure_type, maxtop):
		accuracy = []
		for i in range(10, maxtop+1):
			p = self.run(measure_type, i)
			accuracy.append(p)
		return accuracy

	def precision(self, retrival):
		count = 0
		total = 0
		for drug in retrival.keys():
			retrival_effects = retrival.get(drug)
			retrival_effects = [item[0] for item in retrival_effects]
			real_effects = self.tagdata.get(drug)
			total += len(retrival_effects)
			if real_effects is not None:
				for item in retrival_effects:
					if item in Set(real_effects):
						count += 1
		return count * 1.0/total


