# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script runs an experiment on a number of trials, 
	extracting the results from the model.
"""

from Explanations import Explanations
from Events import Events
import csv

class Experiment():

	# 5,7,8,13,16,23
	def __init__(self):

		# oFile = open('model_results.csv','w')
		# CSV = csv.writer(oFile)

		# results = list()
		# clips = [5,7,9,13,16,23]
		# funcs = [self.trial5,self.trial7,self.trial9,self.trial13,self.trial16,self.trial23]

		# for i in range(len(funcs)):
		# 	r = funcs[i]()
		# 	CSV.writerow([clips[i],r[0][0],r[0][1]])
		# 	CSV.writerow([clips[i],r[1][0],r[1][1]])
		# 	CSV.writerow([clips[i],r[2][0],r[2][1]])

		# oFile.close()
		pass

		

	# ballPositions = [A.x, A.y, A.linx, A.liny, B.x, B.y, B.linx, B.liny, E.x, E.y, E.linx, E.liny]
	# ballPositions[6] = [350, height/2,0,0,width + 30, height/2,-1,0,150,height/2,0,0];
	def trial7(self, animate=False, seq='1', save=False):
		a_pos = (350,300)
		a_vel = (0,0)
		b_pos = (830,300)
		b_vel = (-300,0)
		e_pos = (150,300)
		e_vel = (0,0)
		
		if animate:
			E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
			E.simulate(animate, seq,save)
			return

		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results

	# ballPositions[8] = [width + 30, height/2,-0.9,0,width + 60, 550,-1.1,-0.3,100,height/2,0,0];
	def trial9(self, animate=False, seq='1',save=False):
		a_pos = (830,300)
		a_vel = (-280,0)
		b_pos = (860,50)
		b_vel = (-330,95)
		e_pos = (100,300)
		e_vel = (0,0)
		
		if animate:
			E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
			summary = E.get_summary(animate, seq,save)
			return summary

		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results

	# ballPositions[4] = [200, 350,0,0,width + 30, 550,-1,-0.15,300,450,0,0];
	def trial5(self, animate=False, seq='1',save=False):
		a_pos = (200,250)
		a_vel = (0,0)
		b_pos = (830,50)
		b_vel = (-300,45)
		e_pos = (300,150)
		e_vel = (0,0)
		
		if animate:
			E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
			summary = E.get_summary(animate, seq, save)
			return summary

		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results

	# ballPositions[12] = [width + 30, 280,-0.9,0.06,width + 180, 550,-1.2,-0.4,100,height/2,0,0];
	def trial13(self, animate=False, seq='1',save=False):
		a_pos = (850,340)
		a_vel = (-250,-18)
		b_pos = (970,50)
		b_vel = (-320,120)
		e_pos = (100,300)
		e_vel = (0,0)
		
		if animate:
			E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
			summary = E.get_summary(animate, seq, save)
			return summary

		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results


	# ballPositions[15] = [width + 30, 430,-1,-0.18,width + 30, 170,-3/4,0.18*3/4,width/2-230,height/2,0,0];
	def trial16(self, animate=False, seq='1',save=False):
		a_pos = (830,170)
		a_vel = (-300,56)
		b_pos = (830,430)
		b_vel = (-225,-45.5)
		e_pos = (170,300)
		e_vel = (0,0)
		
		if animate:
			E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
			summary = E.get_summary(animate, seq, save)
			return summary

		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results


	# ballPositions[23] = [width+170, 50,-1,0.35,width + 250, 550,-1.1,-0.2,width+30,250,-0.75,0];
	def trial23(self, animate=False, seq='1',save=False):
		a_pos = (300,500)
		a_vel = (0,0)
		b_pos = (600,500)
		b_vel = (-240,0)
		e_pos = (820,250)
		e_vel = (-350,0)
		
		if animate:
			E = Events(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
			summary = E.get_summary(animate, seq, save)
			return summary

		E = Explanations(a_pos, a_vel, b_pos, b_vel, e_pos, e_vel)
		results = E.posterior_explanations()

		return results
