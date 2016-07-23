# Written By Gabe Orlanski

from url_class import URL
from score_class import score

class scorelist:

    def __init__(self, url):

        self.url = url
        self.scores = []
        self.compared = []

    def addScore(self, _score, _compared):

        self.scores.append(_score)
        self.compared.append(_compared)

    def getScores(self):
        return self.scores

    def getCompared(self):
        return self.compared

    def getScore(self, url):
        return self.scores[self.compared.index(url)]

    def compareScores(self, url):
        """
        :param url: Url you are comparing the scores of to, it is the right
        :param self: the url that has this score, it is the left
        :rtype: int 0 or 1
        """

        left = 0
        right = 0
        for i in range(len(self.compared)):
            if self.compared[i] is not url:
                _lscore = self.scores[i]
                _rscore = url.getScore(self.compared[i])
                if _lscore >= _rscore:
                    left += 1
                else:
                    right += 1
        if left >= right:
            return 0
        else:
            return 1