from pomegranate import *
import csv, random
import numpy as np

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
    observations += [int(row[1]) - 1]

# Train
trans, ems = p.forward_backward(observations[:20])

# Replace all -inf with 0
qwer = []
for tt in ems:
    m = []
    for t in tt:
        d = t
        if np.isinf(t):
            d = 0
        m += [d]
    qwer += [m]
ems = qwer

# convert to distribution
new_emissions = []
for row in ems:
    t = {}
    for (i, val) in enumerate(row):
        t[i] = float(val)
    new_emissions += [DiscreteDistribution(t)]

# Converting to NP array
new_transitions = []
for row in trans:
    t = list(map(float, row))
    new_transitions += [t]
new_transitions = np.array(new_transitions)

#############
pp = HiddenMarkovModel.from_matrix(new_transitions, new_emissions, states)
#############


