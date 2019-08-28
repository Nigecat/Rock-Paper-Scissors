#py -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
import numpy as np
from json import dump, load

class neuralNetwork:
    pass

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
    if action == 0:
        return "paper"
    elif action == 1:
        return "scissors"
    elif action == 2:
        return "rock"

def calculateMove(name, history):
    #Rock: 0
    #Paper: 1
    #Scissors: 2

    #print("History: {}".format(history))

    if len(history) == 0:   #If the history is blank (then we have no data)
        #Pick a random option, this is weighted random because statistically, people play rock on the first turn. 
        #So we have paper as most likely, the others are there in case people catch on (to switch things up).
        return np.random.choice(["rock", "paper", "scissors"], p=[0.2, 0.6, 0.2]) 

    #Else:
    for i in range(len(history) - 1, -1, -1):
        try:
            if history[i] == history[i - 1] and history[i - 1] == history[i - 2]:
                return beats(history[i])
            else:
                break
        except: pass

    #Neural network here


    

    #return "rock"
    return None