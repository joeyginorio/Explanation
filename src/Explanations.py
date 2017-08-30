# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""

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
			temp = C.get_relations(check[0],check[1],samples)
			if len(temp[1]) > 0:
				temp = temp[1][0]
			else:
				temp = temp[0][0]

			relations.append(temp)

		return relations

	def build_explanations(self, relations):

		explanation = set()
		repeat = True
		
		while repeat:
			
			total_relations_pre = len(relations)

			for relation in relations:
				temp = self.build_helper(relation, relations)
				if len(temp) > 0:
					explanation.add(self.build_helper(relation, relations)[0])

			relations += list(explanation)

			# Check if any new explanations made
			relations = set(relations)
			total_relations_post = len(relations)
			relations = list(relations)

			# End while loop if no new explanations made
			if total_relations_pre == total_relations_post:
				repeat=False

		return list(relations)

	def build_helper(self, temp, relations):

		explanation = set()
		
		for relation in relations:
			if temp[len(temp)-2] == relation[0]:
				time = [temp[-1]]
				time += [relation[-1]]
				explanation.add((temp[0:len(temp)-2]+relation[0:len(temp)-1] + (tuple(time),)))

		return tuple(explanation)

	def score_explanations(self, explanations):
		pass





"""

P(E|S) ~ P(S|E)P(E)

P(S|E) = Calculate this using assumption about how we report events and non-events
P(E) = negative exponential or uniform

P(S|E) = 1/Distance(S,E)

Distance(S,E)=How many events mentioned matter
P(E) = 1/len(explanation)


'A/B collide CAUSED B/E '


"""