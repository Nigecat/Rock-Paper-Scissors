from random import randint
from json import dump, load
from itertools import groupby
from random import choices as rndchoice

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

def queryNum(action):
    '''Function to return the number of the action that corresponds to a name

    action -- the action to get the number of
    '''
    if action == "rock":
        return 0
    elif action == "paper":
        return 1
    elif action == "scissors":
        return 2

def trainingData(*files):
    '''Function to retrive the training data

    Pulls data from file.json, returns a list of all the values, can take multiple files as input
    '''

    files = [".\\data\\" + item for item in files]

    data = {}
    for file in files:
        with open(file) as f:
            data = {**data, **load(f)}
    return [data[key] for key in data.keys()]   #Return all the values of the dicts in a list

def dumpHistory(name, history):
    '''Function to dump the current history to the json file

    name -- name of the user to dump the data to
    history -- the history to dump to the file
    '''
    if name != "guest":
        with open(".\\data\\data-user.json") as f:
            try:    #Try/catch block, will catch if data-user.json empty
                data = load(f)
            except:
                data = {}   #Set data to be blank
        data[name] = history
        with open(".\\data\\data-user.json", "w") as f:
            dump(data, f)

def loadHistory(name):
    '''Function to load the history of a user from the json file

    name -- the name of the user to retrive the data from
    '''
    if name != "guest":
        with open(".\\data\\data-user.json") as f:
            try:        #Try/catch block, will catch if data-use.json empty
                data = load(f)
                return data[name]
            except:
                return []   #If data-use.json is empty, return a blank list
        

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
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.3, 0.4, 0.3]))

    #Else: (we don't need an else statement because return will stop the code)
    for i in range(len(history) - 1, -1, -1):   #Run through the history backwards
        try:
            if history[i] == history[i - 1]:# == history[i - 2]:
                if randint(0, 1) == 1:
                    if history[i] == history[i - 1] == history[i - 2]:
                        return beats(history[i])    #Check if the user is repeatedly playing the same action and play the counter
                else:
                    return beats(history[i])
            else:
                break
        except: pass

    data = []
    for item in trainingData("data-training.json", "data-training-study.json"): 
        data = data + item     

    for i in range(len(data)):
        if data[i] == 0: #Convert the numbers to letters (then i can use grouby and sort on them)
            data[i] = "a"
        elif data[i] == 1:
            data[i] = "b"
        elif data[i] == 2:
            data[i] = "c"

    groups = groupby(data, key=lambda x: x[0])   #Group the letters
    predictions = [[a[0], sum (1 for _ in a[1]) / float(len(data))] for a in groups]   #This is the actual code that calculates the computer's next move

    #print(predictions)     #TODO: Write code to show individual percentages

    highest = 0 #Var to store the highest certainty value
    move = "a" #The move the computer is going to make
    for i in range(len(predictions)):
        if predictions[i][1] > highest: #Check if the certainty is higher than the saved one
            highest = predictions[i][1]
            move = predictions[i][0]

    if ''.join(rndchoice(["1", "2", "3", "4"], [0.25, 0.25, 0.25, 0.25])) == "1": #Throw in a bit of random to switch things up
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.33,  0.34, 0.33]) )              #Incase people start to catch on
    elif move == "a":
        return "rock"
    elif move == "b":
        return "paper"
    elif move == "c":
        return "scissors"
    else:
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.33,  0.34, 0.33]))   #Return random choice if something goes wrong and computer hasn't made choice