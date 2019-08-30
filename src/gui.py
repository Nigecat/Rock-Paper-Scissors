from util import *     #Local import from util.py
from game import *     #Local import from game.py
from sys import exit
from tkinter import *

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
        self.init_window()

    def init_window(self):  
        self.root.title(TITLE)
        self.root.configure(background=BACKGROUND)
        self.root.geometry(dimensions(HEIGHT, WIDTH))
        self.root.iconbitmap(r'.\\images\\icon.ico')

        #These are all objects of self so I can referance them in other functions
        self.menubar = Menu(root)  
        self.menubar.add_command(label="Toggle Display Mode", command=self.toggleDisplay)  
        self.menubar.add_command(label="Logout", command=self.logout)  
        self.root.config(menu=self.menubar)  
    
        self.rockButton = Button(root, image=rockImage, text="Rock", bg=BACKGROUND, command=lambda : self.play("rock"))
        self.rockButton.grid(row = 0, column = 0)
        self.rockButton.image = rockImage
        
        self.paperButton = Button(root, image=paperImage, text="Paper", bg=BACKGROUND, command=lambda : self.play("paper"))
        self.paperButton.grid(row = 0, column = 1)
        self.paperButton.image = paperImage

        self.scissorsButton = Button(root, image=scissorsImage, text="Scissors", bg=BACKGROUND, command=lambda : self.play("scissors"))
        self.scissorsButton.grid(row = 0, column = 2)
        self.scissorsButton.image = scissorsImage


        self.playerButton = Button(root, image=blankImage, text=" ", bg=BACKGROUND)
        self.playerButton.grid(row = 1, column = 0)
        self.playerButton.image = blankImage

        self.filler = Label(root, text="    vs    ", bg=BACKGROUND, font=("Courier", 20))
        self.filler.grid(row = 1, column = 1)

        self.computerButton = Button(root, image=blankImage, text=" ", bg=BACKGROUND)
        self.computerButton.grid(row = 1, column = 2)
        self.computerButton.image = blankImage

        self.infoText = Label(root, text="UNDEFINED", bg=BACKGROUND)
        self.infoText.grid(row = 2, column = 1)


    def toggleDisplay(self):
        pass

    def logout(self):
        self.root.withdraw()
        popup = getName(root)
        self.root.wait_window(popup.top)
        self.root.deiconify()

    def play(self, playerMove):
        global history
        computerMove = calculateMove(name, history)
        history.append(queryNum(playerMove))

        gameData[0] += 1
        if playerMove == computerMove:
            gameData[1] += 1    #Draw
            msg = "Draw!"
        elif beats(playerMove) != computerMove:
            gameData[2] += 1    #Win
            msg = "You Win!"
        else:
            gameData[3] += 1    #Lose
            msg = "You lose..."

        #print(gameData)
        #print(history)
        print(f"You play {playerMove}, the computer plays {computerMove}. {msg}")
        print(f"You have won {round(gameData[2] / gameData[0] * 100, 2)}% of games | You have lost {round(gameData[3] / gameData[0] * 100, 2)}% of games | You have drawn {round(gameData[1] / gameData[0] * 100, 2)}% of games | You have played {gameData[0]} games")
        print()

        if playerMove == "rock":
            self.playerButton["image"] = rockImage
        elif playerMove == "paper":
            self.playerButton["image"] = paperImage
        elif playerMove == "scissors":
            self.playerButton["image"] = scissorsImage

        if computerMove == "rock":
            self.computerButton["image"] = rockImage
        elif computerMove == "paper":
            self.computerButton["image"] = paperImage
        elif computerMove == "scissors":
            self.computerButton["image"] = scissorsImage

        #self.infoText["text"] = f"You have won {gameData[2] / gameData[0] * 100}% of games | You have lost {gameData[3] / gameData[0] * 100}% of games | You have drawn {gameData[1] / gameData[0] * 100}% of games | {gameData[0]} total games"

if __name__ == '__main__':
    #Var setup
    WHITE = RGB(255, 255, 255)
    BACKGROUND = WHITE
    HEIGHT = 460
    WIDTH = 610
    TITLE = "Rock-Paper-Scissors"
    #name = "guest"
    name = "nigel"
    gameData = [0, 0, 0, 0] #Stores (in-order) | total games, draws, wins, loses

    root = Tk()

    blankImage = loadImage("blank.gif")
    rockImage = loadImage("rock.gif")
    paperImage = loadImage("paper.gif")
    scissorsImage = loadImage("scissors.gif")

    app = Window(root)

    #root.withdraw()
    #popup = getName(root)
    #root.wait_window(popup.top)
    #root.deiconify()
    history = loadHistory(name)

    root.protocol("WM_DELETE_WINDOW", lambda : [dumpHistory(name, history), exit()])
    root.mainloop()  