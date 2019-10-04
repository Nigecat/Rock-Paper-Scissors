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

    # TODO Implement using the computer history and results into the algorithm

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

    data = []
    for item in trainingData("data-input.json", ignore="results"): #Read the input data and ignore the results column
        data = data + item      #Load the data into a list

    #data = data + playerHistory

    search = [] #Var to store the characters to search for
    playerHistory.reverse()   #Reverse playerHistory, because in python it is faster to referance the start of the list than the end
    try:
        search.append(playerHistory[0])   #Grab the first 4 entries of the list (that latest 4 moves)
        search.append(playerHistory[1])       #This will return a IndexError if playerHistory is too short
        search.append(playerHistory[2])
        search.append(playerHistory[3])
    except IndexError:
        playerHistory.reverse()   #Put playerHistory back to how it was and return a random move
        return rndmove()
    finally:
        playerHistory.reverse()   #Put playerHistory back to normal
        search.reverse()    #Put search back the right way round

    predictions = []    #List to store the predictions of the user's next move
    for i in range(len(data)):  #Run through all the input data
        try:
            if data[i] == search[0] and data[i + 1] == search[1] and data[i + 2] == search[2] and data[i + 3] == search[3]:
                predictions.append(data[i + 4]) #Check if any patterns match and add the next move to the predictions
        except IndexError:
            break
        
    for i in range(len(playerHistory)):  #Run through all the input data (same but for playerHistory (since that has a higher weighting))
        try:
            if playerHistory[i] == search[0] and playerHistory[i + 1] == search[1] and playerHistory[i + 2] == search[2] and playerHistory[i + 3] == search[3]:
                #These have 300x more weight than the pattern matching from the input data
                #predictions.append(playerHistory[i + 4]) #Check if any patterns match and add the next move to the predictions
                if playerHistory[i + 4] == 0:
                    predictions = predictions + [playerHistory[i + 4]] * 600  #Weighting for rock is heigher
                else:
                    predictions = predictions + [playerHistory[i + 4]] * 300
        except IndexError:
            break

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

if __name__ == '__main__':
    from os import system
    system("game.py")