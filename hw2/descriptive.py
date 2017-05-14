import thinkstats

def testMean():
	import random
	testList = []
	for num in range(1000):
		testList.append(random.random())
	print "if this is working correctly,", thinkstats.Mean(testList), "should be about .5"

def testVar():
	import numpy
	pumpkins = [1, 1, 1, 3, 3, 591]
	print "according to numpy, the variance is", numpy.var(pumpkins), "according to Var(), the variance is", thinkstats.Var(pumpkins)

import Pmf

def testPmf():
	import random
	testList = []
	for num in range(100):
		testList.append(int(random.random()*10))
	pmf = Pmf.MakePmf(testList)
	dic = pmf.getDic()
	print "the sum of the pmf of 100 randomly generated numbers should be 1.0. this code calculates it to be", sum(dic.values())

