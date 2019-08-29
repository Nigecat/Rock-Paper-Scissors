from sys import path
try: 
    path.insert(0, './libs')    #Change running directory to the libs folder
    import PySimpleGUI as sg   #Non std lib, import from local
except ImportError:
    print("PySimpleGUI was unable to be imported properly...")
    input()
from game import calculateMove, dumpHistory, loadHistory, queryName, beats  #Imports from game.py

def updateGUI(winRate, playerMove, computerMove):
    playerPath = ".\\images\\{}.gif".format(playerMove)
    computerPath = ".\\images\\{}.gif".format(computerMove)
    layout = [
        [sg.Menu([['Menu', ['Logout']]])],
        [sg.ReadFormButton('rock', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\rock.gif"), sg.Text(""),
            sg.ReadFormButton('paper', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\paper.gif"), sg.Text(""),
            sg.ReadFormButton('scissors', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\scissors.gif"), sg.Text("")],
        [sg.ReadFormButton(playerMove, button_color=sg.TRANSPARENT_BUTTON, image_filename=playerPath), sg.Text("               vs                 "),
            sg.ReadFormButton(computerMove, button_color=sg.TRANSPARENT_BUTTON, image_filename=computerPath), sg.Text("")],
        [sg.Text("Your win rate is: {}%".format(winRate))]

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

def runGUI():
    #name = getName()
    name = "nigel"
    history = loadHistory(name)
    games = []
    layout = [
        [sg.Menu([['Menu', ['Logout']]])],
        [sg.ReadFormButton('rock', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\rock.gif"), sg.Text(""),
            sg.ReadFormButton('paper', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\paper.gif"), sg.Text(""),
            sg.ReadFormButton('scissors', button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\scissors.gif"), sg.Text("")],

        [sg.ReadFormButton("", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\blank.gif"), sg.Text("               vs                 "),
            sg.ReadFormButton("", button_color=sg.TRANSPARENT_BUTTON, image_filename=".\\images\\blank.gif"), sg.Text("")],
        [sg.Text("Your win rate is: UNDEFINED", key="rate")] 
    ]

    window =  sg.Window('Rock-Paper-Scissors', background_color = "#fff", layout=layout)#, icon=r"images\\icon.ico")
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
            #print("You play {}. The computer plays {}. ".format(queryName(history[-1]), move))
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
            #try:
            #    print("Your win rate: {}%".format(wins / len(games) * 100))
            #except ZeroDivisionError:
            #    print("Your win rate: 0%")
            #print("Your lose rate: {}%".format(100 - (wins / len(games) * 100)))
            try:
                window.Hide()
                window = updateGUI(wins / len(games) * 100, queryName(history[-1]), move)
            except ZeroDivisionError:
                window = updateGUI(0, queryName(history[-1]), move)

    dumpHistory(name, history)  #Run when the x is pressed

if __name__ == '__main__':
    runGUI()