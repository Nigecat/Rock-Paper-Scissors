from json import dump
from random import choice
from pandas import read_excel

print("Loading spreadsheet...")
dt = read_excel("Rock_Paper_Scissors_Raw.xlsx")
playerOne = dt["player_one_throw"]
playerTwo = dt["player_two_throw"]

playerOne = [x if x != 3 else choice([0, 1, 2]) for x in playerOne]
playerTwo = [x if x != 3 else choice([0, 1, 2]) for x in playerTwo]

data = {
    "playerOne": playerOne,
    "playerTwo": playerTwo
}

with open("excelOut.json", "w") as f:
    dump(data, f)