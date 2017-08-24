# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script uses a probabilistic context-free grammar (PCFG) to represent
	a compositional space of expressions. For our project, these
	expressions correspond to relations between events represented via 
	a physics engine.
"""


import numpy as np

class Explanations():
	"""
		Provides a set of functions that will represent and sample from the 
		following grammar:

		Explanation -> (Relation Event Explanation)
		Explanation -> (Relation Event End)

		Relation -> Caused (A then B)
		Relation -> Affected (diff point in time)
		Relation -> Prevented (not A then B)
		Relation -> Made no difference

		Event -> (Ball moving)
		Event -> (Enter Ball) 
		Event -> (Static Ball)
		Event -> (Collision Ball Ball)
		Event -> (Collision Ball Wall)
		Event -> (And Event Event)
		
		Ball -> A
		Ball -> B
		Ball -> E

		Wall -> Top
		Wall -> Bottom
		Wall -> Top left
		Wall -> Bottom left

		End -> Ball E went through the gate
		End -> Ball E didn't go through the gate

	"""

	def __init__(self):
		pass

	# Sample a ball
	def ball(self):
		p = np.ones(3)/3
		balls = ['Ball A', 'Ball B', 'Ball E']

		return np.random.choice(balls,p=p)

	# Sample a wall
	def wall(self):
		p = np.ones(4)/4
		walls = ['Top Wall', 'Bottom Wall', 'Top-left Wall', 'Bottom-left Wall']

		return np.random.choice(walls, p=p)

	# Sample an end-condition
	def end(self):
		p = np.ones(2)/2
		ends = ['Ball E going through the gate', 'Ball E not going through the gate']

		return np.random.choice(ends, p=p)

	# Sample an eventcompositionalcompositional
	def event(self):

		p_rec = [.8,.2]
		rec = ['no','yes']

		if np.random.choice(rec,p=p_rec) == 'no':

			p = np.ones(5)/5
			p = p / float(sum(p))

			events = [self.ball() + ' moving', 
					self.ball() + ' not moving',
					self.ball() +' enters', 
					self.ball() + ' and ' + self.ball() + ' collide',
					self.ball() + ' and ' + self.wall() + ' collide']

			return np.random.choice(events, p=p) 

		return self.event() + ' AND ' + self.event()

	def relation(self):
		p = np.ones(4)/4
		relations = ['CAUSED', 'AFFECTED', 'PREVENTED', 'MADE NO DIFFERENCE']

		return np.random.choice(relations, p=p)

	def explanation(self):

		p_rec = [.8,.2]
		rec = ['no','yes']

		if np.random.choice(rec,p=p_rec) == 'no':
			return '(' + self.event() + ' ' + self.relation() +  ' ' + self.end() + ')'

		return '(' + self.event() + ' ' + self.relation() + self.explanation() + ')' 