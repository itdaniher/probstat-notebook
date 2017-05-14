#!/usr/bin/python
from math import sqrt
from scipy import std, mean
resultList = [line.strip('\n').split(',')[6] for line in open(raw_input("what file? ")).readlines()][1:]
resultList = [2.237*800/float(num) for num in resultList]
print ("mean", mean(resultList)), ("std", std(resultList))
