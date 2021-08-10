#Main program

from setup import setup
from sidebar import sidebar
from tkinter import Tk, LEFT, Frame


root = Tk()
root.title("Dashboard")
root.geometry="600x500"
root.resizable(False, False)

button_area=Frame(root)
button_area.pack(side=LEFT, fill="y")
button_area.pack_propagate(False)

setup(button_area)
sidebar(root, button_area)

root.mainloop()