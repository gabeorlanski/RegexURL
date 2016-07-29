# Written By Gabe Orlanski

from url_class import URL
from score_class import Score


class ScoreList:
    def __init__(self):
        self.scores = []

    def addScore(self, _score):

        self.scores.append(_score)

    def getScores(self):
        return self.scores

    def getScore(self, url):
        for i in self.scores:
            if i.has_url(url):
                return i

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

        # Get the list of scores that have either the left or the right URL
        scores_to_iterate = self.specificScoreList(left, right)

        # Lists that will be used to iterate over
        left_list = scores_to_iterate["left"]
        right_list = scores_to_iterate["right"]

        # List that has a tuple of the values of the correpsonding score for both left and right
        combined_list = []

        # Basic ints to keep track of which of the two URLs has better scores
        left_greater = 0
        right_greater = 0

        if len(left_list) != scores_to_iterate[right_list]:
            raise ValueError("Length of the scorelist for the Left URL is not the same as that of the Right URL")
        for i in range(len(left_list)):
            for q in range(len(right_list)):
                if q.getOtherURL(right) == i.getOtherURL(left) and q.getOtherURL(right) is not None:
                    # Add a tuple to the list with the values. Position 0 represents the Left URL, Position 1 the Right
                    combined_list.append((i.value,q.value))
                    break

        # Go through the list of values, and see which is greater
        for i in combined_list:
            if i[0] >= i[1]:
                left_greater += 1
            else:
                right_greater += 1

        if left_greater >= right_greater:
            return 0
        else:
            return 1
