# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script uses a probabilistic context-free grammar (PCFG) to represent
	a compositional space of expressions. For our project, these
	expressions correspond to relations between events represented via 
	a physics engine.
"""


import numpy as np
from Events import Events
from Counterfactuals import Counterfactuals

class Explanations():
	"""

	"""

	def __init__(self):
		pass

	def setup_explanations(self):
		
		C = Counterfactuals()
		checklist, samples = C.setup_checklist()

		relations = list()

		for check in checklist:
			relations.append(C.get_relations(check[0],check[1],samples)[0][0])

		return relations

	def build_explanations(self):

		end = [
			'Ball E not going through the gate',
			'Ball E going through the gate'
		]

