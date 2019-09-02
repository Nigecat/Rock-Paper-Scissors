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
    if "weights" in args.keys():
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

def sampleData(key, **files):
    '''Function to retrive the sample (input) data

    Pulls data from [files.json], returns a list of all the values, can take multiple files as input, can ignore certain keys
    '''

    files = files["files"]

    files = [".\\data\\" + item for item in files]

    data = {}
    for file in files:
        with open(file) as f:
            data = {**data, **load(f)}

    if key == None:
        return [data[key] for key in data.keys()]
    else:
        return data[key]


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



def calculateMove(name, playerHistory, computerHistory, results, sampleHistoryOne, sampleHistoryTwo, sampleResults):
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

    CHECK_RANGE = 3 #Basically a difficulty setting (lower = easier)

    if len(playerHistory) < CHECK_RANGE:   #If the history is blank (then we have no data) or under the check range
        #Pick a random option, this is weighted random because statistically, people play rock on the first turn. 
        return rndmove(weights=[0.3, 0.4, 0.3])

    #Else: (we don't need an else statement because return will stop the code)
    for i in range(len(playerHistory) - 1, -1, -1):   #Run through the playerHistory backwards
        try:
            if playerHistory[i] == playerHistory[i - 1] == playerHistory[i - 2]:
                return beats(playerHistory[i])    #Check if the user is repeatedly playing the same action and play the counter
            else:
                break
        except IndexError: pass

    searchPlayer = []
    searchComputer = []
    searchResults = []
    playerHistory.reverse()  #It's faster to work from the start of the list
    computerHistory.reverse()
    results.reverse()
    for i in range(CHECK_RANGE):    #This isn't the most line efficient way to do it, but it means I only have to loop through the list once (to decrease runtime length)
        searchPlayer.append(playerHistory[i])
        searchComputer.append(computerHistory[i])
        searchResults.append(results[i])
    playerHistory.reverse() 
    computerHistory.reverse()
    results.reverse()
    searchPlayer.reverse()
    searchComputer.reverse()
    searchResults.reverse()

    predictions = []
    for i in range(len(results) - CHECK_RANGE):
        add = True
        for x in range(len(searchResults)):
            if playerHistory[i + x] == searchPlayer[x] and computerHistory[i + x] == searchComputer[x] and results[i + x] == searchResults[x]:
                continue
            else:
                add = False
        if add:     #Patterns from the user's history are weighted 300 times more heavily than the other data
            predictions = predictions + [sampleHistoryTwo[i + CHECK_RANGE]] * 300

    for i in range(len(sampleResults) - CHECK_RANGE):
        add = True
        for x in range(len(searchResults)):
            if sampleHistoryOne[i + x] == searchPlayer[x] and sampleHistoryTwo[i + x] == searchComputer[x] and sampleResults[i + x] == searchResults[x]:
                continue
            else:
                add = False
        if add:
            predictions = predictions + [sampleHistoryTwo[i + CHECK_RANGE]]

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
        return rndmove(weights=[0.0, 0.5, 0.5])
    elif close(rock, scissors, DIFFERENCE):
        return rndmove(weights=[0.5, 0.5, 0])
    elif close(paper, scissors, DIFFERENCE):
        return rndmove(weights=[0.5, 0, 0.5])
    else:   #If none of them are close
        #Return what beats the highest prediction for what the user will play
        if rock > paper and rock > scissors:
            return beats("rock")
        elif paper > rock and paper > scissors:
            return beats("paper")
        elif scissors > rock and scissors > paper:
            return beats("scissors")
        else:
            return rndmove()    #Incase something goes wrong

if __name__ == '__main__':  #If you run this file, redirect you to the other file
    from os import system
    system("gui.py")