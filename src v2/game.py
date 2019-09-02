from json import dump, load
from time import process_time
from random import choices as rndchoice

class setTimer(object):
    def __init__(self):
        self.startTime = 0
        self.stopTime = 0
        self.totalTime = 0

    def start(self):
        self.startTime = process_time()

    def stop(self):
        self.stopTime = process_time()
        self.totalTime = self.stopTime - self.startTime

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

def sampleData(*files, **args):
    '''Function to retrive the sample (input) data

    Pulls data from [files.json], returns a list of all the values, can take multiple files as input, can ignore certain keys
    '''

    files = [".\\data\\" + item for item in files]

    data = {}
    for file in files:
        with open(file) as f:
            data = {**data, **load(f)}

    for item in args["ignore"]:
        data.pop(item, None)
    #bytearray(utf-8)   #Bytearray will increase the run speed (hypothetically, in reality - I can't get it to work)
    return [data[key] for key in data.keys()][0]

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

    if len(playerHistory) < 4:   #If the history is blank (then we have no data) or under 4
        #Pick a random option, this is weighted random because statistically, people play rock on the first turn. 
        return rndmove(weights=[0.3, 0.4, 0.3])

    #Else: (we don't need an else statement because return will stop the code)
    for i in range(len(playerHistory) - 1, -1, -1):   #Run through the playerHistory backwards
        try:
            if playerHistory[i] == playerHistory[i - 1] == playerHistory[i - 2]:
                return beats(playerHistory[i])    #Check if the user is repeatedly playing the same action and play the counter
            else:
                break
        except: pass

    sampleHistoryOne = sampleData("data-input.json", ignore=["playerTwo", "results"])
    sampleHistoryTwo = sampleData("data-input.json", ignore=["playerOne", "results"])
    sampleResults = sampleData("data-input.json", ignore=["playerOne", "playerTwo"])

    CHECK_RANGE = 3

    predictions = []

    searchStrPlayer = [playerHistory[i] for i in range(len(playerHistory) - 1, len(playerHistory) - CHECK_RANGE - 1,-1) ]
    searchStrComputer = [computerHistory[i] for i in range(len(computerHistory) - 1, len(computerHistory) - CHECK_RANGE - 1,-1) ]

    if len(playerHistory) >= CHECK_RANGE:
        for i in range(len(sampleHistoryOne) - CHECK_RANGE):
            for j in range(len(playerHistory) - CHECK_RANGE):
                for x in range(1, CHECK_RANGE + 1):
                    if sampleHistoryOne[i + x] == playerHistory[j + x] and sampleHistoryTwo[i + x] == computerHistory[j + x] and sampleResults[i + x] == results[j + x]:
                        if x == CHECK_RANGE:
                            predictions.append(sampleHistoryOne[i + x + 1])
                    else:
                        break

    if predictions == []:   #If it can't make any predictions return a random move
        return rndmove()

    rock = predictions.count(0) #Count the total of each move
    paper = predictions.count(1)
    scissors = predictions.count(2)
    total = rock + paper + scissors #This if for calculating percentages

    #Convert the totals to percentages (certainty)
    getPercent = lambda count, total: round((count / total) * 100, 2)
    rock = getPercent(rock, total)
    paper = getPercent(paper, total)
    scissors = getPercent(scissors, total)

    print(f"Predictions: Rock: {rock}% | Paper: {paper}% | Scissors: {scissors}% | Data pulled from {total} samples")

    close = lambda num1, num2, dif: abs(num1 - num2) <= dif
    DIFFERENCE = 3  #Difference between percentages for it to pick randomly
    if close(rock, paper, DIFFERENCE):  #Check if any of the predictions are close, and if they are return one of them randomly (to make it less predictable)
        return rndmove(weights=[0.5, 0.5, 0])
    elif close(rock, scissors, DIFFERENCE):
        return rndmove(weights=[0.5, 0, 0.5])
    elif close(paper, scissors, DIFFERENCE):
        return rndmove(weights=[0, 0.5, 0.5])
    else:   #If none of them are close
        #Return what beats the highest prediction for what the user will play
        if rock > paper and rock > scissors:
            return beats("rock")
        elif paper > rock and paper > scissors:
            return beats("paper")
        elif scissors > rock and scissors > paper:
            return beats("scissors")