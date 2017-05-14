def	 ChiSquaredTest(Hist, Pmf):
	sumMe=[]
	#divide through by sum(freq), normalize to go from frequencies to probabilities
	observed = MakePmfFromHist(Hist)
	expected = Pmf
	#make sure both have the same values - zero values are OK!
	for probability, value in observed.GetDict():
		if value not in expected.getDict().keys():
			expected.Incr(value, 0)
	for probability, value in expected.GetDict():
		if value not in observed.getDict().keys():
			observed.Incr(value, 0)
	#error checking
	if len(expected.GetDict()) != len(observed.GetDict()):
		print("you screwed up and now your code isn't going to work. way to go.")
	#shouldn't be needed
	observed.Normalize()
	#shouldn't be needed
	expected.Normalize()
	#begin iteration to compute chi-square statistic
	for probability, value in expected.GetDict()
		numerator = (observed.Prob(value)-expected.Prob(value))**2
		denomenator = expected.Prob(value)
		sumMe.append(numerator/denomenator)
	return sum(sumMe)
