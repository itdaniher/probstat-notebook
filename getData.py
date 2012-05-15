#data-collection script for reddit/wikipedia post/edit correlation project
#all code below by Ian Daniher, written 2010-10-16 to 2010-10-18

import reddit
import urllib
import re
import datetime
import pickle
import string

#made a reddit account for thsi project
#redditUser="CompProbStat"
#redditPassword =redditUser

#set today's date
dtNow = datetime.date.today()

#create reddit session
r = reddit.Reddit()
#login
#r.login(user=redditUser, password=redditPassword)

#select 'wikipedia' subreddit
sr = r.get_subreddit('wikipedia')

goodItems = []

#get the 1000 newest items
items = sr.get_top(time="all", limit=1000)
#make sure the items are en.wikipedia, not another wiki
for item in items:
	if re.match('http://en.wikipedia.org', item.url):
		goodItems.append(item.__dict__)

i = 0

#function to return a wikipedia page's edit history as a list of lists from the post-variables
def getCSV(pstInfo):
#use try/except to failsafe
	try:
#urlencode post-variables and make sure there are no weird chars in here
		urlEncoded = ''.join(s for s in urllib.urlencode(pstInfo) if s in string.printable)
#get the url-encoded csv-format information
		quoted = urllib.urlopen("http://toolserver.org/~daniel/WikiSense/Contributors.php?", urlEncoded).read()
	except:
		print "getCSV error"
		quoted = 'failed'
#decode and correct for plus-sign space sanitization
	unquoted = urllib.unquote(quoted).replace("+", " ")
#make sure there are no weird chars in here
	stripped = ''.join(s for s in unquoted if s in string.printable)
#make a tree from the csv-string using list comprehensions
	treed = [ row.split(',') for row in stripped.split("\r\n") ]
	return treed

i = 0

#itrate through en.wikipedia posts
for goodItem in goodItems:
#get the title of the wikipedia page from the reddit post
	wikiKey = goodItem["url"].split('/')[-1]
#assemble the information needed to get edit history
	pstInfo = {"wikilang":"en", "wikifam":".wikipedia.org", "page":wikiKey, "since":"", "until":"", "order":"-edit_count", "max":"0", "order":"-edit_count", "format":"csv"}
#make a datetime object from the seconds-since-epoch timestamp of the reddit post
	goodItem["created_utc"] = datetime.date.fromtimestamp(goodItem["created_utc"])
#determine number of days since page was posted to reddit
	tDelta = goodItem["created_utc"] - dtNow
#format time appropriately for edit history
	pstInfo["since"] = goodItem["created_utc"].strftime("%Y-%m-%d")
	pstInfo["until"] = dtNow.strftime("%Y-%m-%d")
#get edit history information
	goodItem["infoSince"] = getCSV(pstInfo)
#determine number of edits
	goodItem["editsSince"] = len(goodItem["infoSince"])-1
#save raw history as metadata
	goodItem["pstSince"] = pstInfo
#print out statistics to help with debugging
	print "%i a: between %s and %s, %s edits were made." % (i, str(pstInfo["since"]), str(pstInfo["until"]), str(goodItem["editsSince"]))
#get normalization information - how many edits in the chunk of time prior to posting equal in magnitude to between post and now
	pstInfo["since"] = tDelta + goodItem["created_utc"]
	pstInfo["since"] = pstInfo["since"].strftime("%Y-%m-%d")
	pstInfo["until"] = goodItem["created_utc"].strftime("%Y-%m-%d")
	goodItem["infoBefore"] = getCSV(pstInfo)
	goodItem["pstBefore"] = pstInfo
	goodItem["editsBefore"] = len(goodItem["infoBefore"])-1
	print "%i b: between %s and %s, %s edits were made." % (i, str(pstInfo["since"]), str(pstInfo["until"]), str(goodItem["editsBefore"]))
#purge the session information
	del goodItem["reddit_session"]
#sanitize the title
	goodItem["title"] = ''.join(s for s in goodItem["title"] if s in string.printable[:-5])
#replace item in goodItems
	goodItems[i] = goodItem
#failsafe pickleing
	try:
		f = open('.picklefile','w')
		pickle.dump(goodItems[:i], f)
		f.close()
	except:
		print "pickle error"
	i += 1
