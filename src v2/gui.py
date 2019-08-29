from util import *     #Local import from util.py
from game import *     #Local import from game.py
from tkinter import *

class getName:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Name:").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        global name
        name = self.e.get().lower().strip()
        if name == "":
            name = "guest"
        self.top.destroy()


class Window(Frame):
    def __init__(self, root = None):
        Frame.__init__(self, root)                
        self.root = root
        self.init_window()

    def init_window(self):  
        self.root.title("Rock-Paper-Scissors")
        self.root.configure(background="white")
        self.root.geometry(dimensions(300, 610))

        menubar = Menu(root)  
        menubar.add_command(label="Toggle Display Mode", command=self.toggleDisplay)  
        menubar.add_command(label="Logout", command=self.logout)  
        self.root.config(menu=menubar)  
    
        rockButton = Button(root, image=rockImage, text="Rock", bg='white', command=lambda : self.move("rock"))
        rockButton.grid(row = 0, column = 0)
        rockButton.image = rockImage
        
        paperButton = Button(root, image=paperImage, text="Paper", bg='white', command=lambda : self.move("paper"))
        paperButton.grid(row = 0, column = 1)
        paperButton.image = paperImage

        scissorsButton = Button(root, image=scissorsImage, text="Scissors", bg='white', command=lambda : self.move("scissors"))
        scissorsButton.grid(row = 0, column = 2)
        scissorsButton.image = scissorsImage

    def toggleDisplay(self):
        pass

    def logout(self):
        popup = getName(root)
        root.wait_window(popup.top)

        print(name)

    def move(self, move):
        print(move)


if __name__ == '__main__':
    root = Tk()

    rockImage = loadImage("rock.gif")
    paperImage = loadImage("paper.gif")
    scissorsImage = loadImage("scissors.gif")

    app = Window(root)

    popup = getName(root)
    root.wait_window(popup.top)

    root.mainloop()  

