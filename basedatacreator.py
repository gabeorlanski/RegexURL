# Written By Gabriel Orlanski

from urllib.parse import urlparse
import sys
import pandas as pd


fileofurls = pd.read_csv(sys.argv[1]+".csv",verbose=True)
fileofurls = fileofurls.drop_duplicates(subset="source")

listofurls = {}
# Iterate over Every URL, the Indecies are the URLs
lazy_count = 0
for index, row in fileofurls.iterrows():
    try:
        parsedurl = urlparse(row["source"])
    except AttributeError:
        print("Attr Error")
    try:
        netlocsplit = parsedurl.netloc.split(".")
        subdomain = netlocsplit[0]
        domain = ""
        for i, z in zip(range(len(netlocsplit[1:])), netlocsplit[1:]):
            if i != 0:
                domain = domain + "." + z
            else:
                domain = z
        listofurls["id_"+str(lazy_count)] = dict(domain=domain, subdomain=subdomain,path=parsedurl.path,params=parsedurl.params, tagname=row["tag_name"], displayname=row["display_name"])
        lazy_count+=1
    except:
        pass

pd.DataFrame.from_dict(listofurls).transpose().to_csv("parsed.csv")