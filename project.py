import reddit
import pycurl, urllib


redditUser="CompProbStat"
redditPassword =redditUser

r = reddit.Reddit()
r.login(user=redditUser, password=redditPassword)


class response:
#this class is needed to handle pycurl's WRITEFUNCTION gracefully
    def __init__(self):
        self.contents = ''
    def fill(self,buffer):
        self.contents = self.contents + buffer
    def clear(self):
        self.contents = ''
resp = response()

c = pycurl.Curl()
c.setopt(pycurl.URL, "http://toolserver.org/~daniel/WikiSense/Contributors.php")
c.setopt(pycurl.POST, 1)
UA = "ITD - CompProbStat Scraper"
c.setopt(pycurl.USERAGENT, UA)
pstInfo = {"wikilang":"en","wikifam":".wikipedia.org","page":"Africa","since":"2010-10-01","until":"","grouped":"on","order":"-edit_count","max":"100","order":"-edit_count","format":"tsv"}
c.setopt(pycurl.POSTFIELDS, urllib.urlencode(pstInfo))
c.setopt(pycurl.WRITEFUNCTION, resp.fill)
c.setopt(pycurl.WRITEFUNCTION, resp.fill)
c.perform()
resp.contents

