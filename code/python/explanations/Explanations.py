# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script uses counterfactuals over events in a physics engine to
	generate explanations.
"""

import numpy as np
import operator
from Events import Events
from Counterfactuals import Counterfactuals

class Explanations():
	"""

	"""

	def __init__(self, a_pos, a_vel, b_pos, b_vel, e_pos, e_vel):
		self.E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)

	def posterior_explanations(self):

		relations = self.setup_explanations()
		explanations = self.build_explanations(relations)

		likelihood = np.array(self.likelihood_explanations(explanations))
		prior = np.array(self.prior_explanations(explanations))

		posterior = likelihood*prior
		explanations = [e[0:-1] for e in explanations]
		explanations = [self.edit_explanation(e) for e in explanations]

		sorted_posterior = sorted(dict(zip(explanations,posterior)).items(), 
			key=operator.itemgetter(1), reverse=True)

		return sorted_posterior

	def setup_explanations(self):
		
		C = Counterfactuals(self.E)
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

	def likelihood_explanations(self, explanations):
		
		actual_events = zip(*self.E.get_summary(False,'1'))[0]
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

		actual_events_new = list()
		for e in explanations:
			if complement[actual_events[0]] in e and \
				'not' not in e[2] and \
				complement[actual_events[-1]] in e:

				actual_events_new = [i for i in e[0:-1] if i != 'CAUSED']
				actual_events_new = [i for i in e[0:-1] if i != 'AFFECTED']




		check = 0
		if len(actual_events_new) > 0:
			for e in explanations:
				if all([i in e for i in actual_events_new]):
					check += 1
			if check < 2:
				actual_events = actual_events_new

		total_events_matter = len(actual_events)

		explanations_score = list()

		for explanation in explanations:

			events_matter = 0.0
			for e in actual_events:
				if e in explanation:
					events_matter += 1.0

			score = events_matter / total_events_matter
			explanations_score.append(score)

		return explanations_score

	def prior_explanations(self, explanations):

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

		explanations_prior = list()

		for explanation in explanations:

			events = explanation[0::2]
			s_count = 0.0
			n_count = 0.0

			for exp in explanations:

				if all([e in exp for e in events[0:-1]]) and events[-1]==exp[-2]:
					s_count += 1.0
				if all([e in exp for e in events[0:-1]]) and events[-1]==complement[exp[-2]]:
					s_count += 1.0

				if all([e in exp for e in events[0:-1]]) and events[-1]==exp[-2]:
					n_count += 1.0
				if all([complement[e] in exp for e in events[0:-1]]) and events[-1]==exp[-2]:
					n_count += 1.0

			explanations_prior.append(.5*(1/s_count)+.5*(1/n_count))

		return explanations_prior

	def edit_explanation(self, explanation):

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

		explanation = list(explanation)
		# Add prevents
		checkpoints = range(len(explanation)-1)[0::2]
		for check in checkpoints:
			if 'not' in explanation[check] and explanation[check+1] != 'AFFECTED':
				explanation[check] = complement[explanation[check]]
				explanation[check+1] = 'PREVENTED'

		would = False
		checkpoints = range(len(explanation))[1::2]
		for check in checkpoints:
			if would:
				explanation[check] = 'WOULD HAVE ' + explanation[check] 

			if explanation[check] == 'PREVENTED':
				would = True

		return tuple(explanation)


