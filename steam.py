#Handles steam apps

from requests import get
from PIL import Image, ImageTk
import tkinter
from webbrowser import open as openurl


def get_icon(gameid:int):
    img = Image.open(get(f"https://steamcdn-a.akamaihd.net/steam/apps/{str(gameid)}/header.jpg", stream=True).raw)
    img = img.resize((100,round(img.size[1]*(100/img.size[0]))))
    img = ImageTk.PhotoImage(img)
    return img

def open_game(gameid:int):
    openurl(f"steam://rungameid/{str(gameid)}")

def create_file(gamename:str, gameid:int):
    with open(f"buttons\\{gamename}.txt", "w") as f:
        f.write(f"steam--{gamename}--{str(gameid)}")