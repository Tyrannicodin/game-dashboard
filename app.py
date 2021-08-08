#Manages apps
from tkinter import Button, Label, Tk

def add_app(x:int, y:int, img:Label, button:Button):
    x-=1
    y-=1
    img.grid(column=x, row=y*2)
    button.grid(column=x, row=y*2+1)
