def Mean(numList):
	numList = map(float, numList)
	return sum(numList)/len(numList)
def Var(numList):
	numList = map(float, numList)
	mean = Mean(numList)
	numsToSum = []
	for num in numList:
		num = num - mean
		numsToSum.append(num**2)
	sigmaSquared = sum(numsToSum) / float(len(numList))
	return sigmaSquared
