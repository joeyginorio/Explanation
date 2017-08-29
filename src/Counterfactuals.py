# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script uses counterfactuals to build relations between events
	represented by a physics engine.
"""


"""

	Rules for CF Relation Building:

	1. Simulate actual world, get e_summary()
	- Store current event e, at time t
	- Store next event e_next, at time t+1
	
	2. Simulate counterfactual world
	- Ignore event e, at time t
	- Store next event e_next_cf, at time t+1

	3. Build Relations 

	If next event e_next == e_next_cf
	- If e_next and e_next_cf happen at same time t+1, e MADE NO DIFFERENCE e_next
	- If e_next and e_next_cf happen at different times t+1, e AFFECTED e_next

	If next event e_next != e_next_cf
	- If e_next_cf not in e_summary, e CAUSED e_next
	- If e_next_cf in e_summary, 

	- If next event at t+1 is not in summary list of events, then event at time t 
	prevented event at time t+1
	- If next event at t+1 
"""

from Events import Events
from itertools import combinations
from itertools import product

class Counterfactuals():

	def __init__(self):
		pass

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

		# Initialize events engine
		E = Events()

		# Tree will be stored in a set to avoid duplicate counterfactuals
		counterfactuals = set()
		samples = list()

		cf_seq = list()
		for seq in sequences:
			temp = E.get_summary(False,seq)
			len_before = len(counterfactuals)
			counterfactuals.add(temp)
			len_after = len(counterfactuals)

			if len_before != len_after:
				cf_seq.append(seq)


		# Do the brute force search
		for i in range(100):
			for seq in cf_seq:
				temp = E.get_summary(False,seq)
				samples.append(temp)
				
				# temp = (t for t in temp if t[2] > 0)
				counterfactuals.add(temp)
		
		return list(counterfactuals), samples
		# return cf_seq

	def setup_checklist(self):

		counterfactuals, samples = self.sample_counterfactuals()
		to_check = set()

		for cf in counterfactuals:
			cf = (c for c in cf if c[2] > 0)
			to_check = to_check.union(set(combinations(zip(*cf)[0],2)))

		return tuple(to_check), samples
		
	def get_relation(self, e1, e2, samples):

		cause_1 = 0.0
		cause_2 = 0.0
		for sample in samples:
			sample = zip(*sample)
			for event in sample:

				if e1 in sample[0]:
					e1_index = sample[0].index(e1)
					# e2_index = sample[0].index(e2)
					if sample[1][e1_index] == False and e2 not in sample[0]:
						cause_1 += 1.0
					if sample[1][e1_index] == False and e2 in sample[0]:
						e2_index = sample[0].index(e2)
						if sample[1][e2_index] == False:
							cause_1 += 1.0
						else:
							cause_2 += 1.0


		return cause_1, cause_2

				# pass

	# E1 CAUSED E2 if 