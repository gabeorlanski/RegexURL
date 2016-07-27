# Written By Gabe Orlanski

from url_class import URL
from score_class import Score


class ScoreList:
    def __init__(self, group=None):
        """
        :param group: If the ScoreList is for a group, pass the group it is for
        """
        self.group = group
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

    def specificScoreList(self, left, right):
        """
        :param left: The URL on the left
        :param right: The URL on the right
        :return: dict of the scores
        """

        rtrn_dict = dict(left=[], right=[])

        for score in self.scores:
            if score.has_url(left):
                rtrn_dict["left"].append(score)
            elif score.has_url(right):
                rtrn_dict["right"].append(score)
        return rtrn_dict

    def compareScores(self, left, right):
        scores_to_iterate = self.specificScoreList(left, right)

        for i in range(len(self.scores)):
            # TODO Have this iterate over the dictionary in scores_to_iterate
            # TODO Implement way to make sure I am looking at the score from the comparison of the same URL
            # TODO Get the value from the score
            print("PLACEHOLDER")
        if left >= right:
            return 0
        else:
            return 1
