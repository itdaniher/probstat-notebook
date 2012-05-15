#data-crunch script for reddit/wikipedia post/edit correlaation project
#all code below by Ian Daniher, written 2010-10-18 to 2010-10-21
import pickle
import scipy
import pylab
from scipy import stats
import Cdf
import Pmf
import datetime

def sort(cleanData, key):
	"""sort cleanData dictionary by a key"""
	return sorted(cleanData, key=lambda d: d[key])

def trim(cleanData, key, cutoff):
	"""returns a dictioanry with only items whose key is less than a cutoff value"""
	lambdaFunc = lambda x, cutoff: x < cutoff	
	data = cleanData
	cleanData = []
	for datum in data:
		if lambdaFunc(datum[key], cutoff):
			cleanData.append(datum)
	return cleanData

def standardScores(cleanData, key):
	"""return the standard scores of an element of cleanData"""
	vars = [d[key] for d in cleanData]
	meanVar = scipy.mean(vars)
	stdevVar = scipy.std(vars)
	vars = [(x - meanVar)/stdevVar for x in vars]
	return scipy.array(vars)

def pearsonsCorrelation(cleanData, key1, key2):
	"""wrapper for scipy.stats.pearsonr"""
	return stats.pearsonr([d[key1] for d in cleanData], [d[key2] for d in cleanData])


def getDataFromPickle(file=None):
	"""produces a cleaned list of data-point dictionaries from a pickled datafile"""
#if no file is specified, pull information from the 1000 most Popular
	if file == None:
		file = '1000mostPopular.pickle'
	rawData = pickle.load(open(file))
	cleanData = []
	for datum in rawData:
#don't process a datapoint if 
		if all([ datum['editsBefore'] != 0, datum['editsSince'] != 0]):
			cleanDatum = {}
			daysA = datetime.date(2010, 10, 19) - datum['created_utc']
			cleanDatum['daysA'] = daysA.days
			cleanDatum['name'] = datum['pstSince']['page']
			cleanDatum['editsB'] = datum['editsBefore']
			cleanDatum['editsA'] = datum['editsSince']
			cleanDatum['delta'] = cleanDatum['editsA'] - cleanDatum['editsB']
			cleanDatum['deltaNorm'] = float(cleanDatum['delta'])/cleanDatum['daysA']
			cleanDatum['editsBNorm'] = float(cleanDatum['editsB'])/cleanDatum['daysA']
			cleanDatum['moreEdits'] = cleanDatum['editsB'] < cleanDatum['editsA']
			cleanData.append(cleanDatum)
	return cleanData

pylab.ion()

####ALL FUNCTIONS BELOW SAVE PNGS####

def editIncreaseProbabilityByBinnedStartingEdits(cleanData):
	"""bear with me on this one.... 
this function plots the chance an article has more edits after being posted vs the starting edits.
code below isn't pretty, but the chart it produces is."""
	cleanData = sort(cleanData, 'editsB')
	editsB = [d['editsB'] for d in cleanData]
	colors = ["#3366FF","#6633FF","#CC33FF","#FF33CC","#FF3366","#FF6633","#FFCC33","#CCFF33","#66FF33","#33FF66","#33FFCC","#33CCFF","#003DF5","#002EB8","#F5B800","#B88A00"]
	numBins = 10
	moreThanBins = {}
	for i in range (1,numBins+1):
		low = len(editsB)*(i-1)/numBins
		high = len(editsB)*(i)/numBins-1
		dataName = "bin%iof%i" % (i, numBins)
		locals()[dataName] = cleanData[low:high]
		CDF = Cdf.MakeCdfFromList([d['deltaNorm'] for d in locals()[dataName]])
		sortedComparison = [d['moreEdits'] for d in locals()[dataName]]
		moreThanBins[editsB[low]] = scipy.mean(sortedComparison)
	pylab.clf()
	for i in range(len(moreThanBins)):
		pylab.bar(moreThanBins.keys()[i], moreThanBins.values()[i], color=colors[i], width=4)
	pylab.axis([0,200,0,1])
	pylab.xlabel(r'$edits_{beforePosting}$', fontsize=16)
	pylab.ylabel(r'chance of an item having more ${edits}_{afterPosting}$', fontsize=16)
	pylab.title('starting edits vs. edit increase probability', fontsize=24)
	pylab.savefig('editIncreaseProbabilityByBinnedStartingEdits.png')

def CDF(cleanData):
	"""plots a simple CDF representing the distribution of edits prior to an article being psoted"""
	pylab.clf()
	CDF = Cdf.MakeCdfFromList([d['deltaNorm'] for d in cleanData])
	pylab.plot(CDF.xs, CDF.ps, label='edits before posting')
	pylab.title(r'CDF $\Delta_{edits}$', fontsize=24)
	pylab.xlabel('edit count', fontsize=16)
	pylab.ylabel('percentile rank', fontsize=16)
	pylab.savefig('CDF.png')

def CDFByBins(cleanData):
	"""distributes the data into 5 equal-length bins, plots a CDF for each bin"""
	cleanData = sort(cleanData, 'editsB')
	colors = ["#3366FF","#6633FF","#CC33FF","#FF33CC","#FF3366","#FF6633","#FFCC33","#CCFF33","#66FF33","#33FF66","#33FFCC","#33CCFF","#003DF5","#002EB8","#F5B800","#B88A00"]
	editsB = [d['editsB'] for d in cleanData]
#	for key in cleanData[1].keys():
#		locals()[key] = [d[key] for d in cleanData]
	numBins = 5
	moreThanBins = {}
	pylab.clf()
	for i in range (1,numBins+1):
		low = len(editsB)*(i-1)/numBins
		high = len(editsB)*(i)/numBins-1
		dataName = "bin%iof%i" % (i, numBins)
		locals()[dataName] = cleanData[low:high]
		CDF = Cdf.MakeCdfFromList([d['deltaNorm'] for d in locals()[dataName]])
		pylab.plot(CDF.xs, CDF.ps, label=r'$ %i\ <\ edits_{beforePosting}\ <\ %i $' % (low,high))
	pylab.title('CDFs for %i bins' % numBins, fontsize=24)
	pylab.xlabel(r'normalized $\Delta_{edits}$', fontsize=16)
	pylab.ylabel('percentile rank', fontsize=16)
	pylab.legend(loc=4)
	pylab.savefig('CDFByBins.png')

def PMFByBins(cleanData):
	"""distributes the data into 10 equal-length bins, plots a PMF for each bin"""
	cleanData = sort(cleanData, 'editsB')
	colors = ["#3366FF","#FF6633","#CCFF33","#66FF33","#33FFCC","#33CCFF","#003DF5","#002EB8","#F5B800","#B88A00"]
	editsB = [d['editsB'] for d in cleanData]
#	for key in cleanData[1].keys():
#		locals()[key] = [d[key] for d in cleanData]
	numBins = 5
	moreThanBins = {}
	pylab.clf()
	for i in range (1,numBins+1):
		low = len(editsB)*(i-1)/numBins
		high = len(editsB)*(i)/numBins-1
		dataName = "bin%iof%i" % (i, numBins)
		locals()[dataName] = cleanData[low:high]
		deltaNorm = [d['deltaNorm'] for d in locals()[dataName] ]
		PMF = Pmf.MakePmfFromList(deltaNorm)
		pylab.plot(PMF.Render()[0][2:-2], PMF.Render()[1][2:-2], '*', color=colors[i])
		pylab.axvline(scipy.mean(deltaNorm), linewidth=3, label=r'$ \mu\ for\ %s $' %dataName, color=colors[i])
	pylab.title(r'binned PMFs for $\Delta_{edits}$', fontsize=24)
	pylab.xlabel(r'$\Delta_{edits}$', fontsize=16)
	pylab.ylabel(r'probability of $\Delta_{edits}$', fontsize=16)
	pylab.legend()
	pylab.savefig('PMFByBins.png')

def PMF(cleanData):
	"""displays an annotated PMF comparing editsA and editsB"""
	editsA = [d['editsA'] for d in cleanData]
	editsB = [d['editsB'] for d in cleanData]
	pylab.clf()
	PMF = Pmf.MakePmfFromList(editsB)
	pylab.plot(PMF.GetDict().keys(),PMF.GetDict().values(),'or',label=r'$ edits_{afterPosting} $')
	PMF = Pmf.MakePmfFromList(editsA)
	pylab.plot(PMF.GetDict().keys(),PMF.GetDict().values(),'ob',label=r'$ edits_{beforePosting} $')
	pylab.axvline(scipy.mean(editsA), color='r')
	pylab.axvline(scipy.mean(editsB), color='b')
	pylab.title(r'PMF for $edits_{beforePosting}$ and $edits_{afterPosting}$', fontsize=24)
	pylab.xlabel('edits', fontsize=16)
	pylab.ylabel('probability of edit-count', fontsize=16)
	pylab.legend()
	pylab.savefig('PMF.png')

def PMFTrimed(cleanData):
	"""displays annotated PMFs with values over 1000 eliminated"""
	pylab.clf()
	editsA = [d['editsA'] for d in cleanData]
	editsB = [d['editsB'] for d in cleanData]
	trim = lambda x, cutoff: x*(x < cutoff)
	editsA = [trim(x, 500) for x in editsA]
	editsB = [trim(x, 500) for x in editsB]
	PMF = Pmf.MakePmfFromList(editsB)
	pylab.plot(PMF.GetDict().keys(),PMF.GetDict().values(),'or',label=r'$ edits_{afterPosting} $')
	PMF = Pmf.MakePmfFromList(editsA)
	pylab.plot(PMF.GetDict().keys(),PMF.GetDict().values(),'ob',label=r'$ edits_{afterPosting} $')
	pylab.axvline(scipy.mean(editsA), color='r')
	pylab.axvline(scipy.mean(editsB), color='b')
	pylab.title(r'PMF for $edits_{beforePosting}$ and $edits_{afterPosting}$', fontsize=24)
	pylab.xlabel('edits', fontsize=16)
	pylab.ylabel('probability of edit-count', fontsize=16)
	pylab.legend()
	pylab.savefig('PMFTrimed.png')

def correlationVsCutoff(cleanData):
	pylab.clf()
	cleanData = sort(cleanData, 'daysA')
	daysA = [d['daysA'] for d in cleanData]
	daysA.reverse()
	correlCut = []
	for daysCutoff in daysA:
		dataPoint = {}
		trimmedData = trim(cleanData, 'daysA', daysCutoff)
		dataPoint['pearsons'] = pearsonsCorrelation(trimmedData, 'deltaNorm', 'editsA')[0]
		dataPoint['p-value'] = pearsonsCorrelation(trimmedData, 'deltaNorm', 'editsA')[1]
		dataPoint['length'] = len(trimmedData)
		dataPoint['cutoff'] = daysCutoff
		dataPoint['cutoffNorm'] = daysCutoff/float(max(daysA))
		correlCut.append(dataPoint)
	pylab.plot([d['cutoffNorm'] for d in correlCut], [d['pearsons'] for d in correlCut], label='Pearson\'s Correlation')
	pylab.plot([d['cutoffNorm'] for d in correlCut], [d['p-value'] for d in correlCut], label='p-value')
	pylab.axis([0,1,0,1])
	pylab.title("Pearson's Correlation Factor", fontsize=24)
	pylab.xlabel('percentileDays', fontsize=16)
	pylab.ylabel(r"Pearson's Factor for $\Delta_{edits}$ and $edits_{afterPosting}$", fontsize=16)
	pylab.legend()
	pylab.savefig('correlationVsCutoff.png')


if __name__ == '__main__':
	pylab.ion()
	cleanData = getDataFromPickle('1000mostPopular.pickle')
	correlationVsCutoff(cleanData)
	PMFTrimed(cleanData)
	PMF(cleanData)
	PMFByBins(cleanData)
	CDFByBins(cleanData)
	CDF(cleanData)
	editIncreaseProbabilityByBinnedStartingEdits(cleanData) 



#stats.morestats.bayes_mvs([d['deltaNorm'] for d in cleanData], alpha=.1)
#stats.chisquare([d['deltaNorm'] for d in cleanData])

