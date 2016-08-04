# Written by Gabriel Orlanski
from group_class import Group
import pandas as pd
from urllib.parse import urlparse
from url_class import URL
import logging

logging.basicConfig(filename="programlogs.txt",level=logging.DEBUG)








def groupURLs(listofurls, pbar_queue = None):
    """
    :param listofurls: list of URLs
    :returns: list of objects groups
    """
    logging.info("Grouping URLs")
    listofgroups = []
    useddomains = []
    for url in listofurls:
        if url.domain not in useddomains:
            listofgroups.append(Group(url.domain, url.subdomain))
            useddomains.append(url.domain)
            logging.info("Added %s" % url.domain + " To the domain list")
        listofgroups[useddomains.index(url.domain)].addUrl(url)
    return listofgroups


def groupstofile(inputfile, filepath=None, pbar_queue=None):
    output = dict()
    x = groupURLs(createurllist(inputfile), pbar_queue)
    for i in range(len(x)):
        x[i].generateScores()
        x[i].splitUrlList(pbar_queue)
        output["g_" + str(i)] = ischildren(x[i], str(i))
    return output


def ischildren(group, _id):
    rtr_dict = dict(id=_id, children=[])
    if len(group.children) > 0:
        for i in range(len(group.children)):
            rtr_dict["children"].append(ischildren(group.children[i], _id + "_" + str(i + 1)))
    else:
        rtr_dict["URLs"] = [None for i in group.getUrls()]
        for i, z in zip(group.getUrls(), range(len(group.getUrls()))):
            rtr_dict["URLs"][z] = i.getFullURL()
    return rtr_dict


def createurllist(filePath):
    """
    :param filePath: csv populated with URLs. First field must be the URL
    :returns: list filled with instances of the class URL
    """
    logging.info("Creating URL list")
    # Create DataFrame of the CSV file to iterate over
    fileofurls = pd.DataFrame.from_csv(filePath)
    listofurls = [None for i in range(len(fileofurls.index))]
    # Iterate over Every URL, the Indecies are the URLs
    lazy_count = 0
    for index, row in fileofurls.iterrows():
        try:
            parsedurl = urlparse(index)
        except AttributeError:
            logging.error("Error with the index %s" % index)
        netlocsplit = parsedurl.netloc.split(".")
        subdomain = netlocsplit[0]
        domain = ""
        for i, z in zip(range(len(netlocsplit[1:])), netlocsplit[1:]):
            if i != 0:
                domain = domain + "." + z
            else:
                domain = z
        listofurls[lazy_count] = URL(domain, subdomain, parsedurl.path, parsedurl.params, "id" + str(lazy_count))
        lazy_count += 1

    return listofurls


def mergeSort(alist):
    if len(alist) > 1:
        mid = len(alist) // 2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k] = lefthalf[i]
                i += 1
            else:
                alist[k] = righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            alist[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            alist[k] = righthalf[j]
            j += + 1
            k += 1
    return alist


# Find a path between the two
def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


# Shortest Path
def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None
