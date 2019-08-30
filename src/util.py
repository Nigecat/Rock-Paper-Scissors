from tkinter import PhotoImage

def loadImage(file):
    return PhotoImage(file=".\\images\\{}".format(file))

def dimensions(HEIGHT, WIDTH):
    '''Function to return window dimensions formatted how tkinter requires

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