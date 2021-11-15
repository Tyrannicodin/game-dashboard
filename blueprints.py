#Manages blueprints

from errors import unknown_button_type, incorrect_argument
from tkinter import Button as Bt
from tkinter import Label as Lb
from steam import get_icon, open_game
from functools import partial
from app import add_app
from exe import open_exe, exe_image
from os import remove


def load(bp, root):
    for widget in root.winfo_children():
        try:
            save=widget.name=="BACKGROUND"
        except:
            save=False
        if not save:
            widget.destroy()
    for button in bp:
        pos,name = button.split("--")
        name=name.rstrip()
        x,y=pos.split(",")
        with open("buttons\\"+name+".txt", "r") as f:
            butinfo=f.readlines()[0].split("--")
            if butinfo[0]=="steam":
                if len(butinfo)==3:
                    if x.isdigit() and y.isdigit() and butinfo[2].isdigit():
                        photo=get_icon(int(butinfo[2]))
                        but=Bt(root, text=butinfo[1], command=partial(open_game, gameid=int(butinfo[2])), image=photo, compound="top")
                        but.image=photo
                        but.grid(column=int(x)-1, row=int(y)-1)
                    else:
                        incorrect_argument(f"In button {butinfo[1]}:\nPosition and game id must be integers")
                else:
                    incorrect_argument(f"In button {butinfo[1]}:\nSteam button must have 3 arguments")
            elif butinfo[0]=="exe":
                if len(butinfo)>=4:
                    if x.isdigit() and y.isdigit() and butinfo[2].endswith(".exe"):
                        photo=exe_image(butinfo[3])
                        if not butinfo[4]=="NONE":
                            options=butinfo[4].split(",")
                        else:
                            options=[]
                        but=Bt(root, text=butinfo[1], command=partial(open_exe, butinfo[2], options), image=photo, compound="top")
                        but.image=photo
                        but.grid(column=int(x)-1, row=int(y)-1)
                    else:
                        incorrect_argument(f"In button {butinfo[1]}:\nPosition and must be integer and path must be exe")
                else:
                    incorrect_argument(f"In button {butinfo[1]}:\nExe button must have 4 or more arguments")
            else:
                unknown_button_type(f"In button {butinfo[1]}:\nButton type must be steam or exe, not {butinfo[0]}")

def blueprint_file(tdlist, name, destroy):
    bpname=name.get()
    name=f"blueprints\\{bpname}.txt"
    open(name, "w").close()
    rows=1
    for row in tdlist:
        columns=1
        for column in row:
            if not column.get()=="None":
                print(column.get())
                with open(name, "a") as f:
                    f.write(f"{columns},{rows}--{column.get()}\n")
            columns+=1
        rows+=1
    destroy.destroy()

def delete_bp(bp, destroy):
    remove(f"blueprints\\{bp.get()}")
    destroy.destroy()