import percentile

class Cdf:
	def __init__(self, xs=None, ps=None):
		if xs == None:
			xs = []
		self.xs = xs
		if ps == None:
			ps = []
		self.ps = xs
	def Prob(self, numList, num):
		return percentile.percentile(numList, num)/100.0
	def Value(self, p):
		dic = {}
		if p == 0.0: return self.xs[0]
		if p == 1.0: return self.xs[-1]
		for item in enumerate(self.xs):
			dic[item[1]] = item[0]+1
		print dic
		return dic[p]
	def getDic(self):
		return dict(zip(self.xs, self.ps))
	def Render(self):
		return (self.xs, self.ps)

class Hist:
	def __init__(self, dic=None):
		if dic == None:
			dic = {}
		self.dic = dic
	def incrementFreq(self, val):
		self.dic[val] = self.dic.get(val, 0) + 1
	def getFreq(self, val):
		return self.dic.get(val, 0)
	def getDic(self):
		return self.dic

def MakeHist(valList):
	hist = Hist()
	for val in valList:
		hist.dic[val] = float(hist.getFreq(val) + 1)
	return hist

class Pmf:
	def __init__(self, dic=None):
		if dic == None:
			dic = {}
		self.dic = dic
	def Normalize(self, histDic):
		count = float(sum(histDic.values()))
		for x in histDic.keys():
			self.dic[x] = histDic[x] / count
	def getDic(self):
		return self.dic
	def getProb(self, val):
		return self.dic.get(val, 0)

def MakePmf(valList):
	hist = MakeHist(valList)
	pmf = Pmf()
	pmf.Normalize(hist.getDic())
	return pmf

def MakeCdf(valList):
	pmf = MakePmf(valList).getDic()
	cdf = Cdf()
	cdf.xs = pmf.keys()
	oldNum = 0
	for num in pmf.values():
		num = oldNum + num
		cdf.ps.append(num)
		oldNum = num
	return cdf
