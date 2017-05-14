def percentile(scoreList, score):
	dic = {}
	for item in enumerate(scoreList): dic[item[1]] = float(item[0]+1)
	percentile = dic[score] / float(len(scoreList)) * 100.0
	return percentile

if __name__ == '__main__':
	import random
	scoreList = []
	for a in range(100):
		scoreList.append(int(random.random()*100))
	scoreList = list(set(scoreList))
	score = scoreList[len(scoreList)/2]
	print "the middle value of a randomly generated list of sorted, individual numbers should be around 50. this script calculates it to be ", percentile(scoreList, score)
