# Written By Gabe Orlanski
import logging
import pandas as pd
from urllib.parse import urlparse
from url_class import URL
from score_class import Score
from scorelist_class import ScoreList, functions


class Group:
    def __init__(self, domain, subdomain, tagname):
        logging.info("Making Group for %s" % domain)
        self.domain = domain
        self.subdomain = subdomain
        self.regex = ""
        # regexify()
        self.scores = ScoreList()
        self._url = []
        self.tree = dict(Name="Everything", Children=[])
        self.children = []
        self.orphans = []
        self.tag_name = tagname

    def add_urls(self, urls):
        self._url = urls

    def add_url(self, url):
        """
        :param url: the url to add
        :rtype: None
        """
        self._url.append(url)

    def get_regex(self):
        return self.regex

    def can_compress(self):
        logging.info("Checking if the group can compress")
        if len(self._url) > 1:
            return True
        return False

    def generate_scores(self):
        logging.info("Generating scores")
        for i in range(len(self._url)):
            for x in range(1, len(self._url) - i):
                self.scores.add_score(Score(self._url[i], self._url[i + x], self._url[i].compare_urls(self._url[i + x])))

    def add_score(self, score):
        self.scores.add_score(score)

    #@profile
    def generate_children(self, depth=0):
        logging.info("Splitting Groups")
        # Find the two URLs the least similar, and make two new groups with them
        if self.scores.least_similar() is not False and self.can_compress() is not False and self.scores.check_equal() is not True:
            lowest_score = self.scores.least_similar()

            left = lowest_score.left
            right = lowest_score.right
            if lowest_score.value >= 87:
                return 1
            # Create the two child groups
            left_group = Group(lowest_score.left.domain, lowest_score.left.subdomain,self.tag_name + "_1")
            right_group = Group(lowest_score.right.domain, lowest_score.right.subdomain, self.tag_name + "_2")
            right_group.add_url(right)
            left_group.add_url(left)
            logging.info("LEFT URL: %s" % left.get_full_url())
            logging.info("RIGHT URL: %s" % right.get_full_url())
            logging.info("LOWEST SCORE: %f" % lowest_score.value)
            logging.info("GROUPSCORES: %s" % str([i.value for i in self.scores.scores_array]))
            same_scores = 0
            rejects = []
            # Iterate over the URLs in the group
            for url in self._url:

                # Check which of the two URLs the currently selected URL is more similar too
                # Then add it to that group
                if url != left and url != right:
                    try:
                        if self.scores.get_score(url, left) > self.scores.get_score(url, right):
                            left_group.add_url(url)
                            left_group.add_score(self.scores.get_score(url, left))
                        elif self.scores.get_score(url, left) < self.scores.get_score(url, right):
                            right_group.add_url(url)
                            right_group.add_score(self.scores.get_score(url, right))
                        elif self.scores.get_score(url, left) == self.scores.get_score(url, right):
                            same_scores += 1
                            self.orphans.append(url)

                    except:
                        logging.error("Error With Getting scores of %s" % url.id + " and %s" % left.id + " and %s" % right.id)
                        if url not in rejects:
                            rejects.append(url)
                        pass
            if rejects:
                with open("rejects.txt", "a") as myfile:
                    myfile.write("\n----------NEW GROUP----------")
                    myfile.write("\nTAG: %s" % self.tag_name)
                    for url in rejects:
                        myfile.write("\n%s" % url.get_full_url())
            if same_scores <= round(len(self._url) * .85):
                self.children = [left_group, right_group]
                logging.info("Creating Children Of Children")
                # Recursion it up
                for child in self.children:
                    if child.can_compress() and depth < 10:
                        child.generate_children(depth=depth+1)
            else:
                logging.info("Group Cannot Compress b/c all of the urls are the same")

    def getUrls(self):
        return self._url


def group_urls(listofurls, pbar_queue = None, rtr_domains=False):
    """
    :param listofurls: list of URLs
    :returns: list of objects groups
    """
    logging.info("Grouping URLs")
    listofgroups = []
    useddomains = []
    for url in listofurls:
        if url.domain not in useddomains:
            listofgroups.append(Group(url.domain, url.subdomain,url.tag_name))
            useddomains.append(url.domain)
            logging.info("Added %s" % url.domain + " To the tag list")
        listofgroups[useddomains.index(url.domain)].add_url(url)
    if rtr_domains:
        return (listofgroups, useddomains)
    return listofgroups


def groups_to_file(inputfile, filepath=None, pbar_queue=None):
    output = dict()
    x = create_url_list(inputfile)
    for i in range(len(x)):
        for q in range(len(x[i])):
            x[i][q].generate_scores()
            x[i][q].generate_children()
            try:
                output["g_" + x[i][q].tag_name][x[i][q].domain] = is_children(x[i][q],x[i][q].domain)
            except:
                output["g_" + x[i][q].tag_name] = {x[i][q].domain:is_children(x[i][q],x[i][q].domain)}
    return output


def create_url_list(filePath):
    """
    :param filePath: csv populated with URLs. First field must be the URL
    :returns: list filled with instances of the class URL
    """
    logging.info("Creating URL list")
    # Create DataFrame of the CSV file to iterate over
    fileofurls = pd.read_csv(filePath)
    groups = fileofurls.groupby("tag_name")
    qq = [i[1] for i in groups]
    x = {}
    for i in enumerate(qq):
        q = i[1].source.apply(
            lambda d: urlparse(d).netloc.split(".")[-2] + "." + urlparse(d).netloc.split(".")[-1] + check_variants(urlparse(
                d).path, mode="Path") + "-".join([z.split("=")[0] for z in urlparse(d).query.split("&")])).to_frame()
        q.columns = ["domain"]
        x[i[0]] = pd.concat([i[1], q], axis=1).drop_duplicates(subset="domain")
    logging.info("Finished Reading The File")
    list_groups = [None for i in x.keys()]

    for key in x.keys():
        listofurls = [None for i in range(len(x[key].index))]
        # Iterate over Every URL, the Indecies are the URLs
        lazy_count = 0
        for index, row in x[key].iterrows():
            
            try:
                parsedurl = urlparse(row["source"])
            except AttributeError:
                logging.error("Error with the index %s" % index)
            try:
                netlocsplit = parsedurl.netloc.split(".")
                subdomain = netlocsplit[0]
                domain = ""
                if len(netlocsplit) > 2:
                    for i, z in zip(range(len(netlocsplit[1:])), netlocsplit[1:]):
                        if i != 0:
                            domain = domain + "." + z
                        else:
                            domain = z
                else:
                    domain = ".".join(netlocsplit)
                params = "-".join([i.split("=")[0] for i in parsedurl.query.split("&")])
                listofurls[lazy_count] = URL(domain, subdomain, str(row["source"]),str(row["tag_name"]), parsedurl.path, params, "id" + str(lazy_count))
                lazy_count += 1
            except TypeError:
                logging.error("Split wants a byte")
        
        list_groups[key] = group_urls(listofurls)
    return list_groups


def check_variants(url, mode=None):
        if mode is "Path":
            return url
        elif mode is "File":
            return False
        elif mode is "Param":
            return False
        elif mode is "Filetype":
            return False
        else:
            logging.critical("Args of check_variants not valid")
            return False


def is_children(group, _id):
    rtr_dict = dict(id=_id, children=[])
    if len(group.children) > 0:
        for i in range(len(group.children)):
            rtr_dict["URLs"] = [x.get_full_urls() for x in group.orphans]
            rtr_dict["children"].append(is_children(group.children[i], _id + "_" + str(i + 1)))
    else:
        rtr_dict["URLs"] = [None for i in group.getUrls()]
        for i, z in zip(group.getUrls(), range(len(group.getUrls()))):
            rtr_dict["URLs"][z] = i.get_full_url()
    return rtr_dict


