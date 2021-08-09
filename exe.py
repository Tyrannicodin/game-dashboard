#Handles exe files

from os import system, _exit
from errors import unknown_path
from PIL import Image, ImageTk
from subprocess import Popen


def open_exe(mypath, options=[]):
    optionstr=""
    for option in options:
        optionstr+=f" --{option}"
    try:
        Popen(f"\"{mypath}\"{optionstr}")        
    except:
        unknown_path("Executable path not found")

def exe_image(path):
    try:
        img=Image.open(path)
        img = img.resize((100,round(img.size[1]*(100/img.size[0]))))
        img = ImageTk.PhotoImage(img)
        return img
    except:
        unknown_path("Image path not found")