import PySimpleGUI as sg
from game import calculateMove, dumpHistory, loadHistory

def getName():
    layout = [  
        [sg.Text('Name: ', size = (10, 1)), sg.InputText()],        
        [sg.Submit()], 
        [sg.Text('(Please enter your real name, as it will improve your experience of the game)', size = (60, 1))]
    ]
    window = sg.Window('Rock-Paper-Scissors').Layout(layout)  
    while True:
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
        if event == "rock" or event == "paper" or event == "scissors":  
            move = calculateMove(name, history)
            if event == "rock": #This happens AFTER the computer makes it's move
                history.append(0)
            elif event == "paper":
                history.append(1)
            elif event == "scissors":
                history.append(2)
            print(history[-1], move)
    dumpHistory(name, history)

runGUI()