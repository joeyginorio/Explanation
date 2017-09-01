# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script runs an experiment on a number of trials, 
	extracting the results from the model.
"""

class Experiment():

	def __init__():
		pass

	def trial1(self):
		a_pos = (900,300)
		b_pos = (400,300)
		e_pos = (200,300)
		a_vel = (-300,0)
		b_vel = (0,0)
		e_vel = (0,0)
		
		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results
