from corpus import *
from measure import *
from chi_square import *
from pruning import *
import glob
import math

oo = -99999.0
class run_model:

	def __init__(self):
		print 'Running Medication Therapy Progress-based Model...'
		self.c = corpus()
		self.assoc = association()
		self.chisquare = chi_square()
		self.pr = pruning()
		self.io = io()
		self.tagdata = self.load_tagset('validation/*.txt')
		return

	def load_testset(self, patient_file):
		return self.c.load_corpus(patient_file)

	def load_tagset(self, path):
		tagdata = {}
		files = glob.glob(path)
		for f in files:
			lines = self.io.read_lines(f)
			drug = lines[0].replace('<Drug>', '').replace('</Drug>', '')
			lines = [lines[i].split(' ') for i in range(1, len(lines))]
			lines = [' '.join(item[:len(item)-1]) + '[e]' for item in lines if item[len(item) - 1] == '1']
			tagdata[drug] = lines
		return tagdata


	def update_pairs(self, curdict, pairs):
		for pair in pairs:
			if not curdict.has_key(pair[0]):
				curdict[pair[0]] = [pair[1]]
			else:
				exist = curdict.get(pair[0])
				exist.append(pair[1])
				curdict[pair[0]] = exist
		return curdict


	def update_dict(self, curdict, newdict):
		for key in newdict.keys():
			if not curdict.has_key(key):
				curdict[key] = newdict.get(key)
			else:
				exist = curdict.get(key)
				exist += newdict.get(key)
				curdict[key] = exist
		return curdict


	def get_category(self, term):
		return term[term.index('[')+1: term.index(']')]


	def his2drug_bigram(self, x):
		y = [self.pr.p.his2drug_chain(item, base=2) for item in x]
		if len(y) == 0:
			return 0.0
		else:
			return max(y)

	def his2drug_trigram(self, x):
		y = [self.pr.p.his2drug_chain(item, base=3) for item in x]
		if len(y) == 0:
			return 0.0
		else:
			return max(y)


	def process_hadm(self, hadm, his_length):
		score = {}
		for i in range(len(hadm)):
			if i >= his_length:
				history = hadm[i - his_length:i]
			else:
				history = hadm[:i]
			history = [item[2] for item in history]
			pairs = [(drug, effect) for drug in hadm[i][1] for effect in hadm[i][2] if self.get_category(effect) == 'e']
			if len(history) == 0:
				pairs = [('->'.join(pair), self.assoc.conf(pair[0], pair[1])) for pair in pairs]
				score = self.update_pairs(score, pairs)
			else:
				h = self.pr.create_seq(history)
				for i in range(len(pairs)):
					h2d = [item + [pairs[i][0]] for item in h]
					x = self.assoc.conf(pairs[i][0], pairs[i][1])
					y = self.his2drug_bigram(h2d)
					pairs[i] = ('->'.join(pairs[i]), x * y)
				score = self.update_pairs(score, pairs)
		return score

	def hadm_pooling(self, path, his_length, top = 10):
		result = {}
		files = glob.glob(path)
		# print 'history length = ', his_length
		for f in files:
			data = self.load_testset(f)
			for hadm in data:
				pair_score = self.process_hadm(hadm, his_length=his_length)
				result = self.update_dict(result, pair_score)

		for key in result.keys():
			result[key] = max(result.get(key))
		
		tuples = []
		for key in result.keys():
			tokens = key.split('->')
			tuples.append( (tokens[0], (tokens[1], result.get(key))) )

		# get drug in tagged set
		tuples = [item for item in tuples if self.tagdata.has_key(item[0])]

		# group by drugs
		groups = self.group_by_drug(tuples)

		# retrieve likely effects
		for drug in groups.keys():
			groups[drug] = self.rank(groups.get(drug), top = top)

		print 'history length: ', his_length, 'accuracy: ', self.precision(groups)

		return self.precision(groups)

	def run_mtpm(self, path, maxlength):
		accuracy = []
		for l in range(1, maxlength + 1):
			p = self.hadm_pooling(path, l)
			accuracy.append(p)
		return accuracy

	def topOfSelection(self, path, length, maxtop):
		accuracy = []
		for i in range (10, maxtop+1):
			p = self.hadm_pooling(path, length, i)
			accuracy.append(p)
		return accuracy

	def group_by_drug(self, tuples):
		groups = {}
		for item in tuples:
			if not groups.has_key(item[0]):
				alist = []
				alist.append(item[1])
				groups[item[0]] = alist
			else:
				exist = groups.get(item[0])
				exist.append(item[1])
				groups[item[0]] = exist
		return groups


	def rank(self, effect_score, top = 10):
		x = {}
		for item in effect_score:
			x[item[0]] = item[1]
		sorted_x = sorted(x.items(), key=operator.itemgetter(1))
		l = len(sorted_x)
		return sorted_x[l - top:]

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

	


