from tkinter import *

def loadImage(file):
    return PhotoImage(file=".\\images\\{}".format(file))

#def imageButton(root, **kwargs):
#    row = kwargs["row"]
#    column = kwargs["column"]
#    del kwargs["row"]
#    del kwargs["column"]
#    button = Button(root, kwargs)
#    button.grid(row = row, column = column)
#    button.image = kwargs["image"]

def dimensions(HEIGHT, WIDTH):
    '''Function to return window dimensions how tkinter wants it, takes height by width

    HEIGHT -- window height
    WIDTH -- window width
    '''
    return "{}x{}".format(WIDTH, HEIGHT)

def RGB(red, green, blue):
    """Given integer values of Red, Green, Blue, return a color string "#RRGGBB"

    red -- Red portion from 0 to 255
    green -- Green portion from 0 to 255
    blue -- Blue portion from 0 to 255
    return: A single RGB String in the format "#RRGGBB" where each pair is a hex number.
    """
    return '#%02x%02x%02x' % (red, green, blue)