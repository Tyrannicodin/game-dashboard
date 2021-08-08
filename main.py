#Main program

from setup import setup
from sidebar import sidebar
from tkinter import Tk, LEFT, Frame


root = Tk()
root.title="Dashboard"
root.geometry="600x500"

button_area=Frame(root)
button_area.pack(side=LEFT, fill="y")

setup(button_area)
sidebar(root)

root.mainloop()