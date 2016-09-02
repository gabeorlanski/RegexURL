import re
from urllib.parse import urlparse
import json
import pandas as pd
import os
import logging


def parse_urls(url_list):
    logging.info("Parsing URLs In the list")
    return [urlparse(x) for x in url_list]


def get_words_url(url):
    rtr_list = url.netloc.split(".")
    rtr_lengths = [len(rtr_list)]
    rtr_dict = {"Netloc": False, "Path": False, "File": False, "Query": False, "len": False}
    logging.info("Creating the list of words in the URL")
    if url.path:
        rtr_dict["Path"] = True
        if "." in url.path.split("/")[-1]:
            url_path_wo_file = url.path.split("/")[1:-1] + [url.path.split("/")[-1].split(".")[0]]
            rtr_lengths.append(len(url.path.split("/")[1:]))
            for i in url_path_wo_file:
                rtr_list.append(i)
            rtr_lengths.append(1)
            rtr_list.append(url.path.split("/")[-1].split(".")[1])
            rtr_dict["File"] = True
        else:
            rtr_lengths.append(len(url.path.split("/")[1:]))
            for i in url.path.split("/")[1:]:
                rtr_list.append(i)
        if url.query:
            rtr_lengths.append(len(url.query.split("&")))
            for i in url.query.split("&"):
                if "=" in i:
                    rtr_list.append(i.split("=")[0] + "=")
                else:
                    rtr_list.append(i)

            rtr_dict["Query"] = True
    return [rtr_list, rtr_lengths, rtr_dict]


def checkEqual(iterator):
    logging.info("Checking if the list is filled of equal items")
    try:
        iterator = iter(iterator)
        first = next(iterator)
        return all(first == rest for rest in iterator)
    except StopIteration:
        return True


def dif_lens(list_of_lens):
    cur_lens = []
    logging.info("Handling URLs that have a different amount of Subdomains, Elements in path, or Query items")
    for i in range(len(list_of_lens[0])):
        lens_ = []
        try:
            for x in range(len(list_of_lens)):
                lens_.append(list_of_lens[x][i])
        except IndexError:
            return cur_lens
        if not checkEqual(lens_):
            cur_lens.append(min(lens_))
            return cur_lens
        else:
            cur_lens.append(lens_[0])


# noinspection PyTypeChecker
def regexify(url_list):
    logging.info("Begining the process of Turning the list of URLs into a Regex")
    try:
        lens_urls = [None for i in range(len(url_list))]
        split_urls = [None for i in range(len(url_list))]
        lens_to_use = []
        helper_dict = None
        logging.info("Extrapolating the info from the URLs")
        for i, z in enumerate(parse_urls(url_list)):
            x, v, z = get_words_url(z)
            helper_dict = z
            split_urls[i] = x
            lens_urls[i] = v
        if checkEqual(lens_urls):
            lens_to_use = lens_urls[0]
        else:
            lens_to_use = dif_lens(lens_urls)
            helper_dict["len"] = True
        unique_words_ = [None for i in range(sum(lens_to_use))]
        logging.info("Picking out Unique Words")
        for word in range(sum(lens_to_use)):
            word_list = set()
            for url in range(len(split_urls)):
                word_list.add(split_urls[url][word])
            unique_words_[word] = list(word_list)
        regex = [None for i in unique_words_]
        logging.info("Looping through the unqiue words, looking at their position")
        for c, i in enumerate(unique_words_):
            if len(i) <= 4:
                if len(i) > 1:
                    regex[c] = "(" + "|".join(i) + ")"
                else:
                    regex[c] = i[0]
            else:
                regex[c] = ".{" + str(len(min(i, key=len))) + "," + str(len(max(i, key=len))) + "}"
        formatted = "(http|https)\\:\\/\\/"
        logging.info("Adding the parts of the regex")
        for i, v in enumerate(lens_to_use):
            for part in range(v):
                if i != 0:
                    cur_index = sum(lens_to_use[:i]) + part
                    if i == 1 and helper_dict["Path"]:
                        formatted += "\\/" + regex[cur_index]
                    elif i == 2 and helper_dict["File"]:
                        formatted += "\\." + regex[cur_index]
                    elif (i == 2 or i == 3) and helper_dict["Query"]:
                        part_end_to_add = "\\.+\\&" if "=" in regex[cur_index] else "\\&"
                        if part != 0 and part != v - 1:
                            formatted += regex[cur_index] + part_end_to_add
                        elif part == v - 1:
                            formatted += regex[cur_index] + part_end_to_add.replace("\\&", "")
                        else:
                            formatted += "\\?" + regex[cur_index] + part_end_to_add

                else:
                    if part != 0:
                        formatted += "\\." + regex[part]
                    else:
                        formatted += regex[part]
        if helper_dict["len"]:
            formatted += ".+"
        return formatted
    except Exception as e:
        logging.error("Exception " + str(e) + " Adding the URLs to the rejects file")
        with open("REJECTS_REGEX.txt", 'a') as f:
            f.write("----------------------------------------------------------------------")
            f.write("\n")
            for q in url_list:
                f.write(q + "\n")
        return "CHECK REJECTS_REGEX.txt"


def get_urls(d):
    if len(d["children"]) > 0:
        x = []
        for i in d["children"]:
            x.append(get_urls(i))
        return x
    else:
        return (d["URLs"], d["id"])


def run():
    data = json.loads(open("groups.json").read())
    try:
        os.remove("REJECTS_REGEX.txt")
    except:
        pass
    test = []
    for (level_0, value), c in zip(data.items(), range(len(data.keys()))):
        for level_1, value_2 in value.items():
            temp_list = []
            url_result = get_urls(value_2)
            if not isinstance(url_result, tuple):
                for i in url_result:
                    test.append([level_0.split("_")[1], i[1], regexify(i[0])])
            else:
                test.append([level_0.split("_")[1], url_result[1], regexify(url_result[0])])
    pd.DataFrame(test, columns=["Tag","Source_URL","Regex"]).to_csv("PROGRAM_OUTPUT.csv", index=False)
