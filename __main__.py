# Written By Gabe Orlanski

from url_class import URL
import os
import group_class
import json


def main():
    printopener()


def printopener():
    print(
        "|------------------------------------------------------|\nWelcome To The URL Grouper \nIs your data file in the same directory as this program?")
    path = getpath()
    print("Please enter the name of your data file: ")
    s = input("-->")
    if ".csv" not in s:
        s += ".csv"
    print(path)
    print(s)
    print(os.path.isfile(path + s))
    if not os.path.isfile(path + s):
        raise ValueError("File " + s + " not found")

    of = open("groups.json", "w")
    of.write(json.dumps(group_class.groups_to_file(str(path+s), None, None), indent=2, sort_keys=True))
    of.close()


def getpath():
    path = ""
    _isInCurDir = input("-->")
    if _isInCurDir == "yes" or _isInCurDir == "Yes" or _isInCurDir == "Y":
        path = os.getcwd()
        print("Is it in a subfolder?")
        is_subfolder = input("-->")
        if is_subfolder == "yes" or is_subfolder == "Yes" or is_subfolder == "Y":
            print("What is the path of the Subfolder?")
            subfolder_ = input("-->")
            if subfolder_[0] != "/":
                subfolder_ = "/" + subfolder_
            if subfolder_[-1] != "/":
                subfolder_ += "/"
            return path + subfolder_
        elif is_subfolder == "no" or is_subfolder == "No" or is_subfolder == "N":
            return path
        else:
            print("Invalid Input. \nIs your file in the same directory as this program?")
            return getpath()
    elif _isInCurDir == "no" or _isInCurDir == "No" or _isInCurDir == "N":
        print("Please enter the path to your file: ")
        path = input("-->")
        return path
    else:
        print("Invalid Input. \nIs your file in the same directory as this program?")
        return getpath()

if __name__ == "__main__": main()
