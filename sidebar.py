#Manage sidebar and sidebar functions

from tkinter import Tk, Label, Button, Entry, OptionMenu, StringVar, RIGHT, Frame
from functools import partial
from os import listdir
from app import delete_file

def sidebar(root):
    frame=Frame(root)
    Button(frame, text="Create button", command=create_button).grid(column=0, row=0)
    Button(frame, text="Delete button", command=delete_button).grid(column=0, row=1)
    frame.pack(side=RIGHT)

def delete_button():
    wm=Tk()
    wm.title="Delete button"
    Label(wm, text="Delete button").grid(column=0, row=0)
    options=listdir("buttons")
    variable=StringVar(wm)
    OptionMenu(wm, variable, *options).grid(column=0, row=1)
    Button(wm, text="confirm", command=partial(delete_file, variable)).grid(column=2, row=2)
    wm.destroy()


def create_button():
    wm=Tk()
    wm.title="Create button"
    Label(wm, text="Create new button").grid(column=0, row=0)
    Label(wm, text="Button type: ").grid(column=0, row=1)
    variable=StringVar(wm)
    variable.set("steam")
    OptionMenu(wm, variable, "steam", "exe").grid(column=1, row=1) 
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
        Label(wm, text="Enter information").grid(column=0, row=0)
        Label(wm, text="Name: ").grid(column=0, row=1)
        name = Entry(wm)
        name.grid(column=1, row=1)
        Label(wm, text="Game path: ").grid(column=0, row=2)
        gameid = Entry(wm)
        gameid.grid(column=1, row=2)
        Label(wm, text="Image path: ").grid(column=0, row=3)
        imgid = Entry(wm)
        imgid.grid(column=1, row=3)
        Label(wm, text="Arguments (optional, separate with ',')").grid(column=0, row=3)
        options=Entry(wm)
        options.insert(0, "NONE")
        options.grid(column=1, row=4)
        Button(wm, text="Confirm", command=partial(create_exe, name, gameid, imgid, options, wm)).grid(column=3, row=6)
    else:
        raise ValueError(f"How did you mess that up??? It can't be {app_type}")

def create_steam(name:str, gameid:str, wm):
    if type(name.get())==str and gameid.get().isdigit():
        with open(f"buttons\\{name.get()}.txt", "w") as f:
            f.write(f"steam--{name.get()}--{gameid.get()}")
        wm.destroy()

def create_exe(name, gameid, imgid, options, wm):
    with open(f"buttons\\{name.get()}.txt", "w") as f:
        f.write(f"exe--{name.get()}--{gameid.get()}--{imgid.get()}--{options.get()}")
    wm.destroy()