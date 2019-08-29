#py -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
#C:\Users\nigel.quick\AppData\Local\Programs\Python\Python37-32\Lib\site-packages - local package location
from sys import path    #These modules are part of the python stdlib
from json import dump, load
from itertools import groupby
try: 
    path.insert(0, './libs')    #Change running directory to the libs folder
    from numpy import random as nprnd   #Non stdlib, import from local file
except ImportError:
    from tkinter import messagebox, Tk  #We do this because you can't see the console window
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Rock-Paper-Scissors", "Numpy was unable to be imported...")
    quit()

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
    return [data[key] for key in data.keys()]   #Return all the values of the dict in a list

def dumpHistory(name, history):
    '''Function to dump the current history to the json file

    name -- name of the user to dump the data to
    history -- the history to dump to the file
    '''
    with open("data.json") as f:
        try:    #Try/catch block, will catch if data.json empty
            data = load(f)
        except:
            data = {}   #Set data to be blank
    data[name] = history
    with open('data.json', 'w') as f:
        dump(data, f)

def loadHistory(name):
    '''Function to load the history of a user from the json file

    name -- the name of the user to retrive the data from
    '''
    with open("data.json") as f:
        try:        #Try/catch block, will catch if data.json empty
            data = load(f)
            return data[name]
        except:
            return []   #If data.json is empty, return a blank list
        

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
            if history[i] == history[i - 1] and history[i - 1]:# == history[i - 2]:
                return beats(history[i])    #Check if the user is repeatedly playing the same action and play the counter
            else:
                break
        except: pass

    letters = history
    #tmplist = []
    for item in trainingData(): #Combine all the training data into the list
        letters = letters + item
    #letters = tmplist + history

    for i in range(len(letters)):
        if letters[i] == 0: #Convert the numbers to letters (then i can use grouby and sort on them)
            letters[i] = "a"
        elif letters[i] == 1:
            letters[i] = "b"
        elif letters[i] == 2:
            letters[i] = "c"

    groups = groupby(letters, key=lambda x: x[0])   #Group the letters
    predictions = [[a[0], sum (1 for _ in a[1])/float(len(letters))] for a in groups]   #This is the actual code that calculates the computer's next move

    highest = 0 #Var to store the highest certainty value
    move =  "a" #The move the computer is going to make
    for i in range(len(predictions)):
        if predictions[i][1] > highest: #Check if the certainty is higher than the saved one
            highest = predictions[i][1]
            move = predictions[i][0]

    if nprnd.choice([1, 2, 3, 4], p=[0.25, 0.25, 0.25, 0.25]) == 1: #Throw in a bit of random to switch things up
        return nprnd.choice(["rock", "paper", "scissors"], p=[0.34, 0.32, 0.34])               #Incase people start to catch on
    elif move == "a":
        return "rock"
    elif move == "b":
        return "paper"
    elif move == "c":
        return "scissors"
    else:
        return nprnd.choice(["rock", "paper", "scissors"], p=[0.34, 0.32, 0.34])   #Return random choice if something goes wrong and computer hasn't made choice