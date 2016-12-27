import cookielib, urllib, urllib2, time,sys
from bs4 import BeautifulSoup
import re

account = {'username':'bukdotcom','password':'123456'}
qualityMap = {'best': 6, 'm4a': 5, 'mp3': 3, 'mobile': 1}

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
        quality = qualityMap[argv[2]]
        if (len(lists) > 0):
            print "There are %s song(s) in the playlist, waiting for the download link." %(len(lists))
            self.login(account)
            downloadLinks = self.getlink(lists, quality)
            self.showLinks(downloadLinks)
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

    def getlink(self, links, quality):
        result = []
        for link in links:
            html = self.opener.open(link).read()
            document = BeautifulSoup(html, 'html.parser')
            f = open("test.txt", "w")
            f.write(document.prettify().encode('utf-8'))
            for script in document.find_all('script', type="text/javascript"):
                for line in str(script.encode('utf-8')).split('\n'):
                    pattern = re.compile(ur'<a href="(.*)" onmouseover.*Link Download (\d)', re.UNICODE)
                    data = pattern.search(line)
                    if (data):
                        linkDownload = data.group(1)
                        fileType = int(data.group(2))
                        if (quality == fileType):
                            result.append(linkDownload)
                            break
        return result

    def showLinks(self, links):
        for link in links:
            print(link)

    def login(self,account):
        url = 'http://chiasenhac.vn/login.php'
        values = {'username' : account['username'],'password' : account['password'],'autologin' : 'on','redirect' : '','login' : "%C4%90%C4%83ng+nh%E1%BA%ADp"}
        data = urllib.urlencode(values)
        return self.opener.open(url, data)

if __name__ == '__main__':
    csn(sys.argv)
