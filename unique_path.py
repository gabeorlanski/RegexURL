import pandas as pd
from group_class import create_url_list, group_urls
import pandas as pd
from sklearn.cluster import KMeans

def run_ml(filepath):
    x = create_url_list(filepath)
    path_components = set()
    noteworthy = []
    ares = []
    doms = group_urls(x, None, True)
    for i in x:
        for q in range(1, len(i.path_split)-1):
            if i.path_split[q] != '':
                if "3942" in i.path_split[q]:
                    path_components.add("3942-")
                    noteworthy.append(i)
                elif "201" in i.path_split[q]:
                    ares.append(i)
                    path_components.add("r201-")
                else:
                    path_components.add(i.path_split[q])
    helper_dict = {}
    for i in x:
        helper_dict[i.full_url] = {}
        for q in path_components:
            if q in i.path_split:
                helper_dict[i.full_url][q] = 1
            elif i in noteworthy and "3942" in q:
                helper_dict[i.full_url]["3942-"] = 1
            elif i in ares and "r201" in q:
                helper_dict[i.full_url]["r201-"] = 1
            else:
                helper_dict[i.full_url][q] = 0
        helper_dict[i.full_url]["Domain"] = doms[1].index(i.domain)

    df = pd.DataFrame.from_dict(helper_dict,orient="index")
    df_nodomain = df.drop("Domain",axis=1)
    matrix = df.drop("Domain", axis=1).dot(df.drop("Domain",axis=1).transpose())
    bla = df.groupby("Domain").apply(get_clusters)
    bla.to_csv("WORKPLSE.csv")
    next_df


def get_clusters(df_):
    try:
        test_df2 = df_
        KM = KMeans(n_clusters=2)
        KM.fit(test_df2)
        test_df2["Cluster"] = KM.predict(test_df2)
    except ValueError:
        pass
    try:
        return test_df2.groupby("Cluster").groups
    except KeyError:
        return {0: list(df_.index.values)}

