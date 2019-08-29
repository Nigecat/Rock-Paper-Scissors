#!/usr/bin/env python
from sys import path
try: 
    path.insert(0, './libs')    #Change running directory to the libs folder
    import PySimpleGUI as sg   #Non stdlib, import from local file
except ImportError:
    from tkinter import messagebox, Tk  #We do this because you can't see the console window
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Rock-Paper-Scissors", "PySimpleGUI was unable to be imported...")
    quit()
from game import calculateMove, dumpHistory, loadHistory, queryName, beats  #Imports from game.py

def updateGUI(winRate, playerMove, computerMove, msg, games):
    playerPath = ".\\images\\{}.gif".format(playerMove)
    computerPath = ".\\images\\{}.gif".format(computerMove)
    layout = [
        [sg.Menu([['Menu', ['Logout']]])],
        [sg.ReadFormButton("r", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\rock.gif"), sg.Text(""),
            sg.ReadFormButton("p", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\paper.gif"), sg.Text(""),
            sg.ReadFormButton("s", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\scissors.gif"), sg.Text("")],
        [sg.Text("", background_color="white")],
        [sg.Text("You play: {}".format(playerMove), background_color="white"), sg.Text("                          The computer plays: {}".format(computerMove), background_color="white")],
        [sg.ReadFormButton("", button_color=sg.TRANSPARENT_BUTTON, image_filename=playerPath), sg.Text("               vs                 ", background_color="white"),
            sg.ReadFormButton("", button_color=sg.TRANSPARENT_BUTTON, image_filename=computerPath), sg.Text("")],
        [sg.Text(msg, background_color="white"), sg.Text("Your win rate is: {}%, the number of games played is: {}".format(winRate, games), background_color="white")]

        #[sg.Text(gameAction)],
        #[sg.Text("Your win rate is {}%".format(winRate))]
    ]
    #layout.append('sg.ReadFormButton("{}", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\{}.gif"), sg.Text("")'.format(computerMove, computerMove))


    return sg.Window('Rock-Paper-Scissors', background_color = "#fff").layout(layout) 

def getName():
    layout = [  
        [sg.Text('Name: ', size = (10, 1)), sg.InputText()],        
        [sg.Submit()], 
        [sg.Text('(Please enter your real name, as it will improve your experience of the game)', size = (60, 1))]
    ]
    window = sg.Window('Rock-Paper-Scissors').Layout(layout)  
    while True:
        if window.Read()[0] == None:
            return "guest"
        name = window.Read()[1][0].lower().strip() 
        if name != "":
            try:
                return name
            finally:
                window.Hide()

def main():
    #name = getName()
    name = "nigel"
    history = loadHistory(name)
    games = []
    layout = [
        [sg.Menu([['Menu', ['Logout']]])],
        [sg.ReadFormButton("r", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\rock.gif"), sg.Text(""),
            sg.ReadFormButton("p", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\paper.gif"), sg.Text(""),
            sg.ReadFormButton("s", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\scissors.gif"), sg.Text("")],
    ]

    window =  sg.Window('Rock-Paper-Scissors', background_color = "white", layout=layout)#, icon=r"images\\icon.ico")
    while True:
        event = window.Read()[0]
        if event == None:
            break
        if event == "Logout":
            name = getName()
            history = loadHistory(name)
            games = []
        if event == "r" or event == "p" or event == "s":  
            move = calculateMove(name, history) #Calculate move is a function from game.py
            if event == "r": #This happens AFTER the computer makes it's move
                history.append(0)
            elif event == "p":
                history.append(1)
            elif event == "s":
                history.append(2)
            #print("You play {}. The computer plays {}. ".format(queryName(history[-1]), move))
            if queryName(history[-1]) == move:
                msg = "Draw!"
            elif beats(queryName(history[-1])) != move:
                games.append(1)
                msg = "You win!"
            else:
                games.append(0)
                msg = "You lose..."
            wins = 0
            for item in games:
                if item == 1:
                    wins += 1
            #try:
            #    print("Your win rate: {}%".format(wins / len(games) * 100))
            #except ZeroDivisionError:
            #    print("Your win rate: 0%")
            #print("Your lose rate: {}%".format(100 - (wins / len(games) * 100)))
            try:
                #window.Hide()
                window = updateGUI(wins / len(games) * 100, queryName(history[-1]), move, msg, len(games))
            except ZeroDivisionError:
                window = updateGUI(0, queryName(history[-1]), move, msg, len(games))

    dumpHistory(name, history)  #Run when the x is pressed

if __name__ == '__main__':
    main()