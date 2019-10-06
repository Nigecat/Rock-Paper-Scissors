#
#
#   This file contains the json data handling function
#
#

from json import dump
from json import load

def sampleData(key, **files):
    '''Function to retrive the sample (input) data

    Pulls data from [files.json], returns a list of all the values, can take multiple files as input, can return specific keys
    '''

    files = files["files"]

    files = [".\\data\\" + file for file in files]  #Add the file path to the data files infront of the file name

    data = {}   
    for file in files:
        with open(file) as f:   #Open each json file and add the data from it onto the data dict
            data = {**data, **load(f)}

    if key == None:     #If you dont specify a key, return all of them
        return [data[key] for key in data.keys()]
    else:
        return data[key]

def dumpData(name, **add):
    '''Function to dump the current data to the json file

    name -- name of the user to dump the data to
    add -- the data to add to the file (dict)
    '''

    if name != "guest":
        with open(".\\data\\data-user.json") as f:
            data = load(f)
        data[name] = add
        with open(".\\data\\data-user.json", "w") as f:
            dump(data, f, indent=4)

def loadData(name):
    '''Function to load the data of a user from the json file

    name -- the name of the user to retrive the data from
    '''

    if name != "guest":
        with open(".\\data\\data-user.json") as f:
            try:        #Try/catch block, will catch if data-user.json empty
                data = load(f)
                return data[name]["playerHistory"], data[name]["computerHistory"], data[name]["results"]
            except:
                return [], [], []   #If data-user.json is empty (or user doesn't exist), return a blank list
    else:
        return [], [], []

if __name__ == '__main__':
    from os import system
    system("gui.py")