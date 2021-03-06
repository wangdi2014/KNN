#!/usr/bin/env python
# -*- coding: utf-8 -*-
##################################### Help ####################################
"""Simple KNN implementation
Usage:
  knn.py [-cn]
  knn.py --help
Options:
  -c                          Classification mode
  -n                          Normalize each column
  -h --help                   Show this screen.
"""


################################### Imports ###################################
from docopt import docopt
import numpy as np
import random
import matplotlib.pyplot as plt

################################## Functions ##################################

################################### Classes ###################################
class KNN:
	"""A K-nearest neighbors regression"""
	
	def __init__(self, pts, c):
		self.points = pts
		self.classif = c
		if c:
			self.maxlabel = int(max(data[self.points,10]))

	def predict(self, pt):
		dist = np.array([np.linalg.norm(data[refPoint,1:10] - data[pt,1:10]) for refPoint in self.points])
		dist_sort = dist.argsort()
		nearest_points = [self.points[i] for i in dist_sort[:K]]
		# Classification
		if self.classif:
			labCount = np.empty(self.maxlabel+1)
			for i in xrange(self.maxlabel+1):
				labCount[i] = list(data[nearest_points,10]).count(i)
			return (-labCount).argsort()[0]
		# Regression
		else:
			return sum(data[nearest_points,10])/K
		


##################################### Main ####################################
# Seed for reproductibility
random.seed(1)

# Import user input
arguments = docopt(__doc__)
DATA_FILE_NAME = "/home/koala/Documents/Scripts/KNN/KNN/glass.data"
NB_CROSSVAL = 10
NORM = arguments["-n"]
CLASSIF = arguments["-c"]

# Load data
data_file = open(DATA_FILE_NAME)
data = data_file.readlines()
data = np.array([line[:-1].split(",") for line in data], dtype=np.float64)
# Shuffle the data
neworder = range(len(data))
random.shuffle(neworder)
data = data[neworder,:]

# Normalize the data if needed
if NORM:
	for i in xrange(1,10):
		data[:,i] = (data[:,i] - np.mean(data[:,i]))/np.sqrt(np.var(data[:,1]))

print(data)

meanSSE = []
meanAccuracy = []
# Number of neighbors considered
for K in xrange(1,26):
	# Ten cross validation
	training_length = len(data)/NB_CROSSVAL
	KNNs = []
	SSE = []
	accuracy = []
	
	for i in xrange(NB_CROSSVAL):
		test_indices = range(training_length*i, training_length*(i+1))
		training_indices = [k for k in range(len(data)) if k not in test_indices]
		KNNs.append(KNN(training_indices, CLASSIF))
		predictions = np.array([KNNs[i].predict(j) for j in test_indices])
		expected = np.array([data[j,10] for j in test_indices])
		SSE.append(sum((predictions - expected)**2))
		accuracy.append(sum(predictions == expected)/float(len(test_indices)))
	meanSSE.append(sum(SSE)/NB_CROSSVAL)
	meanAccuracy.append(sum(accuracy)/NB_CROSSVAL)
print meanSSE
plt.plot(range(1,26), meanSSE)
plt.xlabel('K')
plt.ylabel('Mean SSE')
plt.show()
print meanAccuracy
plt.plot(range(1,26), meanAccuracy)
plt.xlabel('K')
plt.ylabel('Mean perfect accuracy')
plt.show()
