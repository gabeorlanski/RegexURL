# Written By Gabe Orlanski

from url_class import URL
import os
from testing import test_1


def main():
    test_1()


def printopener():
   print("|------------------------------------------------------|\nWelcome To The Regexifier \nIs your data file in the same directory as this program?")      
   path = getpath()    
   print("Please enter the name of your data file: ")
   s = input("-->")
   if ".csv" not in s:
       s = s + ".csv"
   if not os.path.isfile(s):
      raise ValueError("File " + s + "not found")
       
    
def getpath():
   path = ""
   _isInCurDir = input("-->")
   if _isInCurDir == "yes" or _isInCurDir == "Yes" or _isInCurDir == "Y":
      path = os.getcwd()
      return path
   elif _isInCurDir == "no" or _isInCurDir == "No" or _isInCurDir == "N":
      print("Please enter the path to your file: ")
      path = input("-->")
      return path
   else:
      print("Invalid Input. \nIs your file in the same directory as this program?")
      return getpath()
    
        
if __name__ == "__main__":main()