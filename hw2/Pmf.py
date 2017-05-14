#N.B. I'm a neophyte at using classes. Variable scope is still something I'm learning.
#dic = {val1: freq, val2: freq}
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

def Freq(hist, val):
	return hist.getFreq(val)

def Prob(pmf, val):
	return pmf.getProb(val)

def MakePmf(valList):
	hist = MakeHist(valList)
	pmf = Pmf()
	pmf.Normalize(hist.getDic())
	return pmf
