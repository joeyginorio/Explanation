# Joey Velez-Ginorio
# BMM Summer Project w/ Tobi

"""
	This script generates events and their animations using pygame
	and pymunk. The main function "simulate" returns a list of events
    tagged with the time they occurred.
"""

import sys
import pygame
import pygame.gfxdraw
from pygame.locals import *
from pymunk.vec2d import Vec2d
from itertools import product
import pymunk
import pymunk.pygame_util
import random
import numpy as np

class Events():
    
    # Initialize the pymunk physics engine details
    def __init__(self, a_pos, a_vel, b_pos, b_vel, e_pos, e_vel):
        self.a_pos = a_pos
        self.b_pos = b_pos
        self.e_pos = e_pos

        self.a_vel = a_vel
        self.b_vel = b_vel
        self.e_vel = e_vel


    def pymunk_setup(self):
        # Initialize space and set gravity for space to do simulation over
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.damping = .8

        # Specify collisions of interest
        self.collision_types = {
            'ball_a':0,
            'ball_b':1,
            'ball_e':2
        }

        # Add rigid bodies to physics engine
        self.balls_body, self.balls_shape = self.add_balls(self.space)
        self.walls = self.add_walls(self.space)

        # Tell pymunk which collisions to catch
        self.collision_setup()
        self.counter = 0

        # Initialize list to hold all events, and the timer to timestamp them
        self.timer = 0.0

    def get_summary(self, animate, seq):

        events = self.simulate(animate, seq)
        times = np.unique([i[1] for i in events])

        summary = list()
        for time in times:

            temp = ""
            first = False
            for event in events:
                if event[1] == time:
                    if not first:
                        temp += event[0]
                        first = True

                    else:
                        temp += ' AND ' + event[0]

            summary.append((temp, time))

        return tuple(summary)

    def simulate(self, animate=False, seq='1'):

        self.pymunk_setup()

        self.events = []
        self.counter = 0
        self.sequence = seq

        # If animating, initialize pygame animation
        if animate:

            pygame.init()
            clock = pygame.time.Clock()

            # Set size/title of display
            screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Compositional Explanation")

            # Load sprites
            ball_a = pygame.image.load('ball_a.png')
            ball_a = pygame.transform.scale(ball_a, (50,50))
            ball_a = ball_a.convert_alpha()
            ball_a_rect = ball_a.get_rect()

            ball_b = pygame.image.load('ball_b.png')
            ball_b = pygame.transform.scale(ball_b, (50,50))
            ball_b = ball_b.convert_alpha()
            ball_b_rect = ball_b.get_rect()

            ball_e = pygame.image.load('ball_e.png')
            ball_e = pygame.transform.scale(ball_e, (50,50))
            ball_e = ball_e.convert_alpha()
            ball_e_rect = ball_e.get_rect()

            # Gives drawing options for the pygame screen
            draw_options = pymunk.pygame_util.DrawOptions(screen)
           
        # Set initial impulses
        self.balls_body[0].apply_impulse_at_local_point(self.a_vel)
        self.balls_body[1].apply_impulse_at_local_point(self.b_vel)
        self.balls_body[2].apply_impulse_at_local_point(self.e_vel)

        # Will be used to auto-exit if balls stop moving
        done = False
        
        # Run the simulation forever, until exit
        while True:

            if self.counter == len(self.sequence):
                self.sequence += '1'

            if animate:

                if done:
                    pygame.display.quit()
                    return self.events

                elif self.balls_stopped():
                    pygame.display.quit()
                    return self.events

                # Lets you exit the animation loop by clicking x on animation    
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit(0)
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        sys.exit(0)

                # Fill screen with white background 
                screen.fill((255,255,255))
                self.space.debug_draw(draw_options)
                pygame.draw.rect(screen, (255,100,100), [0,200,16,200])

        
                ball_a_pos = self.to_pygame(self.balls_body[0].position)
                ball_a_pos[0] -= 50
                ball_a_pos[1] -= 50
                screen.blit(ball_a, ball_a_pos)

                ball_b_pos = self.to_pygame(self.balls_body[1].position)
                ball_b_pos[0] -= 50
                ball_b_pos[1] -= 50
                screen.blit(ball_b, ball_b_pos)

                ball_e_pos = self.to_pygame(self.balls_body[2].position)
                ball_e_pos[0] -= 50
                ball_e_pos[1] -= 50
                screen.blit(ball_e, ball_e_pos)

                # Draw the space
                pygame.display.flip()
                pygame.display.update()
                clock.tick(100)


            else:
                # Simulation auto ends when ball e goes through game or balls stop
                if done:
                    return self.events

                elif self.balls_stopped():
                    return self.events

            # Checks if E through the gate
            done = self.ball_e_through_gate()

            # Take a step in the simulation, update clock/ticks
            self.space.step(1/100.0) #3
            self.timer += (1/100.0)
            self.timer = round(self.timer,5)

        self.counter = 0



    def add_balls(self, space):

        # Each rigid body requires mass and moment
        mass = 1
        radius = 25
        moment = pymunk.moment_for_circle(mass, 0, radius)
        A_body = pymunk.Body(mass, moment)
        B_body = pymunk.Body(mass, moment)
        E_body = pymunk.Body(mass, moment)

    	# Set position of rigid body
        A_body.position = self.a_pos
        B_body.position = self.b_pos
        E_body.position = self.e_pos

    	# Add shape to rigid body
        A_shape = pymunk.Circle(A_body, radius)
        A_shape.collision_type = self.collision_types['ball_a']
        A_shape.elasticity = 1.0
        A_shape.friction = .6
        # A_shape.color = (50,255,50)

        B_shape = pymunk.Circle(B_body, radius)
        B_shape.collision_type = self.collision_types['ball_b']
        B_shape.elasticity = 1.0
        B_shape.friction = .6
        # B_shape.color = (50,50,255)

        E_shape = pymunk.Circle(E_body, radius)
        E_shape.collision_type = self.collision_types['ball_e']
        E_shape.elasticity = 1.0
        E_friction = .6
        # E_shape.color = (50,50,50)

        space.add(A_body, A_shape)
        space.add(B_body, B_shape)
        space.add(E_body, E_shape)

        return (A_body, B_body, E_body),(A_shape, B_shape, E_shape)

    def add_walls(self, space):

        body1 = pymunk.Body(body_type = pymunk.Body.STATIC)
        body1.position = (400,595)
        wall1 = pymunk.Segment(body1, (-400,0),(400,0), 15)
        wall1.color = pygame.color.THECOLORS['black']
        wall1.elasticity = .5
        space.add(wall1)

        body2 = pymunk.Body(body_type = pymunk.Body.STATIC)
        body2.position = (400,5)
        wall2 = pymunk.Segment(body2, (-400,0),(400,0), 15)
        wall2.color = pygame.color.THECOLORS['black']
        wall2.elasticity = .5
        space.add(wall2)

        body3 = pymunk.Body(body_type = pymunk.Body.STATIC)
        body3.position = (0,0)
        wall3 = pymunk.Segment(body3, (0,0),(0,200), 15)
        wall3.color = pygame.color.THECOLORS['black']
        wall3.elasticity = .5
        space.add(wall3)

        body4 = pymunk.Body(body_type = pymunk.Body.STATIC)
        body4.position = (0,0)
        wall4 = pymunk.Segment(body4, (0,400),(0,600), 15)
        wall4.color = pygame.color.THECOLORS['black']
        wall4.elasticity = .5
        space.add(wall4)

        return wall1, wall2, wall3, wall4

    def collide_ball_ab(self, arbiter, space, data):
    
        if int(self.sequence[self.counter]):
            self.events.append(['Ball A and Ball B collide', self.timer])       
            self.counter += 1
            return True
        else:
            self.events.append(['Ball A and Ball B do not collide', self.timer])
            self.counter += 1
            return False

    def collide_ball_ae(self, arbiter, space, data):

        if int(self.sequence[self.counter]):
            self.events.append(['Ball A and Ball E collide', self.timer])
            self.counter += 1
            return True
        else:
            self.events.append(['Ball A and Ball E do not collide', self.timer])
            self.counter += 1
            return False

    def collide_ball_be(self, arbiter, space, data):

        if int(self.sequence[self.counter]):
            self.events.append(['Ball B and Ball E collide', self.timer])
            self.counter += 1
            return True
        else:
            self.events.append(['Ball B and Ball E do not collide', self.timer])
            self.counter += 1
            return False

    def ball_e_through_gate(self):

        if self.balls_body[2].position[0] < -30:
            self.events.append(['Ball E going through the gate', self.timer])
            return True

    def balls_stopped(self):

        temp = [abs(i.velocity[0])+abs(i.velocity[1]) < 20 for i in self.balls_body]

        if all(temp) and self.balls_body[2].position[0] > -20:
            self.events.append(['Ball E not going through the gate', self.timer])
        
        return all(temp)

    def collision_setup(self):

        # Handle collisions between a and b
        ball_ab = self.space.add_collision_handler(self.collision_types['ball_a'], 
                                            self.collision_types['ball_b'])
        ball_ab.begin = self.collide_ball_ab

        # Handle collisions between a and e
        ball_ae = self.space.add_collision_handler(self.collision_types['ball_a'], 
                                            self.collision_types['ball_e'])
        ball_ae.begin = self.collide_ball_ae

        # Handle collisions between b and e
        ball_be = self.space.add_collision_handler(self.collision_types['ball_b'], 
                                            self.collision_types['ball_e'])
        ball_be.begin = self.collide_ball_be

    def to_pygame(self, position):
        # Small hack to convert pymunk to pygame coordinates
        return [int(position.x)+25, int(-position.y+625)]






