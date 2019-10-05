#
#
#   The input data the program uses to create it's move was sourced from an excel spreadsheet, this code converts the spreadsheet into json
#
#

from json import dump
from random import choice
from pandas import read_excel

def beats(action):
    if action == 0:
        return 1
    elif action == 1:
        return 2
    elif action == 2:
        return 0

print("Loading spreadsheet...")
dt = read_excel("Rock_Paper_Scissors_Raw.xlsx")
gameId = dt["game_id"]
playerOne = dt["player_one_throw"]
playerTwo = dt["player_two_throw"]

print("Formatting data...")

print("     (player one)")
playerOne = [x - 1 if x != 0 else choice([0, 1, 2]) for x in playerOne]

print("     (player two)")
playerTwo = [x - 1if x != 0 else choice([0, 1, 2]) for x in playerTwo]

print("     (results)")
results = []
for i in range(len(playerOne)):
    if playerOne[i] == playerTwo[i]:
        results.append(0)    #Draw
    elif beats(playerOne[i]) == playerTwo[i]:
        results.append(1)   #Lose
    else:
        results.append(2)    #Win

data = {
    "playerOne": playerOne,
    "playerTwo": playerTwo,
    "results": results
}

print("Dumping json...")

with open("excelOut.json", "w") as f:
    dump(data, f)

input("DONE")