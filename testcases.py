from score_class import Score
from url_class import URL, detailed_compare
from scorelist_class import Book, Shelf
import random
from group_class import Group, is_children
from urllib.parse import urlparse


class TestBook:
    def __init__(self):
        try:
            self.test_score = Score(URL("HelloWorld", "Im1", "HelloWorld,Im1", id="id0"),
                                    URL("HelloWorld", "Im2", "HelloWorld,Im2", id="id1"), 75)
            self.test_book = Book(self.test_score.right, 0, self.test_score)
        except Exception as e:
            print("Failure with Book Initialization, Exception: %s" % e)


class TestShelf:
    def __init__(self):
        try:
            self.test_shelf = Shelf(TestBook())
        except Exception as e:
            print("Failure with Shelf Initialization, Exception: %s" % e)


class TestShelfSort:
    def __init__(self):
        test_list = [1, 3, 6, 4, 2, 5, 7, 19, 8, 9, 10, 13, 12, 11, 14, 15, 18, 16, 20, 17]
        self.shelf = Shelf()
        try:
            for i, v in enumerate(test_list):
                print(v)
                sub = ("X-", "X2-")
                dom = ("Y-%s" % str(v * 2), "Y2-%s" % str(v))
                id_ = ("id%s" % str(v * 2), "id%s" % str(v))
                test_score = Score(URL(dom[0], sub[0], sub[0] + dom[0], id=id_[0]),
                                   URL(dom[1], sub[1], sub[1] + dom[1], id=id_[1]), random.randint(0, 100))
                self.shelf.add_score(test_score)
            for i in self.shelf.books:
                print(i.url.id)
            self.shelf.sort_scores()
            print("---------------------")
            for i in self.shelf.books:
                print(i.url.id)
        except Exception as e:
            print("Failure with Shelf.Sort, Exception: %s" % e)


class TestGroup:
    def __init__(self):
        urls_bla = [
            "http://i.simpli.fi/dpx?cid=42167&m=1&sifi_tuid=20769&cbri=965697365535&referrer=http%3A//www.martianherald.com/19-amazing-underwater-discoveries/page/5%3Futm_source%3Doutbrain%26utm_medium%3Dreferral%26utm_campaign%3DAmazingUnderwater-US-DTT-O%26utm_term%3D4775950",
      "http://um.simpli.fi/lj_match",
      "http://um.simpli.fi/aol",
      "http://um.simpli.fi/match_redirect?sifi_redir=%2F%2Ftags.bluekai.com%2Fsite%2F29931%3Fid%3D%24UID",
      "http://um.simpli.fi/lr",
      "http://um.simpli.fi/spotx_match",
      "http://um.simpli.fi/fb_match",
      "http://um.simpli.fi/an",
      "http://um.simpli.fi/cw_match",
      "http://um.simpli.fi/rb_match",
      "http://um.simpli.fi/ox_match",
      "http://um.simpli.fi/pm_match?https://image2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTgwNiZ0bD01MTg0MDA=&piggybackCookie=uid:$UID"
        ]
        urls = [None for i in urls_bla]
        lazy_count = 0
        for qq in urls_bla:
            try:
                parsedurl = urlparse(qq)
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
                urls[lazy_count] = URL(domain, subdomain, str(qq),str("simpli"), parsedurl.path, params, "id" + str(lazy_count))
                lazy_count += 1
            except:
                print("ERROR")
                pass
        self.group = Group("Simpli.fi", "um", "simpli")
        self.group.add_urls(urls)
        self.group.generate_scores()
        self.group.generate_children()

qq = TestGroup()
print(is_children(qq.group,"01"))