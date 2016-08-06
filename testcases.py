from score_class import Score
from url_class import URL
from scorelist_class import Book,Shelf
import random


class TestBook:
    def __init__(self):
        try:
            self.test_score = Score(URL("HelloWorld","Im1","HelloWorld,Im1",id="id0"),URL("HelloWorld","Im2","HelloWorld,Im2",id="id1"),75)
            self.test_book = Book(self.test_score.right,0,self.test_score)
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
        test_list = [1,3,6,4,2,5,7,19,8,9,10,13,12,11,14,15,18,16,20,17]
        self.shelf = Shelf()
        try:
            for i, v in enumerate(test_list):
                print(v)
                sub = ("X-","X2-")
                dom = ("Y-%s" % str(v*2),"Y2-%s" % str(v))
                id_ = ("id%s" % str(v*2), "id%s" % str(v))
                test_score = Score(URL(dom[0],sub[0],sub[0]+dom[0],id=id_[0]),URL(dom[1],sub[1],sub[1]+dom[1],id=id_[1]),random.randint(0,100))
                self.shelf.add_score(test_score)
            for i in self.shelf.books:
                print(i.url.id)
            self.shelf.sort_scores()
            print("---------------------")
            for i in self.shelf.books:
                print(i.url.id)
        except Exception as e:
            print("Failure with Shelf.Sort, Exception: %s" % e)

TestShelfSort()