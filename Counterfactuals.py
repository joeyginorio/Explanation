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
from itertools import product

class Counterfactuals():

	def __init__(self):
		pass

	def get_tree(self):

       	# Build a space of counterfactuals (fix this to a smarter search later)
		sequences = []
		sequences += [''.join(seq) for seq in product('01', repeat=1)]
		sequences += [''.join(seq) for seq in product('01', repeat=2)]
		sequences += [''.join(seq) for seq in product('01', repeat=3)]
		sequences += [''.join(seq) for seq in product('01', repeat=4)]
		sequences += [''.join(seq) for seq in product('01', repeat=5)]
		sequences += [''.join(seq) for seq in product('01', repeat=6)]

		# Initialize events engine
		E = Events()

		# Tree will be stored in a set to avoid duplicate counterfactuals
		tree = set()

		# Do the brute force search
		for seq in sequences:
			tree.add(E.get_summary(False,seq))
		
		return list(tree)

	def build_relations(self, tree):

		# Takes in a tree, and builds relations among its branches





