#Main program

from sidebar import sidebar
from background import create_background
from setup import setup
from blueprints import load

from tkinter import Tk, LEFT, Frame
from time import time
from os import chdir
from sys import path

chdir(path[0])

root = Tk()
root.title("Dashboard")
root.attributes("-fullscreen", True)
stop=False
def quit():
    global stop
    stop=True
root.protocol("WM_DELETE_WINDOW", quit)

config, blueprint = setup()

background, slides, current = create_background(config["Background"], root)
background.name="BACKGROUND"
background.place(x=0, y=0, relheight=1, relwidth=1)
lasttime=time()

load(blueprint, root)

interval=config["Background"]["interval"]

while True:
    if int(lasttime)+interval==int(time()) and config["Background"]["mode"]=="SLIDESHOW":
        print("E")
        lasttime=time()
        if len(slides)-1==current:
            current=0
        background.configure(image=slides[current])
        background.image=slides[current]
        current+=1
    if not stop:
        root.update()
    else:
        break