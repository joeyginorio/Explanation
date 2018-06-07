from model import World
import sys
import pandas as pd
import numpy as np

##############################
# parameters
##############################

n_simulations = 2
# n_simulations = 4
# n_simulations_difference = 2 #number of simulations to check for difference-making
n_simulations_difference = 1 #number of simulations to check for difference-making
# n_simulations = 2
# trials = range(0,18)
trials = range(0,32)
# trials = [2]
# trials = [16]
noise = float(sys.argv[1]) #noise 
# noise = 0
perturb_robust = 3
# record_data = False
record_data = True
experiment = '3ball'
# animate = True
animate = False
# n_participants = 1
n_participants = 41

##############################
# set up data structure 
##############################

column_names = ['participant','trial','A_difference','A_how','A_whether','A_sufficient','A_robust','B_difference','B_how','B_whether','B_sufficient','B_robust']

df = pd.DataFrame(0.0, index=np.arange(len(trials)), columns=column_names)

df['trial'] = trials
df['noise'] = noise
df['perturb'] = perturb_robust
df['n_simulations'] = n_simulations
df['n_simulations_difference'] = n_simulations_difference
df['trial'] = df['trial']+1

##############################
# run simulations 
##############################

w = World()

for participant in range(0,n_participants):

	for idx, trial in enumerate(trials):
		df.loc[idx, 'A_difference'] = w.difference_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', alternatives = ['B'], df = df, n_simulations = n_simulations_difference, animate = animate)
		
		if df.loc[idx, 'A_difference'] != 0: 
			df.loc[idx, 'A_how'] = w.how_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', df = df, animate = animate)
			df.loc[idx, 'A_whether'] = w.whether_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', df = df, n_simulations = n_simulations, animate = animate)
			df.loc[idx, 'A_sufficient'] = w.sufficient_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'A', alternatives = ['B'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)	
			df.loc[idx, 'A_robust'] = w.robust_cause(w = w, experiment = experiment, noise = noise, perturb = perturb_robust, trial = trial, cause = 'A', alternatives = ['B'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)	

		df.loc[idx, 'B_difference'] = w.difference_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', alternatives = ['A'], df = df, n_simulations = n_simulations_difference, animate = animate)

		if df.loc[idx, 'B_difference'] != 0: 
			df.loc[idx, 'B_how'] = w.how_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', df = df, animate = animate)
			df.loc[idx, 'B_whether'] = w.whether_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', df = df, n_simulations = n_simulations, animate = animate)
			df.loc[idx, 'B_sufficient'] = w.sufficient_cause(w = w, experiment = experiment, noise = noise, trial = trial, cause = 'B', alternatives = ['A'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)
			df.loc[idx, 'B_robust'] = w.robust_cause(w = w, experiment = experiment, noise = noise, perturb = perturb_robust, trial = trial, cause = 'B', alternatives = ['A'], target = 'E', df = df, n_simulations = n_simulations, animate = animate)

	df['participant'] = participant+1
	df = df*1 #logical to integer
	# print 'participant ' + str(participant+1) + ' done'
	# print df.to_string()

	if record_data:
		df.to_csv('results/3ball_results_noise_' + str(noise).replace(".", "_") + "_perturb_" + str(perturb_robust) + "_nsamples_" + str(n_simulations) + "_participant_" + str(participant+1) + '.csv',index=False)
