import sys
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
import itertools
import json
import numpy as np
import math
from pymunk import Vec2d
import collections #for keeping the order in which dictionaries were created

class World():
	"""
	Sets up world and simulates a particular trial
	- can save the resulting images 
	- can animate or not animate the simulation 
	- note: y-coordinates are flipped compared to javascript or flash implementation
	- run python window in low resolution mode: /usr/local/Cellar/python@2/2.7.14_3/Frameworks/Python.framework/Versions/2.7/Resources/Python.app
	- counterfactual tests could be made more efficient by only running the actual situation once
	"""

	def __init__(self):
		pass 

	def pymunk_setup(self,experiment):
		# Initialize space and set gravity for space to do simulation over
		self.width = 800
		self.height = 600
		self.ball_size = 60 
		self.speed = 200 # scales how fast balls are moving 
		self.step_size = 1/50.0
		self.step_max = 300 # step at which to stop the animation
		self.step = 0 # used to record when events happen 
		self.space = pymunk.Space()
		self.events = [] # used to record events 
		# containers for bodies and shapes
		self.bodies = collections.OrderedDict()
		self.shapes = collections.OrderedDict()	
		self.sprites = collections.OrderedDict()
		
		self.collision_types = {
			'static': 0,
			'dynamic': 1,
			'teleport': 2
		}		
		self.experiment = experiment

		if self.experiment == '3ball':
			self.target_ball = 'E'
		else:
			self.target_ball = 'B'
	
		# add walls 
		self.add_wall(position = (400,590), length = 800, height = 20, name = 'top_wall', space = self.space)
		self.add_wall(position = (400,10), length = 800, height = 20, name = 'bottom_wall', space = self.space)
		self.add_wall(position = (10,100), length = 20, height = 200, name = 'top_left_wall', space = self.space)
		self.add_wall(position = (10,500), length = 20, height = 200, name = 'bottom_left_wall', space = self.space)

		# read in trial info 
		self.read_trials()
		self.balls = self.trials[self.trial]['balls']

		# add objects 
		if self.experiment == 'teleport':
			self.objects = self.trials[self.trial]['objects']
			for object in self.objects: 
				if object['name'] == 'brick':
					body, shape = self.add_brick(position = object['position'], name = object['name'], rotation = object['rotation'], space = self.space)
				if object['name'] == 'teleport_entrance':
					body, shape = self.add_teleport_entrance(position = object['position'], name = object['name'], rotation = object['rotation'], status = object['status'], space = self.space)
				if object['name'] == 'teleport_exit':
					body, shape = self.add_teleport_exit(position = object['position'], name = object['name'], status = object['status'], space = self.space)
				self.bodies[object['name']] = body
				self.shapes[object['name']] = shape		

		# add balls 
		for ball in self.balls:
			body, shape = self.add_ball(position = ball['position'], name = ball['name'], velocity = ball['velocity'], size = self.ball_size, space = self.space) 
			self.bodies[ball['name']] = body
			self.shapes[ball['name']] = shape

	# read in trial information 
	def read_trials(self):
		self.trials = json.load(open('trialinfo/' + self.experiment + '_trials.json', 'r'))

	# setup collision handlers 
	def collision_setup(self):	
		handler_dynamic = self.space.add_collision_handler(self.collision_types['dynamic'], self.collision_types['dynamic'])
		handler_dynamic.begin = self.collisions
		
		if self.experiment == 'teleport':		
			handler_teleport = self.space.add_collision_handler(self.collision_types['teleport'], self.collision_types['dynamic'])
			if self.bodies['teleport_entrance'].status == 'on':
				handler_teleport.begin = self.teleport


	# handle dynamic events
	def collisions(self,arbiter,space,data):
		# print arbiter.is_first_contact #checks whether it was the first contact between the shapes 
		event = {
			'balls': [arbiter.shapes[0].body.name,arbiter.shapes[1].body.name],
			'step': self.step,
			'type': 'collision'
		}
		self.events.append(event)
		return True

	# handle teleport
	def teleport(self,arbiter,space,data):
		objects = [arbiter.shapes[0].body,arbiter.shapes[1].body]
		for object in objects: 
			if object.name == 'B':
				object.position = self.bodies['teleport_exit'].position 
		return False	

	def add_wall(self, position, length, height, name, space):
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		wall = pymunk.Poly.create_box(body, size = (length, height))
		wall.elasticity = 1
		wall.name = name 
		wall.collision_type = self.collision_types['static']
		space.add(wall)
		return wall	

	def add_ball(self, position, velocity, size, name, space):
		mass = 1
		radius = size/2
		moment = pymunk.moment_for_circle(mass, 0, radius)
		body = pymunk.Body(mass, moment)
		body.position = position
		body.size = (size,size)
		body.angle = 0
		velocity = map(lambda x: x*self.speed,velocity) 
		body.apply_impulse_at_local_point(velocity) #set velocity
		body.name = name 
		shape = pymunk.Circle(body, radius)
		shape.elasticity = 1.0
		shape.friction = 0
		shape.collision_type = self.collision_types['dynamic']
		space.add(body, shape)
		return body, shape

	def add_brick(self, position, rotation, name, space):
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		body.name = name 
		body.size = (35, 100)
		body.angle = math.radians(rotation)
		shape = pymunk.Poly.create_box(body, size = body.size)
		shape.elasticity = 1
		shape.collision_type = self.collision_types['static']
		space.add(body, shape)
		return body, shape

	def add_teleport_entrance(self, position, rotation, name, status, space):
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		body.name = name 
		body.size = (35, 100)
		body.angle = math.radians(rotation)
		body.status = status
		shape = pymunk.Poly.create_box(body, size = body.size)
		shape.sensor = True
		shape.collision_type = self.collision_types['teleport']
		space.add(body, shape)
		return body, shape

	def add_teleport_exit(self, position, name, status, space):
		# take out of physics later ... 
		body = pymunk.Body(body_type = pymunk.Body.STATIC)
		body.position = position
		body.name = name 
		# body.size = (40,40)
		body.angle = 0
		body.status = status
		shape = pymunk.Circle(body, 20)
		shape.sensor = True
		# space.add(body, shape)
		return body, shape

	def remove(self,ball,step,animate):
		if self.step == step:
			self.space.remove(self.shapes[ball]) #remove body from space 
			self.space.remove(self.bodies[ball]) #remove body from space 
			del self.bodies[ball] #remove body 
			del self.shapes[ball] #remove shape
			if animate: 		
				del self.sprites[ball] #remove sprite 

	def perturb(self,ball,step,magnitude = 0):
		if self.step == step:
			b = self.bodies[ball]
			b.position = (b.position.x+self.gaussian_noise()*magnitude,
				b.position.y+self.gaussian_noise()*magnitude)

	def apply_noise(self,ball,step,noise):
		if not noise == 0:
			b = self.bodies[ball]
			if self.step > step:
				x_vel = b.velocity[0]
				y_vel = b.velocity[1]
				perturb = self.gaussian_noise()*noise
				cos_noise = np.cos(perturb*np.pi/180)
				sin_noise = np.sin(perturb*np.pi/180)
				x_vel_noise = x_vel * cos_noise - y_vel * sin_noise
				y_vel_noise = x_vel * sin_noise + y_vel * cos_noise
				b.velocity = x_vel_noise,y_vel_noise

	def end_clip(self,animate):
		if self.step > self.step_max:
			b = self.bodies[self.target_ball]
			event = {
					'ball': self.target_ball,
					'step': self.step,
					'type': 'outcome',
				}
			if b.position[0] > -self.ball_size/2:
				event['outcome'] = 0
			else:
				event['outcome'] = 1
			event['outcome_fine'] = b.position
			self.events.append(event)
			pygame.display.quit()
			return True

	def simulate(self, experiment = '3ball', animate=True, trial=0, noise = 0, save=False, info=[]):
		# Initialization 
		self.trial = trial
		self.pymunk_setup(experiment)
		self.collision_setup()
		pic_count = 0 # used for saving images 
		done = False # pointer to say when animation is done 
		self.info = info
		self.noise = noise
		
		# If animating, initialize pygame animation
		if animate:
			pygame.init()
			clock = pygame.time.Clock()

			# Set size/title of display
			screen = pygame.display.set_mode((self.width, self.height))
			pygame.display.set_caption("Animation")

			# Load sprites
			for body in self.bodies:
				b = self.bodies.get(body)
				if  b.name == 'teleport_entrance' or b.name == 'teleport_exit':
					name = b.name + "_" + b.status
				else: 
					name = b.name
				sprite = pygame.image.load('figures/' + name + '.png')
				self.sprites[body] = sprite

		# Run the simulation forever, until exit
		while not done:
			if animate:
				# Lets you exit the animation loop by clicking escape on animation
				for event in pygame.event.get():
					if event.type == QUIT:
							sys.exit(0)
					elif event.type == KEYDOWN and event.key == K_ESCAPE:
							sys.exit(0)

				# Draw static elements 
				screen.fill((255,255,255)) #background 
				pygame.draw.rect(screen, pygame.color.THECOLORS['red'], [0,200,20,200]) #goal
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,0,800,20]) #top wall
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,580,800,20]) #bottom wall
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,0,20,200]) #top left
				pygame.draw.rect(screen, pygame.color.THECOLORS['black'], [0,400,20,200]) #bottom left
				
				# update object positions over time 
				for body in self.bodies:
					self.update_sprite(body = self.bodies.get(body), sprite = self.sprites.get(body),screen = screen)

				# Draw the space
				pygame.display.flip()
				pygame.display.update()
				clock.tick(100)
				
				if save:
					pygame.image.save(screen, 'figures/frames/animation'+'{:03}'.format(pic_count)+'.png')
					pic_count += 1

			# manipulations 
			if self.info:
				for action in self.info:
					if action['action'] == 'remove':
						self.remove(ball = action['ball'], step = action['step'], animate = animate)
					if action['action'] == 'perturb':
						self.perturb(ball = action['ball'], step = action['step'], magnitude = action['magnitude'])
					if action['action'] == 'noise':
						self.apply_noise(ball = action['ball'], step = action['step'], noise = self.noise)

			# Take a step in the simulation, update clock/ticks
			done = self.end_clip(animate = animate)

			self.space.step(self.step_size) 
			self.step += 1

		return self.events

	def flipy(self, y):
	    """Small hack to convert chipmunk physics to pygame coordinates"""
	    return -y+600

	def update_sprite(self,body,sprite,screen):
		p = body.position
		p = Vec2d(p.x, self.flipy(p.y))
		angle_degrees = math.degrees(body.angle)
		rotated_shape = pygame.transform.rotate(sprite, angle_degrees)
		offset = Vec2d(rotated_shape.get_size()) / 2.
		p = p - offset
		screen.blit(rotated_shape, p)

	def gaussian_noise(self):
		u = 1 - np.random.random()
		v = 1 - np.random.random()
		return np.sqrt(-2*np.log(u)) * np.cos(2 * np.pi * v)

	##############################
	# define counterfactual operations 
	##############################

	def difference_cause(self, w, experiment, noise, trial, cause, alternatives, df, n_simulations, animate):
		# run actual world 
	 	events = w.simulate(experiment = experiment, trial = trial, animate=animate)	

		# record actual outcome, records first collision in which ball participated 
		collision_time = float("inf")
		for event in events:
			if event['type'] == 'collision':
				for ball in event['balls']:
					if ball == cause:
						if event['step'] < collision_time:
							collision_time = event['step']
			if event['type'] == 'outcome':
				outcome_actual = event['outcome_fine']

		# remove candidate cause 
		info = [{
			'action': 'remove',
			'ball': cause,
			'step': collision_time-1
		}]

		# noise in alternative causes 
		for alternative in alternatives: 
				info.append({
					'action': 'noise',
					'ball': alternative,
					'step': collision_time-1
				})

		outcomes = []
		for x in range(0, n_simulations):
			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			for event in events:
				if event['type'] == 'outcome':
					outcome_counterfactual = event['outcome_fine']
			outcomes.append(outcome_actual != outcome_counterfactual)
		
		return any(outcomes)

	def whether_cause(self, experiment, noise, w, trial, cause, df, n_simulations, animate):
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate=animate)	

		# record actual outcome, records first collision in which ball participated 
		collision_time = float("inf")
		for event in events:
			if event['type'] == 'collision':
				for ball in event['balls']:
					if ball == cause:
						if event['step'] < collision_time:
							collision_time = event['step']
			if event['type'] == 'outcome':
				outcome_actual = event['outcome']

		# remove candidate cause 
		info = [{
			'action': 'remove',
			'ball': cause,
			'step': collision_time
		}
		]

		# record what bodies are in the world 
		other_balls = []
		for body in w.space.bodies:
			other_balls.append(body.name)
		other_balls.remove(cause) #remove cause from list 

		for ball in other_balls:
			info.append({
				'action':'noise',
				'ball':ball,
				'step': collision_time
				})

		outcomes = []
		for x in range(0, n_simulations):
			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			for event in events:
				if event['type'] == 'outcome':
					outcomes.append(event['outcome'] != outcome_actual)
		
		return sum(outcomes)/float(n_simulations)

	def how_cause(self, w, experiment, noise, trial, cause, df, animate):
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate=animate)	
				
		# record actual outcome, records first collision in which ball participated 
		collision_time = float("inf")
		for event in events:
			if event['type'] == 'collision':
				for ball in event['balls']:
					if ball == cause:
						if event['step'] < collision_time:
							collision_time = event['step']
			if event['type'] == 'outcome':
				outcome_actual = event['outcome_fine']

		# perturb candidate cause 
		info = [{
			'action': 'perturb',
			'ball': cause,
			'step': collision_time-1,
			'magnitude': 0.0001
		}]

		events = w.simulate(experiment = experiment, trial = trial, animate = animate, info = info)
		for event in events:
			if event['type'] == 'outcome':
				outcome_counterfactual = event['outcome_fine']
		
		return (outcome_counterfactual != outcome_actual)

	def sufficient_cause(self, w, experiment, noise, trial, cause, alternatives, target, df, n_simulations, animate):
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate=animate)	

		# record actual outcome, records first collision in which ball participated 
		collision_time = float("inf")
		for event in events:
			if event['type'] == 'collision':
				for ball in event['balls']:
					if ball == cause:
						if event['step'] < collision_time:
							collision_time = event['step']
			if event['type'] == 'outcome':
				outcome_actual = event['outcome']

		outcomes = []
		for x in range(0, n_simulations):
			info = []
			# remove alternative cause 
			for alternative in alternatives: 
				info.append({
					'action': 'remove',
					'ball': alternative,
					# 'step': collision_time
					'step': 0
				})

			info.append({
				'action': 'noise',
				'ball': target,
				'step': collision_time
				})

			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			for event in events:
				if event['type'] == 'outcome':
					outcome_counterfactual = event['outcome']

			info = []
			# remove alternative cause 
			for alternative in alternatives: 
				info.append({
					'action': 'remove',
					'ball': alternative,
					'step': 0
				})

			# remove cause 
			info.append({
				'action': 'noise',
				'ball': target,
				'step': collision_time
				})

			info.append({
				'action': 'remove',
				'ball': cause,
				'step': collision_time
				})

			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			for event in events:
				if event['type'] == 'outcome':
					outcome_counterfactual_contingency = event['outcome']
			 
			outcomes.append((outcome_actual == outcome_counterfactual) and (outcome_counterfactual != outcome_counterfactual_contingency))
		
		return sum(outcomes)/float(n_simulations)

	def robust_cause(self, w, experiment, noise, perturb, trial, cause, alternatives, target, df, n_simulations, animate):
		# run actual world 
		events = w.simulate(experiment = experiment, trial = trial, animate=animate)	

		# record actual outcome, records first collision in which ball participated 
		collision_time = float("inf")
		for event in events:
			if event['type'] == 'collision':
				for ball in event['balls']:
					if ball == cause:
						if event['step'] < collision_time:
							collision_time = event['step']
			if event['type'] == 'outcome':
				outcome_actual = event['outcome']

		outcomes = []
		for x in range(0, n_simulations):
			info = []
			
			# perturb alternative cause 
			for alternative in alternatives: 
				info.append({
					# 'action': 'noise',
					# 'ball': alternative,
					# 'step': 0
					'action': 'perturb',
					'ball': alternative,
					'step': 0,
					'magnitude': perturb
				})

			info.append({
				'action': 'noise',
				'ball': target,
				'step': collision_time
				})

			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			for event in events:
				if event['type'] == 'outcome':
					outcome_counterfactual = event['outcome']

			info = []
			
			# perturb and apply noise to alternative cause 
			for alternative in alternatives: 
				# apply perturbation
				info.append({
					'action': 'perturb',
					'ball': alternative,
					'step': 0,
					'magnitude': perturb
				})

				# noise after collision
				info.append({
					'action': 'noise',
					'ball': alternative,
					'step': collision_time
				})

			# remove cause 
			info.append({
				'action': 'noise',
				'ball': target,
				'step': collision_time
				})

			info.append({
				'action': 'remove',
				'ball': cause,
				'step': (collision_time-10) #remove a little earlier because of pertubation
				})

			events = w.simulate(experiment = experiment, trial = trial, animate = animate, noise = noise, info = info)
			for event in events:
				if event['type'] == 'outcome':
					outcome_counterfactual_contingency = event['outcome']
			 
			outcomes.append((outcome_actual == outcome_counterfactual) and (outcome_counterfactual != outcome_counterfactual_contingency))
		
		return sum(outcomes)/float(n_simulations)
