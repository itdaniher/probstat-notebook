#!/usr/bin/python
#Ian Daniher - 02-09-2010

import csv
from math import sqrt

def csvDict(file):
	tree = []
	dictList = []
#use the csv.reader object to make a csv object out of the contents of "file"
	csvReader = csv.reader(open(file,'r'))
#iterate through csvReader to construct a list of lists called "tree"
	for row in csvReader:
		tree.append(row)
	for limb in tree[1:]:
		dict = {}
		#iterate through the length of the first row
		for num in range(len(tree[0])):
			#if the object is *not* the first item, float it
			if num > 0:
				val = float(limb[num])
#if it is the first item, let it be
			else:
				 val = limb[num]
#construct a dictionary with the key of the num'th item in the first row of the csv
			dict[tree[0][num]] = val
#append that to dictlist
		dictList.append(dict)
	return dictList


def return800m(dictList):
	resultList = []
#make an iteration object for dictList, allowing single-command, non-distructive popping 
	iterVal=iter(dictList)
	for val in range(len(dictList)):
#append the value of the dictionary entry 'run800m' to resultList
		resultList.append(iterVal.next()['run800m'])
	return resultList

def MPS2MPH(resultList):
#1 meter per second is equal to 2.237 miles per hour
	resultList = [2.237*800/num for num in resultList]
	return resultList

def analyze(resultList):
#count number of items in list
	count=len(resultList)
#average value = sum / count
	mean=sum(resultList)/count
#do step one of stdev calcs
	resultList=[(num-mean)**2 for num in resultList]
#do step two fo stdev calcs
	stdDev=sqrt(sum(resultList)/(count-1))
	print "mean:", mean
	print "std:", stdDev

dictList = csvDict('heptathlon.csv')
resultList = return800m(dictList)
mphList = MPS2MPH(resultList)
analyze(mphList)
