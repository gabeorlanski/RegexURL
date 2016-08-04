# Written By Gabe Orlanski
import time

from score_class import Score
from scorelist_class import ScoreList


class Group:
    def __init__(self, domain, subdomain):
        self.domain = domain
        self.subdomain = subdomain
        self.regex = ""
        # regexify()
        self.scores = ScoreList()
        self._url = []
        self.tree = dict(Name="Everything", Children=[])
        self.children = []

    def addUrls(self, urls):
        self._url = urls

    def addUrl(self, url):
        """
        :param url: the url to add
        :rtype: None
        """
        self._url.append(url)

    def getRegex(self):
        return self.regex

    def canCompress(self):
        if len(self._url) > 50:
            return True
        return False

    def generateScores(self):
        for i in range(len(self._url)):
            for x in range(1, len(self._url) - i):
                self.scores.addScore(Score(self._url[i], self._url[i+x], self._url[i].compareurls(self._url[i + x])))

    def addScore(self, score):
        self.scores.addScore(score)

    #@profile
    def splitUrlList(self, pbar_queue):
        # Find the two URLs the least similar, and make two new groups with them
        if self.scores.least_similar() is not False and self.canCompress() is not False and self.scores.checkEqual() is not True:
            lowest_score = self.scores.least_similar()
            left = lowest_score.left
            right = lowest_score.right
            if lowest_score.value == 100:
                return 1
            # Create the two child groups
            left_group = Group(lowest_score.left.domain, lowest_score.left.subdomain)
            right_group = Group(lowest_score.right.domain,lowest_score.right.subdomain)
            right_group.addUrl(right)
            left_group.addUrl(left)
            same_scores = 0
            # Iterate over the URLs in the group
            for url in self._url:

                # Check which of the two URLs the currently selected URL is more similar too
                # Then add it to that group
                if url != left and url != right:
                    try:
                        if self.scores.getScore(url,left) > self.scores.getScore(url,right):
                            left_group.addUrl(url)
                            left_group.addScore(self.scores.getScore(url, left))
                        elif self.scores.getScore(url,left) < self.scores.getScore(url,right):
                            right_group.addUrl(url)
                            right_group.addScore(self.scores.getScore(url, right))
                        else:
                            same_scores +=1
                    except:
                        pass
            t_1 = time.time()
            left_group.generateScores()
            right_group.generateScores()
            t_2 = time.time()
            self.children = [left_group, right_group]
            if same_scores != round(len(self._url)*.9):
                # Recursion it up
                for child in self.children:
                    if child.canCompress():
                        child.splitUrlList(pbar_queue)

    def getUrls(self):
        return self._url

