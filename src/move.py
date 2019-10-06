#
#
#   Please read gui.py first
#   This is the file responsible for generating the computer's move
#
#

from utils import *

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

    config = readConfig("config.json")
    CHECK_RANGE = config["CHECK_RANGE"]     #A difficulty setting (lower = easier), default is 3 (not recommended to increase it further than 5)
    PLAYER_WEIGHTING = config["PLAYER_WEIGHTING"]     #THe weighting for the user data compared to the input data (a multiplier)
    DIFFERENCE= config["DIFFERENCE"]     #Difference between percentages for it to pick randomly

    if len(playerHistory) < CHECK_RANGE:   #If the history is blank (then we have no data) or under the check range
        #Pick a random option, this is weighted random because statistically, people play rock on the first turn. 
        return rndmove(weights=[0.3, 0.4, 0.3])

    else: #we don't need an else statement because return will stop the code
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
    playerHistory.reverse()     #Put the lists back the right way round
    computerHistory.reverse()
    results.reverse()
    searchPlayer.reverse()  #Since we did it backwards, the output would also be backwards, so we need to reverse it
    searchComputer.reverse()
    searchResults.reverse()

    predictions = []
    for i in range(len(results) - CHECK_RANGE):
        add = True
        for x in range(len(searchResults)): #Run through the results and check if there are any patterns matching the user data of the length of the check range
            if playerHistory[i + x] == searchPlayer[x] and computerHistory[i + x] == searchComputer[x] and results[i + x] == searchResults[x]:
                continue
            else:
                add = False
        if add:     #Patterns from the user's history are weighted 300 times more heavily than the other data
            predictions = predictions + [sampleHistoryTwo[i + CHECK_RANGE]] * PLAYER_WEIGHTING

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

    try: 
        #Convert the totals to percentages (certainty)
        getPercent = lambda count, total: round((count / total) * 100, 2)  #Temp funct to get the percent
        rock = getPercent(rock, total)
        paper = getPercent(paper, total)
        scissors = getPercent(scissors, total)

        print(f"Predictions: Rock: {rock}% | Paper: {paper}% | Scissors: {scissors}% | Data pulled from {total} samples")   #The percentage certainty of what it thinks the player is going to play

        close = lambda num1, num2, dif: abs(num1 - num2) <= dif
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
                return rndmove()    #Incase they are all exactly the same

    except ZeroDivisionError:
        return rndmove()

if __name__ == '__main__':  #If you run this file, redirect you to the other file
    from os import system
    system("gui.py")