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

    def addUrl(self, url):
        """
        :param url: the url to add
        :rtype: None
        """
        self._url.append(url)

    def getRegex(self):
        return self.regex

    @staticmethod
    def canCompress(urls):
        if len(urls) > 10:
            return True
        return False

    def generateScores(self):
        totalscores = []
        for i in range(len(self._url)):
            scores = []
            for x in range(1, len(self._url) - i):
                scores.append(self._url[i].compareurls(self._url[i + x]))
                return totalscores

    @staticmethod
    def splitUrlList(urllist):
        """
        :param urllist: List of URLs,
        :return:
        """
        # TODO Make the class' score list
        # TODO Make a way for this method to access the class' score list
        # TODO Figure out either recursion method or some other method to keep shrinking the group until a certain point
        # TODO Use the Dictionary Tree method to store the subgroups
        # TODO Finish this method
        print("Im A placeholder")
