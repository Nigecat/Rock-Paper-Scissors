from json import dump, load
from random import choices as rndchoice

def rndmove(**args):
    '''Function to return a random move

    args -- arguments for the functions, if the population is left blank. It will default to (rock, paper, scissors)
    '''
    if "population" in args.keys() and "weights" in args.keys():
        return ''.join(rndchoice(population=args["population"], weights=args["weights"]))
    elif "weights" in args.keys() and "population" not in args.keys():
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=args["weights"]))
    else:
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.333, 0.334, 0.333])) 

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

def trainingData(*files, **args):
    '''Function to retrive the training data

    Pulls data from file.json, returns a list of all the values, can take multiple files as input, can ignore certain keys
    '''

    files = [".\\data\\" + item for item in files]

    data = {}
    for file in files:
        with open(file) as f:
            data = {**data, **load(f)}

    for item in args["ignore"]:
        data.pop(item, None)
    #bytearray(utf-8)   #Bytearray will increase the run speed (hypothetically, in reality - it doesn't work)
    return [data[key] for key in data.keys()]

def dumpData(name, **data):
    '''Function to dump the current data to the json file

    name -- name of the user to dump the data to
    data -- the data to dump to the file (dict)
    '''

    if name != "guest":
        tmp = {}
        tmp[name] = data
        data = tmp
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
                return [], [], []   #If data-user.json is empty, return a blank list

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



def calculateMove(name, playerHistory, computerHistory, results):
    '''Function to calculate the computer's move

    name -- the name of the user playing
    playerHistory -- the user's history
    computerHistory -- the user's history
    results -- the game results
    Note for code reading:
        Rock: 0
        Paper: 1
        Scissors: 2
    '''

    # TODO Re-write this entire thing