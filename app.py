#Manages apps

from tkinter import Button, Label, Tk
from os import remove


def add_app(x:int, y:int, img:Label, button:Button):
    x-=1
    y-=1
    img.grid(column=x, row=y*2)
    button.grid(column=x, row=y*2+1)

def delete_file(app_name, destroy):
    app_name=app_name.get()
    remove(f"buttons\\{app_name}")
    destroy.destroy()