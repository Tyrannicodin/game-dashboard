#Manage sidebar and sidebar functions

from tkinter import Tk, Label, Button, Entry, OptionMenu, StringVar, RIGHT
from functools import partial


def sidebar(root):
    Button(root, text="Create button", command=create_button).pack(side=RIGHT)

def create_button():
    wm=Tk()
    wm.title="Create button"
    Label(wm, text="Create new button").grid(column=0, row=0)
    Label(wm, text="Button type: ").grid(column=0, row=1)
    variable=StringVar(wm)
    variable.set("steam")
    menu = OptionMenu(wm, variable, "steam", "exe")
    menu.grid(column=1, row=1)
    Button(wm, text="Confirm", command=partial(getinfo, variable, wm)).grid(column=2, row=3)
    while True:
        try:
            wm.update()
        except:
            break

def getinfo(app_type, wm):
    app_type=app_type.get()
    if app_type=="steam":
        for widget in wm.winfo_children():
            widget.destroy()
        Label(wm, text="Enter information").grid(column=0, row=0)
        Label(wm, text="Name: ").grid(column=0, row=1)
        name = Entry(wm)
        name.grid(column=1, row=1)
        Label(wm, text="Game id: ").grid(column=0, row=2)
        gameid = Entry(wm)
        gameid.grid(column=1, row=2)
        Button(wm, text="Confirm", command=partial(create_steam, name, gameid, wm)).grid(column=3, row=4)
    elif app_type=="exe":
        for widget in wm.winfo_children():
            widget.destroy()
    else:
        raise ValueError(f"How did you mess that up??? It can't be {app_type}")

def create_steam(name:str, gameid:str, wm):
    if type(name.get())==str and gameid.get().isdigit():
        with open(f"buttons\\{name.get()}.txt", "w") as f:
            f.write(f"steam--{name.get()}--{gameid.get()}")
        wm.destroy()