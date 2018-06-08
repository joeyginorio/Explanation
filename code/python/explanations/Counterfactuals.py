# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script uses counterfactuals to build relations between events
	represented by a physics engine.
"""

from Events import Events
from itertools import combinations
from itertools import product

class Counterfactuals():

	def __init__(self, E):
		self.E = E

	# in non-noisy world, search over all counterfactuals that would matter
	# then with that set, simulate 100 times w/ noise
	def sample_counterfactuals(self):

       	# Build a space of counterfactuals (fix this to a smarter search later)
		sequences = []
		sequences += [''.join(seq) for seq in product('01', repeat=1)]
		sequences += [''.join(seq) for seq in product('01', repeat=2)]
		sequences += [''.join(seq) for seq in product('01', repeat=3)]
		# sequences += [''.join(seq) for seq in product('01', repeat=4)]
		# sequences += [''.join(seq) for seq in product('01', repeat=5)]

		# Tree will be stored in a set to avoid duplicate counterfactuals
		counterfactuals = set()
		samples = list()

		# When exhaustively searching the binary sequences, track which
		# sequences lead to novel counterfactuals, store in cf_seq
		cf_seq = list()
		for seq in sequences:
			temp = self.E.get_summary(False,seq)
			len_before = len(counterfactuals)
			counterfactuals.add(temp)
			len_after = len(counterfactuals)
			if len_before != len_after:
				cf_seq.append(seq)


		# Construct counterfactuals and samples from cf_seq
		for i in range(1):
			for seq in cf_seq:
				temp = self.E.get_summary(False,seq)
				samples.append(temp)
				
				# temp = (t for t in temp if t[2] > 0)
				counterfactuals.add(temp)
		
		return list(counterfactuals), samples
		# return cf_seq

	# sets up checklist of event pairs to construct causal relations for!
	def setup_checklist(self):

		counterfactuals, samples = self.sample_counterfactuals()
		to_check = set()

		for cf in counterfactuals:
			to_check = to_check.union(set(combinations(zip(*cf)[0],2)))

		to_check_final = list()
		for check in to_check:
			if check[1] != 'Ball E going through the gate' and \
				check[1] != 'Ball E not going through the gate' and \
				'not' in check[1]:
				continue
			else:
				to_check_final.append(check)

		return tuple(to_check_final), samples
		
	# construct causal relations for:
	# -cause
	# -prevented
	# -affected
	def get_relations(self, e1, e2, samples):
        
		complement = {
            'Ball A and Ball B collide': 'Ball A and Ball B do not collide',
            'Ball A and Ball E collide': 'Ball A and Ball E do not collide',
            'Ball B and Ball E collide': 'Ball B and Ball E do not collide',
            'Ball A and Ball B do not collide': 'Ball A and Ball B collide',
            'Ball A and Ball E do not collide': 'Ball A and Ball E collide',
            'Ball B and Ball E do not collide': 'Ball B and Ball E collide',
            'Ball E going through the gate': 'Ball E not going through the gate',
            'Ball E not going through the gate': 'Ball E going through the gate'
        }

		caused = list()
		prevented = list()
		affected = list()

		cause_1 = 0.0
		cause_2 = 0.0
		affect_1 = 0.0
		affect_2 = 0.0
		affect_times = set()
		for sample in samples:
			sample = zip(*sample)
			for event in sample:

				
				if e1 in sample[0] and e2 in sample[0]:
					cause_1 += 1
				if e1 in sample[0] and e2 not in sample[0]:
					cause_2 += 1

				if e1 in sample[0] and e2 in sample[0]:
					affect_1 += 1
					e2_index = sample[0].index(e2)
					if len(affect_times) == 0:
						affect_times.add(sample[1][e2_index])
					else: 
						if all([abs(sample[1][e2_index]-t) > .08 for t in list(affect_times)]):
							affect_times.add(sample[1][e2_index])

				if complement[e1] in sample[0] and e2 in sample[0]:
					affect_2 += 1
					e2_index = sample[0].index(e2)
					if len(affect_times) == 0:
						affect_times.add(sample[1][e2_index])
					else: 
						if all([abs(sample[1][e2_index]-t) > .08 for t in list(affect_times)]):
							affect_times.add(sample[1][e2_index])


		caused.append((e1,'CAUSED',e2, cause_1/(cause_1+cause_2)))
		prevented.append((e1,'PREVENTED',complement[e2], cause_1/(cause_1+cause_2)))
		if len(affect_times) > 1:
			affected.append((e1,'AFFECTED',e2, tuple(affect_times)))

		return caused, affected

	# E1 CAUSED E2 if 
	# e1 -> e2
	# e1 -> ~e2
	# E1 AFFECTED E2 if 
	# When E1 in sample, e2 at time t
	# When E2 not in sample, e2 at time t+1
	"""
	
	if e1 in sample[0] and e2 in sample[0]:
		if e2 




	"""