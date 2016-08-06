"""
Written By Gabe Orlanski
This purpose of this class is to allow the comparison and storage of URLs for clustering them into groups
"""
import logging


class URL:
    def __init__(self, domain, subdomain, fullURL,filepath=None, urlparams=None, id=None):
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
            self.path = filepath
            self.path_split = filepath.split("/")
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
            if len(self.path[-1].split(".")) > 1:
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

    #@profile
    def compare_urls(self, url):
        """
        :param url: The url you are comparing it to (URL)
        :return: If it can be clustered or not (Bool)
        """
        if self.full_url == url.get_full_url():
            return 100
        else:
            negSimScore = {"Path": 0, "filename":0, "file_type":0, "params": 0}

            positiveSimScore = {"Path": None, "filename":None, "file_type":None}
            _attrMods = {"Path": .7, "filename":.075, "file_type": .075}

            if none_checker(self.path, url.path):
                negSimScore["Path"] += len_checker(self.path, url.path)
                positiveSimScore["Path"] = url_comparator(self.path_split, url.path_split)
                if none_checker(self.file, url.file):
                    negSimScore["filename"] += len_checker(self.file, url.file)
                    positiveSimScore["filename"] = url_comparator(self.file, url.file)
                    if none_checker(self.filetype, url.filetype):
                        negSimScore["file_type"] += len_checker(self.filetype, url.filetype)
                        positiveSimScore["file_type"] = url_comparator(self.filetype, url.filetype)
                    #if none_checker(self.params, url.params):
                        #negSimScore["params"] += len_checker(self.params, url.params)
                        #positiveSimScore["params"] = url_comparator(self.params_split, url.params_split)

            if positiveSimScore["Path"] is None:
                positiveSimScore["Path"] = none_but_equal(self.path, url.path)

            if positiveSimScore["filename"] is None:
                positiveSimScore["filename"] = none_but_equal(self.file, url.file)

            if positiveSimScore["file_type"] is None:
                positiveSimScore["file_type"] = none_but_equal(self.filetype, url.filetype)
            #if positiveSimScore["params"] is None:
                #positiveSimScore["params"] = none_but_equal(self.params, url.params)

            _totalSimilarity = 0

            for i in positiveSimScore.keys():
                try:
                    # noinspection PyTypeChecker
                    _totalSimilarity += (positiveSimScore[i] - negSimScore[i]) * _attrMods[i]
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


# @profile
def url_comparator(left, right):
    _larger = True if len(left) > len(right) else False
    _length = abs(len(right) - len(left))
    if _larger:
        itercheck = right
    else:
        itercheck = left
    _totalScore = 0
    if _length < 1:
        try:
            _totalScore += similarity_score(left, right)
        except TypeError:
            pass

    else:
        for i in range(len(itercheck)):
            try:
                _totalScore += 1 / _length * similarity_score(left[i], right[i])
            except (TypeError, IndexError, ZeroDivisionError) as e:
                pass

    return _totalScore


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
