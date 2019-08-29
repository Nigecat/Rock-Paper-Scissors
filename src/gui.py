from sys import path
try: 
    path.insert(0, './libs')    #Change running directory to the libs folder
    import PySimpleGUI as sg   #Non std lib, import from local
except ImportError:
    print("PySimpleGUI was unable to be imported properly...")
    input()
from game import calculateMove, dumpHistory, loadHistory, queryName, beats  #Imports from game.py

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

def runGUI():
    #name = getName()
    name = "nigel"
    history = loadHistory(name)
    games = []
    layout = [
        [sg.Menu([['Menu', ['Logout']]])],
        [sg.ReadFormButton('rock', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\rock.gif"), sg.Text(""),
            sg.ReadFormButton('paper', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\paper.gif"), sg.Text(""),
            sg.ReadFormButton('scissors', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\scissors.gif"), sg.Text("")]
    ]
    window =  sg.Window('Rock-Paper-Scissors', background_color = "#fff").layout(layout) #, icon=r"images\\icon.ico")
    while True:
        event = window.Read()[0]
        if event == None:
            break
        if event == "Logout":
            name = getName()
            history = loadHistory(name)
            games = []
        if event == "rock" or event == "paper" or event == "scissors":  
            move = calculateMove(name, history)
            if event == "rock": #This happens AFTER the computer makes it's move
                history.append(0)
            elif event == "paper":
                history.append(1)
            elif event == "scissors":
                history.append(2)
            print("You play {}. The computer plays {}. ".format(queryName(history[-1]), move))
            if queryName(history[-1]) == move:
                pass
                #print("Draw!")
            elif beats(queryName(history[-1])) != move:
                games.append(1)
                #print("You win!")
            else:
                games.append(0)
                #print("You lose!")
            wins = 0
            for item in games:
                if item == 1:
                    wins += 1
            print("Your win rate: {}%".format(wins / len(games) * 100))
            #print("Your lose rate: {}%".format(100 - (wins / len(games) * 100)))

    dumpHistory(name, history)  #Run when the x is pressed

if __name__ == '__main__':
    runGUI()