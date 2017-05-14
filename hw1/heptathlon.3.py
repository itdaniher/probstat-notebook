#!/usr/bin/python
#Ian Daniher - 02-09-2010

import csv
from scipy import sqrt

def csvDict(file):
	tree = []
	dictList = []
	csvReader = csv.reader(open(file,'r'))
#use the csv.reader object to make a csv object out of the contents of "file"
	for row in csvReader:
		tree.append(row)
#iterate through csvReader to construct a list of lists called "tree"
	for limb in tree[1:]:
		dict = {}
		for num in range(len(tree[0])):
#iterate through the length of the first row
			if num > 0:
				val = float(limb[num])
#if the object is *not* the first item, float it
			else:
				 val = limb[num]
#if it is the first item, let it be
			dict[tree[0][num]] = val
#construct a dictionary with the key of the num'th item in the first row of the csv
		dictList.append(dict)
#append that to dictlist
	return dictList


def return800m(dictList):
	resultList = []
	iterVal=iter(dictList)
#make an iteration object for dictList, allowing single-command, non-distructive popping 
	for val in range(len(dictList)):
		resultList.append(iterVal.next()['run800m'])
#append the value of the dictionary entry 'run800m' to resultList
	return resultList

def MPS2MPH(resultList):
	resultList = [2.237*800/num for num in resultList]
#1 meter per second is equal to 2.237 miles per hour
	return resultList

def analyze(resultList):
	num=len(resultList)
	tmpList = []
	mean=sum(resultList)/num
	iterVal=iter(resultList)
	for val in range(num):
		tmpList.append((iterVal.next()-mean)**2)
	stdDev=sqrt(sum(tmpList)/(num-1))
	print "mean:", mean
	print "std:", stdDev


dictList = csvDict('heptathlon.csv')
resultList = return800m(dictList)
mphList = MPS2MPH(resultList)
analyze(mphList)
