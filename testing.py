from group_class import group
import random
from url_class import URL

def test_1():
    test_1 = URL("um","simpli.fi","/","match_redirect","sifi_redir=%2F%2Ftags.bluekai.com%2Fsite%2F29931%3Fid%3D%24UID")
    test_2 = URL("um","simpli.fi","/","pm_match?https://image2.pubmatic.com/AdServer/Pug?vcode=bz0yJnR5cGU9MSZjb2RlPTgwNiZ0bD01MTg0MDA=&piggybackCookie=uid:$UID")
    print(test_1.compareurls(test_2))