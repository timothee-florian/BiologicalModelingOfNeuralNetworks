import hopfield 
# reload(hopfield)
# import multiprocessing
import random as rand
import numpy as np
import matplotlib.pyplot as plt
# import pylab as pl
import time
import os

FLAG_progress = False # Show process progress (True or False)
FLAG_plot = False

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

plt.close('all')

# -------------------------------------
# -------------------------------------
# -------------------------------------

start = time.time()

# Exercise 1

print('\nEXERCISE 1\n===========\n')

# Run
K = 100 # Number of times the algorithm is run for cross-validations

# Network size
N = 100 # size of the network, i.e. if N=10 it will consists of 10x10 pixels

# Random patterns
P = range(1,30+1,1) # Total number of patterns that will be stored
ratio = 0.5 # probability of a pixel being 1 instead of -1

# Updates
decay = 1.0

# Steps
Z = 1000 # Number of storage/recall iterations
c = 5

# Storage and recalls
P_s = 0.8 # Probability ps for storage
P_f = 0.1 # ratio of flipped pixels

with open(os.path.join('"Exercises', 'Exercise1.py'), 'r') as f:
    exec(f.read())

# -------------------------------------
# -------------------------------------
# -------------------------------------

# Exercise 2

print('\nEXERCISE 2\n===========\n')

# Network size
N = range(100,1000+1,10) # size of the network, i.e. if N=10 it will consists of 10x10 pixels

# Random patterns
ratio = 0.5 # probability of a pixel being 1 instead of -1

# Updates
decay = 1.0

# Steps
Z = 1000 # Number of storage/recall iterations
c = 5

# Storage and recalls
P_s = 0.8 # Probability ps for storage
P_f = 0.1 # ratio of flipped pixels

# Exercise parameters
error_max = 0.05
P_init = 27

with open(os.path.join('"Exercises', 'Exercise2.py'), 'r') as f:
    exec(f.read())

# -------------------------------------
# -------------------------------------
# -------------------------------------

# Exercise 3

print('\nEXERCISE 3\n===========\n')

# Network size
N = 100 # size of the network, i.e. if N=10 it will consists of 10x10 pixels

# Random patterns
p = 100 # Total number of patterns that will be stored
ratio = 0.5 # probability of a pixel being 1 instead of -1

# Updates
Decay = range(0,1000+1,1) # Decay multiplied by resolution
resolution = 0.001 # Multiplied to the values of Decay

# Steps
Z = 1000 # Number of storage/recall iterations
c = 5

# Storage and recalls
P_s = 0.8 # Probability ps for storage
P_f = 0.1 # ratio of flipped pixels

# Exercise parameters
T_window = 20
m = 5

with open(os.path.join('"Exercises', 'Exercise3.py'), 'r') as f:
    exec(f.read())

# -------------------------------------
# -------------------------------------
# -------------------------------------

# Exercise 4

print('\nEXERCISE 4\n===========\n')

# Network size
N = 100 # size of the network, i.e. if N=10 it will consists of 10x10 pixels

# Random patterns
p = 100 # Total number of patterns that will be stored
ratio = 0.5 # probability of a pixel being 1 instead of -1

# Updates
Decay = range(0,1000+1,1) # Decay multiplied by resolution
resolution = 0.001 # Multiplied to the values of Decay

# Steps
Z = 1000 # Number of storage/recall iterations
c = 5

# Storage and recalls
P_s = 0.8 # Probability ps for storage
P_f = 0.1 # ratio of flipped pixels

# Exercise parameters
T_window = 20
M = range(2,15+1,1)

with open(os.path.join('"Exercises', 'Exercise4.py'), 'r') as f:
    exec(f.read())

# -------------------------------------
# -------------------------------------
# -------------------------------------

end = time.time()
print('Elapsed time:', end-start, 'seconds')