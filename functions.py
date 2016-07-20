# Written by Gabriel Orlanski




def comparestr(left, right):
    """
    :param left: Your URL (String)
    :param right: The URL you are comparing with (String)
    :return: The difference letters of the two strings and the indices of those differences (Dictionary)
    """
    
    # Choose which of the two URLs is shorter so that it can be iterated over
    _str = len(left) if len(right) > len(left) else len(right)
    
    # Arrays to help organize and keep track of the different letters in each URL
    _differentInLeft = []
    _differentInRight = []
    
    # Array to save the index of the differences
    _indexOfDifferences = []
    
    # Letters in both left and right
    _inBoth = []
    
    # Tuple to deal with any differences in length
    _lengthDifferences = None
    if len(left) > len(right):
        _lengthDifferences = (len(left) - len(right), [i for i in left[len(right):]])
    elif len(right) > len(left):
        _lengthDifferences = (len(right) - len(left), [i for i in right[len(left):]])
    
    for letter_index in range(_str):
        if left[letter_index].isnumeric() and right[letter_index].isnumeric():
            _inBoth.append("#")
        else:
            if left[letter_index] != right[letter_index]:
                _differentInLeft.append(left[letter_index])
                _differentInRight.append(right[letter_index])
                _indexOfDifferences.append(letter_index)
            else:
                _inBoth.append(left[letter_index])
    
    # Return the results as a Dictionary, where Left is an array of the differences in your URL
    # and Right is differences in the other URL
    return {"Same": _inBoth, "Left": _differentInLeft, "Right": _differentInRight, "Indices": _indexOfDifferences,
        "Length_difference": _lengthDifferences}

    
def similarityscore(left, right):
    """
    :param left: Your String (String)
    :param right: The String you are comparing with (String)
    :return: Similarity score (Float)
    """
    
    # Results from comparing the two strings
    
    _compareResults = comparestr(left, right)
    _totalLength = len(_compareResults["Same"]) + len(_compareResults["Left"])
    # % of letters that are the same to the length
    _pctSame = len(_compareResults["Same"]) / _totalLength
    
    # Factor in the difference in length
    try:
        _pctSame -= len(_compareResults["Length_difference"][1]) / (len(_compareResults["Same"]) + len(_compareResults["Left"]))*_pctSame/10
    except TypeError:
        pass
    
        return _pctSame * 100
def lenchecker(left, right):
    if len(left) != len(right):
        return 5*abs(len(left)-len(right))
    return 0

def nonechecker(left, right):
    if left != None and right != None:
        
        return True
    return False

def nonebutequal(left,right):
    if left is None and right is None:
        if left == right:
            return 100 
    return 0

def urlcomparator(left,right):
    _length = abs(len(left)-len(right))
    _larger = True if len(left) > len(right) else False

    _totalScore = 0
    if _length <= 1:
        _totalScore +=  similarityscore(left,right)    

    else:    
        for i in range(_length):
            _totalScore += 1/_length * similarityscore(left[i],right[i])
    
    return _totalScore
    
    