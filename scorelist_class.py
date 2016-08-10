# Written By Gabe Orlanski
import functions
import logging
import url_class


class ScoreList:
    def __init__(self):
        self.scores_array = []
        self.scores_tree = {}

    def add_score(self, _score, appendedscore = True):

        try:
            self.scores_tree[_score.left.id].add_score(_score)
        except KeyError:
            self.scores_tree[_score.left.id] = Shelf(_score)
        if appendedscore:
            self.scores_array.append(_score)

    def get_scores(self, **kwargs):
        if "url" in kwargs:
            return self.scores_tree[kwargs["url"].id]
        return self.scores_array

    def get_score(self, lvl_1, lvl_2):
        try:
            return self.scores_tree[lvl_1.id].get_score(url=lvl_2)
        except KeyError:
            logging.error("KeyError when trying to get the score for %s" % lvl_1.id + " and " + lvl_2.id)
            pass

    def specific_score_list(self, left, right):
        """
        :param left: The URL on the left
        :param right: The URL on the right
        :return: dict of the scores
        """

        return dict(left=[self.scores_tree[left][i] for i in self.scores_tree[left].keys()], right=[self.scores_tree[right][i] for i in self.scores_tree[right].keys()])

    def add_score_array(self, scores):
        temp_list = [None for i in range(len(scores+self.scores_array))]
        for i in range(len(self.scores_array)):
            temp_list[i] = self.scores_array[i]
        for i,z in zip(scores, range(len(scores))):
            temp_list[len(self.scores_array)+z] = scores[z]
            self.add_score(i, False)
        self.scores_array = temp_list

    def compare_scores(self, left, right):

        # Get the list of scores that have either the left or the right URL
        scores_to_iterate = self.specific_score_list(left, right)

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
            return sorted(self.scores_array)[0]
        except IndexError:
            return False

    def check_equal(self):
        try:
            iterator = iter(self.scores_array)
            first = next(iterator)
            return all(first == rest for rest in iterator)
        except StopIteration:
            return True


class Shelf:
    def __init__(self, first_book=None):
        try:
            self.books = [Book(first_book.right, 0, first_book)]
        except:
            self.books = []

    def add_score(self, book):
        if len(self.books) != 0:
            temp_book = Book(book.right, len(self.books)-1,book)
        else:
            temp_book = Book(book.right, 0, book)
        self.books.append(temp_book)

    def sort_scores(self):
        self.books = sorted(self.books)

    def get_book(self, **kwargs):
        if "pos" in kwargs:
            return self.books[kwargs["pos"]]
        elif "url" in kwargs:
            return self.books[self.books.index(kwargs["url"])]


class Book:
    """
    The book class serves as a backend method to hold the scores when they are in the "Shelf" this allows easy sorting of the Shelf based on the right url of the score
    """
    def __init__(self, url, pos, score):
        """
        :param url: The URL that is the "right" of the score
        :param pos: The Index of the book
        :param score: The "Pages" of the book, the actual info being stored
        """
        self.url = url
        self.pos = pos
        self.score = score

    def __eq__(self, other):
        if isinstance(other, url_class.URL):
            return self.url == other
        return self.url.id_num == other.url.id_num

    def __lt__(self, other):
        if isinstance(other, url_class.URL):
            return self.url < other
        return self.url.id_num < other.url.id_num

    def __gt__(self, other):
        if isinstance(other, url_class.URL):
            return self.url > other
        return self.url.id_num > other.url.id_num

    def __le__(self, other):
        if isinstance(other, url_class.URL):
            return self.url <= other
        return self.url.id_num <= other.url.id_num

    def __ge__(self, other):
        if isinstance(other, url_class.URL):
            return self.url >= other
        return self.url.id_num >= other.url.id_num