#Manages blueprints

from errors import unknown_button_type, incorrect_argument
from tkinter import Button as Bt
from tkinter import Label as Lb
from tkinter import PhotoImage as PI
from PIL import ImageTk, Image
from requests import get
from steam import get_icon, open_game
from functools import partial
from app import add_app
from exe import open_exe, exe_image

def load(bp, root):
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
                        img=Lb(root, image=photo)
                        img.image=photo
                        but=Bt(root, text=butinfo[1], command=partial(open_game, gameid=int(butinfo[2])))
                        add_app(int(x), int(y), img, but)
                    else:
                        incorrect_argument(f"In button {butinfo[1]}:\nPosition and game id must be integers")
                else:
                    incorrect_argument(f"In button {butinfo[1]}:\nSteam button must have 3 arguments")
            elif butinfo[0]=="exe":
                if len(butinfo)>=4:
                    if x.isdigit() and y.isdigit() and butinfo[2].endswith(".exe"):
                        photo=exe_image(butinfo[3])
                        img=Lb(root, image=photo)
                        img.image=photo
                        if not butinfo[4]=="NONE":
                            options=butinfo[4].split(",")
                        else:
                            options=[]
                        but=Bt(root, text=butinfo[1], command=partial(open_exe, butinfo[2], options))
                        add_app(int(x), int(y), img, but)
                    else:
                        incorrect_argument(f"In button {butinfo[1]}:\nPosition and must be integer and path must be exe")
                else:
                    incorrect_argument(f"In button {butinfo[1]}:\nExe button must have 4 or more arguments")
            else:
                unknown_button_type(f"In button {butinfo[1]}:\nButton type must be steam or exe, not {butinfo[0]}")