#
#
#   This file is used for storing the utility function, these are general use functions
#
#

from json import load
from time import process_time
from tkinter import PhotoImage
from random import choices as rndchoice

class setTimer(object):
    '''Function to create a timer object
    
    This is just interesting data on how the game is going
    '''

    def __init__(self):
        self.startTime = 0
        self.stopTime = 0
        self.totalTime = 0

    def start(self):
        '''Start the timer'''
        self.startTime = process_time()

    def stop(self):
        '''Stop the timer'''
        self.stopTime = process_time()
        self.totalTime = self.stopTime - self.startTime

def loadImage(file):
    '''Formats a file and returns it as an image

    file -- the input file
    '''

    return PhotoImage(file=".\\images\\{}".format(file))

def readConfig(file):
    '''Function to read the config file

    file -- the config file to read (json)
    '''

    with open("config.json") as f:
        data = load(f)

    return data

def rndmove(**args):
    '''Function to return a random move

    args -- arguments for the functions, if no weights are included, it will default to 33/33/33
    '''

    if "weights" in args.keys():
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=args["weights"]))
    else:
        return ''.join(rndchoice(population=["rock", "paper", "scissors"], weights=[0.3333, 0.3334, 0.3333])) 

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

if __name__ == '__main__':
    from os import system
    system("gui.py")