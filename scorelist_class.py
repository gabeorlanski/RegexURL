# Written By Gabe Orlanski
import functions


class ScoreList:
    def __init__(self):
        self.scores_array = []
        self.scores_tree = {}

    def addScore(self, _score, appendedscore = True):
        if _score.left.id in self.scores_tree:
            self.scores_tree[_score.left.id][_score.right.id] = _score
        else:
            self.scores_tree[_score.left.id] = {_score.right.id: _score}
        if _score.right.id in self.scores_tree:
            self.scores_tree[_score.right.id][_score.left.id] = _score
        else:
            self.scores_tree[_score.right.id] = {_score.left.id: _score}
        if appendedscore:
            self.scores_array.append(_score)

    def getScores(self, **kwargs):
        if "url" in kwargs:
            return self.scores_tree[kwargs["url"].id]
        return self.scores_array

    def getScore(self, lvl_1, lvl_2):
        try:
            return self.scores_tree[lvl_1.id][lvl_2.id]
        except KeyError:
            pass

    def specificScoreList(self, left, right):
        """
        :param left: The URL on the left
        :param right: The URL on the right
        :return: dict of the scores
        """

        return dict(left=[self.scores_tree[left][i] for i in self.scores_tree[left].keys()], right=[self.scores_tree[right][i] for i in self.scores_tree[right].keys()])

    def addScoreArray(self, scores):
        temp_list = [None for i in range(len(scores+self.scores_array))]
        for i in range(len(self.scores_array)):
            temp_list[i] = self.scores_array[i]
        for i,z in zip(scores, range(len(scores))):
            temp_list[len(self.scores_array)+z] = scores[z]
            self.addScore(i, False)
        self.scores_array = temp_list

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
                    combined_list.append((i.value, q.value))
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

    def least_similar(self):
        try:
            return functions.mergeSort(self.scores_array)[0]
        except IndexError:
            return False

    #@profile
    def checkEqual(self):
        try:
            iterator = iter(self.scores_array)
            first = next(iterator)
            return all(first == rest for rest in iterator)
        except StopIteration:
            return True