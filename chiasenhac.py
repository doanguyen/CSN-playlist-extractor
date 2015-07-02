import cookielib, urllib, urllib2, time,sys
from bs4 import BeautifulSoup

account= {'username':'bukdotcom','password':'123456'}

class csn():
	"""
	Retrieve single-song/playlist from chiasenhac.com
	"""
	def __init__(self,argv):
		if len(argv)<3:
			print """
Using: python chiasenhac.py playlist option
       option: best/m4a/mp3/mobile
		""";exit()
		self.cookies = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(debuglevel=0),urllib2.HTTPSHandler(debuglevel=0),urllib2.HTTPCookieProcessor(self.cookies))
		lists = self.playlist(argv[1])
		if (len(lists) > 0):
			print "There are %s song(s) in the playlist, waiting for the download link." %(len(lists))
			self.login(account)
			final = self.getlink(lists)		
			if argv[2] == "best":
				self.confuse(final,3) #flac
			elif argv[2] == "m4a":
				self.confuse(final,2) # 500kbps
			elif argv[2] == "mp3":
				self.confuse(final,1) # 320 kbps
			elif argv[2] == "mobile":
				self.confuse(final,0) # 32 kbps
			else:
				self.confuse(final,3) #flac
		else:
			print "Wrong link"
		exit()
	def playlist(self,link):
		response = self.opener.open(link)
		soup = BeautifulSoup(response.read(), 'html.parser').find(id="playlist").find_all('a')
		single_song = []
		for link in soup:
			if "download" in link.get("href"):
				single_song.append(link.get("href"))
		return single_song
	def getlink(self,links):
		total = dict();i = 1
		for link in links:
			html = self.opener.open(link).read()
			download_link = BeautifulSoup(html, 'html.parser').find(id="downloadlink")
			song = []
			for link in download_link.find_all('a'):
				song.append(link.get('href'))
			pass
			total[i] = filter(None,song);i+=1
		return total
		pass
	def login(self,account):
		url = 'http://chiasenhac.com/login.php'
		values = {'username' : account['username'],'password' : account['password'],'autologin' : 'on','redirect' : '','login' : "%C4%90%C4%83ng+nh%E1%BA%ADp"}
		data = urllib.urlencode(values)
		return self.opener.open(url, data)
		pass
	def confuse(self,y,z):
		xx = 1
		for x in y:
			print y[xx][z]; xx +=1;
if __name__ == '__main__':
	csn(sys.argv)