#!/usr/bin/python
# coding=utf-8

import random
import matplotlib.pyplot
import Cdf

'''Exercise 3  
The random module provides paretovariate, which generates random values from a Pareto distribution. It takes a parameter for α, but no parameter for xm. What is the default value for xm?
#default for xm=1
Write a wrapper function named paretovariate that takes α and xm as parameters and uses random.paretovariate to generate values from a two-parameter Pareto distribution.

Use your function to generate a sample from a Pareto distribution. Compute the CCDF and plot it on a log-log scale. Is it a straight line? What is the slope?'''

samples = []
paretoCdf = {}

alpha = 1.5
x_min = 1

def paretovariate(alpha,x_min):
	return x_min*random.paretovariate(alpha)

for num in range(1000):
	samples.append(paretovariate(alpha, x_min))

itersamples = iter(samples)

for num in range(len(samples)):
	x = itersamples.next()
	ccdf = 1-(x/x_min)**(-alpha)
	paretoCdf[x] = ccdf
#...if you plot logy versus logx, it should look like a straight line with slope −α and intercept −α logxm...
matplotlib.pyplot.loglog(paretoCdf.values(), paretoCdf.keys())
matplotlib.pyplot.show()
