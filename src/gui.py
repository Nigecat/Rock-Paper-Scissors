#from game import *     #VSCode hates wildcard import and literaly throws hundreds of errors at the unused functions
from sys import exit
#from tkinter import *      # ^^ Same as above, I will uncomment these before submitting if I remember
from tkinter import PhotoImage, Toplevel, Label, Button, Entry, Frame, Menu, Tk
from game import queryName, queryNum, calculateMove, dumpHistory, loadHistory, beats  #Local import from game.py

def loadImage(file):
    return PhotoImage(file=".\\images\\{}".format(file))

class getName:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.top.configure(background=BACKGROUND)
        self.top.iconbitmap(r'.\\images\\icon.ico')
        Label(top, text="Name:", bg=BACKGROUND).pack()
        self.e = Entry(top, bg=BACKGROUND)
        self.e.pack(padx=5)
        b = Button(top, text="OK", bg=BACKGROUND, command=self.ok)
        b.pack(pady=5)

    def ok(self):
        global name
        name = self.e.get().lower().strip()
        if name != "":
            self.top.destroy()

class Window(Frame):
    def __init__(self, root = None):
        Frame.__init__(self, root)                
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", lambda : [dumpHistory(name, self.history), exit()])
        self.history = loadHistory(name)
        self.init_window()
        self.init_gameInfo()

    def init_window(self):  
        self.root.title(TITLE)
        self.root.configure(background=BACKGROUND)
        self.root.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.root.iconbitmap(r'.\\images\\icon.ico')

        self.blankImage = loadImage("blank.gif")
        self.rockImage = loadImage("rock.gif")
        self.paperImage = loadImage("paper.gif")
        self.scissorsImage = loadImage("scissors.gif")

        #These are all objects of self so I can referance them in other functions
        self.simpleImages = True
        self.showStats = False

        self.menubar = Menu(self.root)  
        self.menubar.add_command(label="Toggle Display Mode", command=self.toggleDisplay)  
        self.menubar.add_command(label="Toggle Interesting Stats", command=self.toggleStats)  
        self.menubar.add_command(label="Logout", command=self.logout)  
        self.root.config(menu=self.menubar)  
    
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
        self.master = Tk()
        self.master.title(TITLE)
        self.master.configure(background=BACKGROUND)
        self.master.geometry("1600x100+800+400")
        self.master.iconbitmap(r'.\\images\\icon.ico')

        self.line1 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line1.pack()

        self.line2 = Label(self.master, text=" ", font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line2.pack()

        self.master.protocol("WM_DELETE_WINDOW", lambda : [dumpHistory(name, self.history), exit()])
        self.master.mainloop()  

    def toggleStats(self):
        self.showStats = not self.showStats

    def toggleDisplay(self):
        self.simpleImages = not self.simpleImages

        if self.simpleImages:
            self.rockImage = loadImage("rock.gif")
            self.paperImage = loadImage("paper.gif")
            self.scissorsImage = loadImage("scissors.gif")
        else:
            self.rockImage = loadImage("rock_real.gif")
            #self.paperImage = loadImage("paper_real.gif")
            self.scissorsImage = loadImage("scissors_real.gif")

        self.rockButton = Button(self.root, image=self.rockImage, text="Rock", bg=BACKGROUND, command=lambda : self.play("rock"))
        self.rockButton.grid(row = 0, column = 0)
        self.rockButton.image = self.rockImage
        
        #self.paperButton = Button(self.root, image=self.paperImage, text="Paper", bg=BACKGROUND, command=lambda : self.play("paper"))
        #self.paperButton.grid(row = 0, column = 1)
        #self.paperButton.image = self.paperImage

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
        self.root.withdraw()
        popup = getName(root)
        self.root.wait_window(popup.top)
        self.root.deiconify()

    def play(self, playerMove):
        computerMove = calculateMove(name, self.history)    #Call function for the computer to make it's move

        self.history.append(queryNum(playerMove))        #Adds to history AFTER computer makes it's move

        gameData[0] += 1
        if playerMove == computerMove:
            gameData[1] += 1    #Draw
            msg = "Draw!"
            self.filler["background"] = YELLOW
            self.root.configure(background=YELLOW)        
        elif beats(playerMove) != computerMove:
            gameData[2] += 1    #Win
            msg = "You win!"
            self.filler["background"] = GREEN
            self.root.configure(background=GREEN)
        else:
            gameData[3] += 1    #Lose
            msg = "You lose..."
            self.filler["background"] = RED
            self.root.configure(background=RED)

        if playerMove == "rock":
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

        self.updateInfo(f"You play {playerMove}, the computer plays {computerMove}. {msg}", f"You have won {round(gameData[2] / gameData[0] * 100, 2)}% of games | You have lost {round(gameData[3] / gameData[0] * 100, 2)}% of games | You have drawn {round(gameData[1] / gameData[0] * 100, 2)}% of games | You have played {gameData[0]} games")

    def updateInfo(self, *lines):
        self.line1.destroy()
        self.line2.destroy()

        self.line1 = Label(self.master, text=lines[0], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line1.pack()

        self.line2 = Label(self.master, text=lines[1], font=("Courier", FONTSIZE), bg=BACKGROUND)
        self.line2.pack()

if __name__ == "__main__":
    #Var setup
    RGB = lambda red, green, blue: "#%02x%02x%02x" % (red, green, blue)   #RGB to hex
    WHITE = RGB(255, 255, 255)
    RED = RGB(255, 0, 0)
    YELLOW = RGB(255, 255, 0)
    GREEN = RGB(46, 204, 64)
    BACKGROUND = WHITE
    HEIGHT = 431
    WIDTH = 610
    TITLE = "Rock-Paper-Scissors"
    FONTSIZE = 12
    #name = "guest"
    name = "nigel"
    gameData = [0, 0, 0, 0] #Stores: [total games, draws, wins, loses]

    root = Tk()
    app = Window(root)

    #root.withdraw()
    #popup = getName(root)
    #root.wait_window(popup.top)
    #root.deiconify()

    root.mainloop()  