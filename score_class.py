# Written By Gabe Orlanski

from url_class import URL


class Score:
    def __init__(self, url1, url2, value):
        self.value = value
        self.left = url1
        self.right = url2

    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False

    def __gt__(self, other):
        if self.value > other.value:
            return True
        return False

    def __lt__(self, other):
        if self.value < other.value:
            return True
        return False

    def __ge__(self, other):
        if self.value >= other.value:
            return True
        return False

    def __le__(self, other):
        if self.value <= other.value:
            return True
        return False

    def has_url(self, url):
        if self.left == url or self.right == url:
            return True
        return False

    def getOtherUrl(self, url, url2=None):
        if self.has_url(url):
            if self.left == url:
                return self.right
            elif self.right == url:
                return self.left
        elif url is not None and self.has_url(url2):
            if self.left == url2:
                return self.right
            elif self.right == url2:
                return self.left
        return None
