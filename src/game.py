#py -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
#C:\Users\nigel.quick\AppData\Local\Programs\Python\Python37-32\Lib\site-packages - local package location
from sys import path
from json import dump, load
from itertools import groupby
try: 
    path.insert(0, './libs')    #Change running directory to the libs folder
    from numpy import random as nprnd   #Non std lib, import from local
except ImportError:
    print("Numpy was unable to be imported properly...")
    input()

def queryName(num):
    '''Function to return the name of the action that corresponds to a number

    num -- the number of the action to get the name of
    '''
    if num == 0:
        return "rock"
    elif num == 1:
        return "paper"
    elif num == 2:
        return "scissors"

def trainingData():
    '''Function to retrive the training data

    Pulls data from data-training.json, returns a list of all the keys
    '''
    with open("data-training.json") as f:
        data = load(f)
    return [data[key] for key in data.keys()]

def dumpHistory(name, history):
    '''Function to dump the current history to the json file

    name -- name of the user to dump the data to
    history -- the history to dump to the file
    '''
    with open("data.json") as f:
        try:
            data = load(f)
        except:
            data = {}
    data[name] = history
    with open('data.json', 'w') as f:
        dump(data, f)

def loadHistory(name):
    '''Function to load the history of a user from the json file

    name -- the name of the user to retrive the data from
    '''
    with open("data.json") as f:
        try:
            data = load(f)
            return data[name]
        except:
            return []
        

def beats(action):
    '''Function to return what beats what

    action -- the action that is played, whatever beats this action will be returned
    '''
    if action == 0 or action == "rock":
        return "paper"
    elif action == 1 or action == "paper":
        return "scissors"
    elif action == 2 or action == "scissors":
        return "rock"

def calculateMove(name, history):
    '''Function to calculate the computer's move

    name -- the name of the user playing
    history -- the user's history
    Note for code reading:
        Rock: 0
        Paper: 1
        Scissors: 2
    '''

    if len(history) == 0:   #If the history is blank (then we have no data)
        #Pick a random option, this is weighted random because statistically, people play rock on the first turn. 
        #So we have paper as most likely, the others are there in case people catch on (to switch things up).
        return nprnd.choice(["rock", "paper", "scissors"], p=[0.2, 0.6, 0.2]) 

    #Else: (we don't need an else statement because return will stop the code)
    for i in range(len(history) - 1, -1, -1):   #Run through the history backwards
        try:
            if history[i] == history[i - 1] and history[i - 1] == history[i - 2]:
                return beats(history[i])    #Check if the user is repeatedly playing the same action and play the counter
            else:
                break
        except: pass

    #letters = history + trainingData()[0] + trainingData()[1] + trainingData()[2] + trainingData()[3] + trainingData()[4]
    letters = history
    for item in trainingData():
        letters = letters + item

    for i in range(len(letters)):
        if letters[i] == 0:
            letters[i] = "a"
        elif letters[i] == 1:
            letters[i] = "b"
        elif letters[i] == 2:
            letters[i] = "c"

    groups = groupby(letters, key=lambda x: x[0])
    predictions = [[a[0], sum (1 for _ in a[1])/float(len(letters))] for a in groups]

    highest = 0
    move =  "a"
    for i in range(len(predictions)):
        if predictions[i][1] > highest:
            highest = predictions[i][1]
            move = predictions[i][0]

    if nprnd.choice([1, 2, 3, 4, 5], p=[0.2, 0.2, 0.2, 0.2, 0.2]) == 1: #Throw in a bit of random to switch things up
        return nprnd.choice(["rock", "paper", "scissors"], p=[0.3, 0.4, 0.3]) 
    elif move == "a":
        return "rock"
    elif move == "b":
        return "paper"
    elif move == "c":
        return "scissors"
    else:
        return nprnd.choice(["rock", "paper", "scissors"], p=[0.3, 0.4, 0.3])   #Return random choice if something goes wrong