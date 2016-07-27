# Written By Gabe Orlanski

from url_class import URL


class Group:
    def __init__(self, domain, subdomain, tree=None):
        self.domain = domain
        self.subdomain = subdomain
        self.regex = ""
        # regexify()
        self._url = []
        self.tree = dict(Name="Everything", Children=[])

    def addurl(self, url):
        """
        :param url: the url to add
        :rtype: None
        """
        self._url.append(url)

    def getregex(self):
        return self.regex

    @staticmethod
    def cancompress(urls):
        if len(urls) > 10:
            return True
        return False

    @staticmethod
    def spliturllist(urllist):
        """
        :param urllist: List of URLs,
        :return:
        """
        totalscores = []
        for i in range(len(urllist)):
            scores = []
            for x in range(1, len(urllist) - i):
                scores.append(urllist[i].compareurls(urllist[i + x]))
