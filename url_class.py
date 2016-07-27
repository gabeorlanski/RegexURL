"""
Written By Gabe Orlanski
This purpose of this class is to allow the comparison and storage of URLs for clustering them into groups
"""

from functions import nonechecker, lenchecker, nonebutequal, urlcomparator


class URL:
    def __init__(self, domain, subdomain, filepath=None, urlparams=None, id=None):
        """
        :param domain: Domain of the url (String)
            example: "reddit.com" in www.reddit.com/r/test/ex.js;name=Hi
        :param subdomain: Subdomain of the url (String)
            example: "www" in www.reddit.com/r/test/ex.js;name=Hi
        :param filepath: Filepath of the domain. Defaults to none when there is no file path (String)
            example: "/r/test/ex.js" in www.reddit.com/r/test/ex.js;name=Hi
        :param urltype: The type of file this URL leads to. Defaults to None when the URL does not call a file (String)
            example: "js" in www.reddit.com/r/test/ex.js;name=Hi
        :param urlparams: The parameters of the script the URL calls. Defaults to None when there is no script (String)
            example: "name=Hi" in www.reddit.com/r/test/ex.js;name=Hi
        :return: None
        """
        self.id = id
        self.domain = domain.split(".")
        self.subdomain = subdomain
        if filepath != None:
            self.path = filepath.split("/")
        else:
            self.path = None

        try:
            self.file_type = urltype.split(".")[1]
            self.file_name = urltype.split(".")[0]
        except IndexError:
            self.file_name = urltype
            self.file_type = None
            
        if urlparams != None:
            self.params = urlparams.split("&")
        else:
            self.params = None

    def compareurls(self, url):
        """
        :param url: The url you are comparing it to (URL)
        :return: If it can be clustered or not (Bool)
        """
        _negSimScore = {"Path": 0, "file_name":0, "file_type":0, "params": 0}
        
        _positiveSimScore = {"Path": None, "file_name":None, "file_type":None, "params": None}
        _attrMods = {"Path": .7, "file_name":.075, "file_type": .075, "params": .15}
        
        if nonechecker(self.path,url.path):        
            _negSimScore["Path"] += lenchecker(self.path,url.path)
            _positiveSimScore["Path"] = urlcomparator(self.path,url.path)
            if nonechecker(self.file_name,url.file_name):
                _negSimScore["file_name"] += lenchecker(self.file_name,url.file_name)
                _positiveSimScore["file_name"] = urlcomparator(self.file_name,url.file_name)
                if nonechecker(self.file_type,url.file_type):
                    _negSimScore["file_type"] += lenchecker(self.file_type,url.file_name)
                    _positiveSimScore["file_type"] = urlcomparator(self.file_type,url.file_type)
                if nonechecker(self.params,url.params):
                    _negSimScore["params"] += lenchecker(self.params,url.params)
                    _positiveSimScore["params"] = urlcomparator(self.params,url.params)
        
        if _positiveSimScore["Path"] is None:
            _positiveSimScore["Path"] = nonebutequal(self.path, url.path)

        if _positiveSimScore["file_name"] is None:
            _positiveSimScore["file_name"] = nonebutequal(self.file_name,url.file_name)

        if _positiveSimScore["file_type"] is None:
            _positiveSimScore["file_type"] = nonebutequal(self.file_type,url.file_name)

        if _positiveSimScore["params"] is None:
            _positiveSimScore["params"] = nonebutequal(self.params,url.params)
            
        _totalSimilarity = 0
        
        for i in _positiveSimScore.keys():
            try:
                _totalSimilarity += (_positiveSimScore[i] - _negSimScore[i]) * _attrMods[i]
            except:
                pass
            
        return _totalSimilarity
