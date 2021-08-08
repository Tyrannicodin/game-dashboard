#Main program

from setup import setup
from sidebar import sidebar
from tkinter import Tk, LEFT, Frame


root = Tk()
root.title="Dashboard"
root.geometry="600x500"

setup(root)

root.mainloop()