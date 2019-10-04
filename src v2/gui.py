#
#
#   This script is a computer implementation of rock paper scissors, for more details on this game please visit https://en.wikipedia.org/wiki/Rock-paper-scissors
#   This is the file responsible for creating and maintaining the user interface
#
#

from game import *      #Import from local file game.py  
from tkinter import PhotoImage, Toplevel, Label, Button, Entry, Frame, Menu, Tk, messagebox

def loadImage(file):
    '''Formats a file and returns it as an image

    file -- the input file
    '''

    return PhotoImage(file=".\\images\\{}".format(file))

class getName:
    '''Class to get the name of the user'''

    def __init__(self, parent):     
        '''Create input window for the user's name'''

        top = self.top = Toplevel(parent)
        self.top.configure(background=BACKGROUND)
        self.top.resizable(0, 0) 
        self.top.iconbitmap(r'.\\images\\icon.ico')
        Label(top, text="Name:", bg=BACKGROUND).pack()
        self.e = Entry(top, bg=BACKGROUND)
        self.e.pack(padx=5)
        b = Button(top, text="OK", bg=BACKGROUND, command=self.ok)
        b.pack(pady=5)
        self.top.bind("<Return>", self.ok)
        self.top.protocol("WM_DELETE_WINDOW", self.close)

    def ok(self, event = None):
        '''Gets called when the ok button is clicked'''

        global name
        name = self.e.get().lower().strip() #Set the global variable 'name' to the entereed user's name
        if name != "":
            self.top.destroy()  #Terminate the input window

    def close(self, event = None):
        '''Gets called when the window is closed (by the x button)'''

        global name
        name = "guest"  #Default to guest, this will not save data
        self.top.destroy()

class Window(Frame):
    def __init__(self, root = None):
        Frame.__init__(self, root)                
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", lambda : [dumpData(name, playerHistory=self.playerHistory, computerHistory=self.computerHistory, results=self.results), exit()])
        self.playerHistory, self.computerHistory, self.results = loadData(name)
        data = sampleData(None, files=["data-input.json"])
        self.sampleHistoryOne = data[0]
        self.sampleHistoryTwo = data[1]
        self.sampleResults = data[2]

        self.logout()   #Logout the user to get their username
        self.init_window()  #Initialize the main game window
        self.init_gameInfo()       #Initialize the game info window

    def init_window(self):  
        '''Init the main play window'''

        self.master.title(f"{TITLE} | Logged in as: {name}")    #Setup the window
        self.root.configure(background=BACKGROUND)
        self.root.geometry("{}x{}+0+0".format(WIDTH, HEIGHT))
        self.root.iconbitmap(r'.\\images\\icon.ico')
        self.root.resizable(0, 0) 

        #Load the images for the icons
        self.blankImage = loadImage("blank.gif")
        self.rockImage = loadImage("rock.gif")
        self.paperImage = loadImage("paper.gif")
        self.scissorsImage = loadImage("scissors.gif")

        #These are all objects of self so I can referance them in other functions (these are the interface widgets)
        self.simpleImages = True

        #Setup the menubar widgets, these are clickable
        self.menubar = Menu(self.root)  
        self.menubar.add_command(label="Clear Data", command=self.clearData)  
        self.menubar.add_command(label="Toggle Display Mode", command=self.toggleDisplay)  
        self.menubar.add_command(label="Logout", command=self.logout)  
        self.root.config(menu=self.menubar)  
    
        #Create the button widgets for the display
        self.rockButton = Button(self.root, image=self.rockImage, text="Rock", bg=BACKGROUND, command=lambda : self.play("rock"))
        self.rockButton.grid(row = 0, column = 0)
        self.rockButton.image = self.rockImage
        
        self.paperButton = Button(self.root, image=self.paperImage, text="Paper", bg=BACKGROUND, command=lambda : self.play("paper"))
        self.paperButton.grid(row = 0, column = 1)
        self.paperButton.image = self.paperImage

        self.scissorsButton = Button(self.root, image=self.scissorsImage, text="Scissors", bg=BACKGROUND, command=lambda : self.play("scissors"))
        self.scissorsButton.grid(row = 0, column = 2)
        self.scissorsButton.image = self.scissorsImage


        self.playerButton = Button(self.root, image=self.blankImage, text=" ", bg=BACKGROUND)
        self.playerButton.grid(row = 1, column = 0)
        self.playerButton.image = self.blankImage

        self.filler = Label(self.root, text="    vs    ", bg=BACKGROUND, font=("Courier", 20))
        self.filler.grid(row = 1, column = 1)

        self.computerButton = Button(self.root, image=self.blankImage, text=" ", bg=BACKGROUND)
        self.computerButton.grid(row = 1, column = 2)
        self.computerButton.image = self.blankImage

    def init_gameInfo(self):
        '''Init the game info window'''

        self.master = Tk()
        self.master.title(f"{TITLE} | Logged in as: {name}")
        self.master.configure(background=BACKGROUND)
        self.master.geometry("600x150+{}+0".format(WIDTH + 1))
        self.master.iconbitmap(r'.\\images\\icon.ico')
        self.master.resizable(0, 0) 

        #The lines of text on the second window, these are for displaying the round information
        self.line1 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line1.pack()

        self.line2 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line2.pack()

        self.line3 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line3.pack()

        self.line4 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line4.pack()

        self.line5 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line5.pack()

        self.master.protocol("WM_DELETE_WINDOW", lambda : [dumpData(name, playerHistory=self.playerHistory, computerHistory=self.computerHistory, results=self.results), exit()])
        self.master.mainloop()  

    def clearData(self):
        '''Clear the data of the current logged in user'''

        self.root.withdraw()
        MsgBox = messagebox.askquestion("Clear Data", "Are you sure you want to clear the data for: {}".format(name), icon = "warning")
        if MsgBox == "yes":     #Make sure the user meant to click this button and it wasn't an accident
            self.playerHistory = []
            self.computerHistory = []
            self.results = []
        self.root.deiconify()

    def toggleDisplay(self):
        '''Toggle between the real life and icon display'''

        self.simpleImages = not self.simpleImages   #Toggle the simpleImages bool

        if self.simpleImages:       #Load the new images
            self.rockImage = loadImage("rock.gif")
            self.paperImage = loadImage("paper.gif")
            self.scissorsImage = loadImage("scissors.gif")
        else:
            self.rockImage = loadImage("rock_real.gif")
            self.paperImage = loadImage("paper_real.gif")
            self.scissorsImage = loadImage("scissors_real.gif")

        #Re-create the buttons
        self.rockButton = Button(self.root, image=self.rockImage, text="Rock", bg=BACKGROUND, command=lambda : self.play("rock"))
        self.rockButton.grid(row = 0, column = 0)
        self.rockButton.image = self.rockImage
        
        self.paperButton = Button(self.root, image=self.paperImage, text="Paper", bg=BACKGROUND, command=lambda : self.play("paper"))
        self.paperButton.grid(row = 0, column = 1)
        self.paperButton.image = self.paperImage

        self.scissorsButton = Button(self.root, image=self.scissorsImage, text="Scissors", bg=BACKGROUND, command=lambda : self.play("scissors"))
        self.scissorsButton.grid(row = 0, column = 2)
        self.scissorsButton.image = self.scissorsImage


        self.playerButton = Button(self.root, image=self.blankImage, text=" ", bg=BACKGROUND)
        self.playerButton.grid(row = 1, column = 0)
        self.playerButton.image = self.blankImage

        self.filler = Label(self.root, text="    vs    ", bg=BACKGROUND, font=("Courier", 20))
        self.filler.grid(row = 1, column = 1)

        self.computerButton = Button(self.root, image=self.blankImage, text=" ", bg=BACKGROUND)
        self.computerButton.grid(row = 1, column = 2)
        self.computerButton.image = self.blankImage

    def logout(self):
        '''Logout the current user'''

        dumpData(name, playerHistory=self.playerHistory, computerHistory=self.computerHistory, results=self.results)

        self.root.withdraw()        #Hide both the other game windows
        self.master.withdraw()
        popup = getName(root)   #Load the other popup window to get the username
        self.root.wait_window(popup.top)
        self.root.deiconify()        #Unhide the fame windows
        self.master.deiconify()

        self.root.title(f"{TITLE} | Logged in as: {name}")  #Update the titles
        self.master.title(f"{TITLE} | Logged in as: {name}")

        self.playerHistory, self.computerHistory, self.results = loadData(name) #Re-load the data

    def play(self, playerMove):
        '''Gets called when the player plays a move

        playerMove -- the move the player has played
        '''

        timer = setTimer()  #Timer to time the function, it's just interesting data
        timer.start()
        
        #Call function for the computer to make it's move
        computerMove = calculateMove(name, self.playerHistory, self.computerHistory, self.results, self.sampleHistoryOne, self.sampleHistoryTwo, self.sampleResults)   
        
        timer.stop()
        print(f"Elapsed time: {timer.totalTime}")   #Gets printed to the console window

        self.playerHistory.append(queryNum(playerMove))        #Adds to history AFTER computer makes it's move (it doesn't cheat)
        self.computerHistory.append(queryNum(computerMove))

        gameData[0] += 1
        if playerMove == computerMove:
            gameData[1] += 1    #Draw
            msg = "Draw!"
            self.results.append(0)  #Update the storage var 
            self.filler["background"] = YELLOW  #Change colour of the square in the middle on the bottom row
            self.root.configure(background=YELLOW)         #Corrosponding to the game result
        elif beats(playerMove) != computerMove:
            gameData[2] += 1    #Win
            msg = "You win!"
            self.results.append(2)
            self.filler["background"] = GREEN
            self.root.configure(background=GREEN)
        else:
            gameData[3] += 1    #Lose
            msg = "You lose..."
            self.results.append(1)
            self.filler["background"] = RED
            self.root.configure(background=RED)

        if playerMove == "rock":    #Set the images that show who played what
            self.playerButton["image"] = self.rockImage
        elif playerMove == "paper":
            self.playerButton["image"] = self.paperImage
        elif playerMove == "scissors":
            self.playerButton["image"] = self.scissorsImage

        if computerMove == "rock":
            self.computerButton["image"] = self.rockImage
        elif computerMove == "paper":
            self.computerButton["image"] = self.paperImage
        elif computerMove == "scissors":
            self.computerButton["image"] = self.scissorsImage        

        self.updateInfo(f"You play {playerMove}, the computer plays {computerMove}. {msg}", f"You have won {round(gameData[2] / gameData[0] * 100, 2)}% of games", f"You have lost {round(gameData[3] / gameData[0] * 100, 2)}% of games", f"You have drawn {round(gameData[1] / gameData[0] * 100, 2)}% of games", f"You have played {gameData[0]} games")

    def updateInfo(self, *lines):
        '''Update the info on the game info window

        lines -- the lines to display
        '''

        self.line1.destroy()        #Deletes the lines
        self.line2.destroy()
        self.line3.destroy()
        self.line4.destroy()
        self.line5.destroy()

        self.line1 = Label(self.master, text=lines[0], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line1.pack()

        self.line2 = Label(self.master, text=lines[1], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line2.pack()

        self.line3 = Label(self.master, text=lines[2], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line3.pack()

        self.line4 = Label(self.master, text=lines[3], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line4.pack()

        self.line5 = Label(self.master, text=lines[4], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line5.pack()

if __name__ == '__main__':
    #Main function that runs when you run the file

    #RGB = lambda red, green, blue: "#%02x%02x%02x" % (red, green, blue)   #RGB to hex
    config = readConfig("config.json")
    WHITE = config["WHITE"]
    RED = config["RED"]
    YELLOW = config["YELLOW"]
    GREEN = config["GREEN"]
    BACKGROUND = config["BACKGROUND"]
    HEIGHT = config["HEIGHT"]
    WIDTH = config["WIDTH"]
    TITLE = config["TITLE"]
    FONTSIZE = config["FONTSIZE"]

    name = "guest"
    gameData = [0, 0, 0, 0] #Stores: [total games, draws, wins, loses]

    root = Tk()
    app = Window(root)
    root.mainloop()  