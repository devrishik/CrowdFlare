import csv, random
import numpy as np

from .models import HMM

from pomegranate import *, DiscreteDistribution, HiddenMarkovModel

# initial states probabilities
states = np.array([0.05 for x in range(1, 21)])

reader = csv.reader(open('/Users/bizzz/Desktop/transitional_probability.csv'))
transitions = []
for row in reader:
    t = list(map(float, row[1:]))
    transitions += [t]
transitions = np.array(transitions)

reader = csv.reader(open('/Users/bizzz/Desktop/emission probability.csv'))
emissions = []                                
for row in reader:
    t = {}
    for (i, val) in enumerate(row):
        val = float(val)
        if i>0:
            t[i-1] = val
    emissions += [DiscreteDistribution(t)]

############
p = HiddenMarkovModel.from_matrix(transitions, emissions, states)
############

# Observations
reader = csv.reader(open('/Users/bizzz/Desktop/training.csv'))
observations = []
for row in reader:
    observations += [((int(row[0]) - 1), (int(row[1]) - 1))]

# Train
trans, ems = p.forward_backward(observations[:20])



#############
pp = HiddenMarkovModel.from_matrix(new_transitions, new_emissions, states)
#############

def gold_ratio():
	'''
	return the gold ratio from the latest model
	'''
	return 0.2

def new_model(observations):
	'''
	Create a new model with new Observations
	'''
	pass
