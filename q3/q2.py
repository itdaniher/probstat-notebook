def closest(target, collection) :
	#mad props to http://stackoverflow.com/questions/445782/finding-closest-match-in-collection-of-numbers
	return min((abs(target - i), i) for i in collection)[1]
def CredibleInterval(Pmf, p):
	#basically, go from pmf -> cdf and match for 50 \pm p in the cdf
	#make list "deConstructed to contain the raw info extracted from the PMF
	deConstructed = []
	#make code easy to read
	numVals = len(Pmf.getDict())
	#iterate through the dict
	for probability, value in Pmf.GetDict():
	#use the definition of PMF; PMF = {numOccurances/numVals:value}
		for i in xrange(probability*numVals):
			deConstructed.append(value)
	#make a CDF from the deconstructed list
	Cdf = MakeCdfFromList(deConstructed)
	#p is a percentage - convert to percentile via centering around fifty
	highPercentile=50+p/2.0
	#no promise of exact match - use "closest" function
	highPercentile=closest(highPercentile,CDF.ps*len(CDF.ps))
	lowPercentile=50-p/2.0
	lowPercentile=closest(lowPercentile,CDF.ps*len(CDF.ps))
	#return the value at high and low percentiles times the number of values
	return (Cdf.value(lowPercentile)*len(CDF.ps),Cdf.value(highPercentile)*len(CDF.ps))
