# Written By Gabe Orlanski

from url_class import URL

class group:
    def __init__(self, domain, subdomain): 
        self.domain = domain
        self.subdomain = subdomain
        self.regex = ""
        # regexify()
        self._url = []
    
    def addurl(self, url):
        self._url.append(url)
    
    
    
    def getregex(self):
        return self.regex
    
    def compareurllist(self):
        if len(self._url) > 10:
            for i in range(len(self._url)):
                print(self._url[i])
                for x in self._url[:len(self._url)-i]:
                    print(x)
                print("\n")