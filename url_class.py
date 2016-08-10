"""
Written By Gabe Orlanski
This purpose of this class is to allow the comparison and storage of URLs for clustering them into groups
"""
import logging


class URL:
    def __init__(self, domain, subdomain, fullURL, filepath=None, urlparams=None, id=None):
        """
        :param domain: Domain of the url (String)
            example: "reddit.com" in www.reddit.com/r/test/ex.js;name=Hi
        :param subdomain: Subdomain of the url (String)
            example: "www" in www.reddit.com/r/test/ex.js;name=Hi
        :param filepath: Filepath of the domain. Defaults to none when there is no file path (String)
            example: "/r/test/ex.js" in www.reddit.com/r/test/ex.js;name=Hi
        :param urlparams: The parameters of the script the URL calls. Defaults to None when there is no script (String)
            example: "name=Hi" in www.reddit.com/r/test/ex.js;name=Hi
        :return: None
        """
        self.id = id
        self.id_num = int(id.split("d")[1])
        self.full_url = fullURL
        self.domain = domain
        self.domain_spilt = self.domain.split(".")
        self.subdomain = subdomain
        if filepath is not None:
            self.path = filepath.split(";")[0]
            self.path_split = filepath.split(";")[0].split("/")
        else:
            self.path = None
            self.path_split = None
        if urlparams is not None:
            self.params = urlparams
            self.params_split = urlparams.split(";")
        else:
            self.params = None
            self.params_split = None
        try:
            if len(self.path_split[-1].split(".")) > 1:
                self.filetype = self.path_split[-1].split(".")[1]
                self.file = self.path_split[-1].split(".")[0]
            else:
                self.filetype = None
                self.file = self.path_split[-1]
        except:
            self.filetype = None
            self.file = None
        if self.path == self.params:
            self.params = None

    # @profile
    def compare_urls(self, url):
        """
        :param url: The url you are comparing it to (URL)
        :return: If it can be clustered or not (Bool)
        """
        if self.full_url == url.get_full_url():
            return 100
        else:

            positiveSimScore = {"Path": 0, "filename": 0, "file_type": 0}
            _attrMods = {"Path": .45, "filename": .35, "file_type": .2}

            if self.path == url.path:
                positiveSimScore["Path"] = 100
            else:
                if self.check_variants(url, mode="Path"):
                    positiveSimScore["Path"] = 100
                else:
                    positiveSimScore["Path"] = self.check_list(url, "Path")
            if self.file == url.file:
                positiveSimScore["filename"] = 100
            else:
                positiveSimScore["filename"] = 0
            if self.filetype == url.filetype:
                positiveSimScore["file_type"] = 100
            else:
                positiveSimScore["file_type"] = 0
            _totalSimilarity = 0

            for i in positiveSimScore.keys():
                try:
                    # noinspection PyTypeChecker
                    _totalSimilarity += positiveSimScore[i] * _attrMods[i]
                except:
                    pass
            if _totalSimilarity < 0:
                _totalSimilarity = 0
            return _totalSimilarity

    def get_full_url(self):
        return self.full_url

    def __eq__(self, other):
        return self.id_num == other.id_num

    def __le__(self, other):
        return self.id_num <= other.id_num

    def __ge__(self, other):
        return self.id_num >= other.id_num

    def __gt__(self, other):
        return self.id_num > other.id_num

    def __lt__(self, other):
        return self.id_num < other.id_num

    def check_variants(self, other, mode=None):
        if mode is "Path":
            if ("3942" in other.path or "r201" in other.path) or ("3942" in self.path or "r201" in self.path):
                return 100
            else:
                return False
        elif mode is "File":
            return False
        elif mode is "Param":
            return False
        elif mode is "Filetype":
            return False
        else:
            logging.critical("Args of check_variants not valid")
            return False

    def check_list(self, other, mode=None):
        if mode is "Path":
            iter_len = len(self.path_split) if len(self.path_split) <= len(other.path_split) else len(other.path_split)
            num_wrong = 0
            for i in range(iter_len):
                if self.path_split[i] != other.path_split[i]:
                    num_wrong += 1
            len_diff = abs(len(self.path_split) - len(other.path_split))
            return (1 - (num_wrong / iter_len * (len_diff + iter_len) / iter_len)) * 100
        else:
            logging.critical("Of Check_list Not Valid!")
            return 0


def len_checker(left, right):
    if len(left) != len(right):
        return 5 * abs(len(left) - len(right))
    return 0


def none_checker(left, right):
    if left is not None and right is not None:
        return True
    return False


def none_but_equal(left, right):
    if left is None and right is None:
        if left == right:
            return 100
    return 0


def compare_str(left, right):
    """
    :param left: Your URL (String)
    :param right: The URL you are comparing with (String)
    :return: The difference letters of the two strings and the indices of those differences (Dictionary)
    """
    # Choose which of the two URLs is shorter so that it can be iterated over
    _str = len(left) if len(right) > len(left) else len(right)

    # Arrays to help organize and keep track of the different letters in each URL
    _differentInRight = [None for i in range(_str)]
    _differentInLeft = _differentInRight

    # Array to save the index of the differences
    _indexOfDifferences = _differentInRight

    # Letters in both left and right
    _inBoth = _differentInRight

    # Tuple to deal with any differences in length
    _lengthDifferences = None
    if len(left) > len(right):
        _lengthDifferences = (len(left) - len(right), [i for i in left[len(right):]])
    elif len(right) > len(left):
        _lengthDifferences = (len(right) - len(left), [i for i in right[len(left):]])

    for letter_index in range(_str):
        if left[letter_index].isnumeric() and right[letter_index].isnumeric():
            _inBoth[letter_index] = "#"
        else:
            if left[letter_index] != right[letter_index]:
                _differentInLeft[letter_index] = left[letter_index]
                _differentInRight[letter_index] = right[letter_index]
                _indexOfDifferences[letter_index] = letter_index
            else:
                try:
                    _inBoth[letter_index] = [letter_index]
                except IndexError:
                    pass
    _inBoth = [x for x in _inBoth if x is not None]
    _differentInLeft = [x for x in _differentInLeft if x is not None]
    _differentInRight = [x for x in _differentInRight if x is not None]
    _indexOfDifferences = [x for x in _indexOfDifferences if x is not None]
    # Return the results as a Dictionary, where Left is an array of the differences in your URL
    # and Right is differences in the other URL
    return dict(Same=_inBoth, Left=_differentInLeft, Right=_differentInRight, Indices=_indexOfDifferences,
                Length_difference=_lengthDifferences)


# @profile
def similarity_score(left, right):
    """
    :param left: Your String (String)
    :param right: The String you are comparing with (String)
    :return: Similarity score (Float)
    """

    # Results from comparing the two strings
    _compareResults = compare_str(left, right)
    _totalLength = len(_compareResults["Same"]) + len(_compareResults["Left"])
    # % of letters that are the same to the length
    _pctSame = len(_compareResults["Same"])
    if _totalLength != 0:
        _pctSame = len(_compareResults["Same"]) / _totalLength

    # Factor in the difference in length
    try:
        _pctSame -= len(_compareResults["Length_difference"][1]) / (
            len(_compareResults["Same"]) + len(_compareResults["Left"])) * _pctSame / 10
    except TypeError:
        pass

    return _pctSame * 100
