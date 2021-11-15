#Manages apps

from tkinter import Button
from os import remove


def add_app(x:int, y:int, button:Button):
    x-=1
    y-=1
    button.grid(column=x, row=y)

def delete_file(app_name, destroy):
    app_name=app_name.get()
    remove(f"buttons\\{app_name}")
    destroy.destroy()