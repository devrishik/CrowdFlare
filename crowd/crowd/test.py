import csv, random
import numpy as np
from crowd.markov import HMM, Distribution
from crowd.hmmestimate import HMM as HMM2


np.set_printoptions(suppress=True)

states = [x for x in range (1, 21)]

reader = csv.reader(open('/Users/bizzz/Desktop/transitional_probability.csv'))
transitions = {}
for row in reader:
    key = int(row[0])
    if key in transitions:
        pass
    transitions[key] = Distribution(categories=map(float, row[1:]), k=random.random())

reader = csv.reader(open('/Users/bizzz/Desktop/emission probability.csv'))
emissions = {}
for row in reader:
    key = int(row[0])
    value = Distribution(categories=map(float, row[1:]), k=random.random())
    if key in emissions:
        pass
    emissions[key] = value

reader = csv.reader(open('/Users/bizzz/Desktop/training.csv'))
states = []
observations = []
for row in reader:
    states += [float(row[0])]
    observations += [int(row[1]) - 1]
observations = Distribution(categories=observations, k=random.random())

# h=HMM(states, emissions)

reader = csv.reader(open('/Users/bizzz/Desktop/training.csv'))
seq = []
for row in reader:
    key = int(row[0])
    value = int(row[1])
    seq += [(key, value)]

# h.Train(seq)

hmm = HMM2()

# initial states probabilities
hmm.pi = np.array([0.05 for x in range(1, 21)], dtype='f')

reader = csv.reader(open('/Users/bizzz/Desktop/transitional_probability.csv'))
transitions = []
for row in reader:
    # t = [int(row[0])]
    t = []
    t += list(map(float, row[1:]))
    transitions += [t]
transitions = np.array(transitions)

reader = csv.reader(open('/Users/bizzz/Desktop/emission probability.csv'))
emissions = []
for row in reader:
    # t = [int(row[0])]
    t = []
    t += list(map(float, row[1:]))
    emissions += [t]
emissions = np.array(emissions)

reader = csv.reader(open('/Users/bizzz/Desktop/training.csv'))
# states = []
observations = []
for row in reader:
    # states += [float(row[0])]
    observations += [int(row[1]) - 1]
observations = np.array(observations)

hmm.A = transitions
hmm.B = emissions

hmm.train(observations, 0.00001, graphics=True)
