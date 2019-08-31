from random import randint
from json import dump, load
#from numpy import array, int8   #External library
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

    #data = list(chain.from_iterable([data[key] for key in data.keys()]))
    #return array(data, dtype=int8)   #Return all the values of the dicts in a list, store them as 8 bit integers
    return [data[key] for key in data.keys()]

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
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.3, 0.4, 0.3]))

    #Else: (we don't need an else statement because return will stop the code)
    for i in range(len(history) - 1, -1, -1):   #Run through the history backwards
        try:
            if history[i] == history[i - 1] == history[i - 2]:
                return beats(history[i])    #Check if the user is repeatedly playing the same action and play the counter
            else:
                break
        except: pass

    data = []
    for item in trainingData("data-training.json", "data-training-study.json"): 
        data = data + item      #Load the data into a list

    #data = data + history

    search = [] #Var to store the characters to search for
    history.reverse()   #Reverse history, because in python it is faster to referance the start of the list than the end
    try:
        search.append(history[0])   #Grab the first 4 entries of the list (that latest 4 moves)
        search.append(history[1])       #This will return a IndexError if history is too short
        search.append(history[2])
        search.append(history[3])
    except IndexError:
        history.reverse()   #Put history back to how it was and return a random response
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.33, 0.34, 0.33]))
    finally:
        history.reverse()   #Put history back to normal
        search.reverse()    #Put search back the right way round

    predictions = []    #List to store the predictions of the user's next move
    for i in range(len(data)):  #Run through all the input data
        try:
            if data[i] == search[0] and data[i + 1] == search[1] and data[i + 2] == search[2] and data[i + 3] == search[3]:
                predictions.append(data[i + 4]) #Check if any patterns match and add the next move to the predictions
        except IndexError:
            break

    rock = predictions.count(0) #Count the total of each move
    paper = predictions.count(1)
    scissors = predictions.count(2)
    total = rock + paper + scissors

    print(f"Rock: {round((rock / total) * 100, 2)}% | Paper: {round((paper / total) * 100, 2)}% | Scissors: {round((scissors / total) * 100, 2)}%")

    #Return what beats the highest prediction for what the user will play
    if rock > paper and rock > scissors:
        return beats("rock")
    elif paper > rock and paper > scissors:
        return beats("paper")
    elif scissors > rock and scissors > paper:
        return beats("scissors")