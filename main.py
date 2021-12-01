# Imports and set directory #
from tkinter import Entry, StringVar, Tk, Canvas, Toplevel, OptionMenu, Button
from os import listdir, chdir, startfile, mkdir
from types import ModuleType
from PIL import Image, ImageFont, ImageDraw
from importlib import import_module
from PIL.ImageTk import PhotoImage
from webbrowser import open as op
from requests import get
from time import time
from sys import path
import json
chdir(path[0])
# Config #
defaultconfig={
    "Background":{
        "path":"LOCAL",
        "mode":"SLIDESHOW",
        "interval":60,
        "Location":"background.png"
    },
    "Icons":{
        "font":"arial.pil",
        "icons":[]
    }
}
if "config.json" in listdir():
    with open("config.json", "r") as f:
        config=json.load(f)
else:
    with open("config.json", "w") as f:
        json.dump(defaultconfig, f, sort_keys=True, indent=2)
    config=defaultconfig
# Main window setup #
main = Tk()
main.title("Desktop")
main.attributes("-fullscreen", True)
stop=False
def quit():
    global stop
    stop=True
main.protocol("WM_DELETE_WINDOW", quit)
maincanv=Canvas(main)
maincanv.pack(fill="both")
main.update()
maincanv.config(height=main.winfo_height(), highlightthickness=0)
# Background setup #
lasttime=time()
path=config["Background"]["path"].replace("LOCAL", path[0])
if config["Background"]["mode"]=="SLIDESHOW":
    images=[image for image in listdir(path) if image.split(".")[-1]=="png"]
    slides=[]
    for image in images:
        slides.append(PhotoImage(Image.open(path+"\\"+image)))
    interval=config["Background"]["interval"]
    current=0
    try:
        bgId=maincanv.create_image(0, 0, image=slides[current], anchor="nw")
        current+=1
    except:
        raise IndexError("Target folder must have one or more images in")
# PLUGINS SETUP #
try:
    listdir("plugins")
except:
    mkdir("plugins")
def get_plugin(plugin_folder):
    if plugin_folder in listdir("plugins"):
        try:
            with open(f"plugins\\{plugin_folder}\\meta.json", "r") as f:
                plugin_meta=json.load(f)
                canvas = Canvas(maincanv, width=plugin_meta["Width"]*100, height=plugin_meta["Height"]*115)
                module=import_module(f"plugins.{plugin_folder}.main")
                module.main(canvas, f"plugins\\{plugin_folder}")
                return canvas
        except OSError:
            pass
    else:
        pass
# Add Icons #
def ret_command(icon:list):
    if icon[2].isdigit():
        gameid=icon[2]
        return lambda ignore : op(f"steam://rungameid/{gameid}")
    elif icon[2].endswith(".exe"):
        launchstr=icon[2]
        exec_string=f'"{launchstr}"'
        try:
            for part in icon[5:]:
                exec_string+=f" --{part}"
            return lambda ignore : startfile(exec_string)
        except IndexError:
            return lambda ignore : startfile(exec_string)
    else:
        iconname=icon[0]
        raise ValueError(f"Error in {iconname}\n Icon's third value must be steam game id or end with '.exe'")
icons=[]
def reload_icons():
    global icons
    for icon in icons:
        maincanv.delete(icon)
    icons=[]
    for icon in config["Icons"]["icons"]:
        if len(icon)>=5:
            if not icon[1]=="PLUGIN":
                if icon[1]=="STEAM":
                    gameid=icon[2]
                    img=Image.open(get(f"https://steamcdn-a.akamaihd.net/steam/apps/{gameid}/header.jpg", stream=True).raw)
                elif icon[1].endswith(".png"):
                    img=Image.open(icon[1])
                else:
                    iconname=icon[0]
                    raise ValueError(f"Error in {iconname}\n Icon's second value must be 'STEAM' or end with '.png'")
                img=img.resize((100, 100))
                img=img.convert("RGBA")
                font = ImageFont.truetype(config["Icons"]["font"], 15)
                fsize=font.getsize(icon[0])
                text=Image.new("RGBA", (fsize[0], 15), (0, 0, 0, 0))
                textdraw=ImageDraw.Draw(text)
                textdraw.text((0, 0), icon[0], font=font)
                bg=Image.new("RGBA", (100, 100+text.size[1]), (0, 0, 0, 0))
                bg.paste(img, (0, 0), img)
                bg.paste(text, (round((bg.size[0]/2)-(text.size[0]/2)), 100), text)
                bgTk = PhotoImage(bg)
                canvBut=maincanv.create_image(icon[3]*100, icon[4]*115, image=bgTk, anchor="nw")
                icons.append([bgTk, canvBut])
                maincanv.tag_bind(canvBut, "<Button-1>", ret_command(icon))
            else:
                get_plugin(icon[0]).place(x=icon[3]*100, y=icon[4]*115, anchor="nw")
reload_icons()
# Settings button #
settings_open=False
settings=Toplevel(main)
settings.title("Settings")
settings.geometry("200x200-0+0")
settings.withdraw()
def settings_quit():
    toggle_settings("")
settings.protocol("WM_DELETE_WINDOW", settings_quit)
def toggle_settings(event):
    global settings_open
    global settings
    if not settings_open:
        settings_open=True
        settings.deiconify()
    else:
        settings_open=False
        settings.withdraw()
cog=Image.open("cog.png")
cog=cog.resize((50, 50))
cogTk=PhotoImage(cog)
icons.append(cogTk)
setbut=maincanv.create_image(main.winfo_width(), 0, image=cogTk, anchor="ne")
maincanv.tag_bind(setbut, "<Button-1>", toggle_settings)
# BUTTON CREATION HANDLER #
def create_button(settings):
    button=Toplevel(settings)
    name=Entry(button)
    name.insert(0, "Button name")
    image=Entry(button)
    image.insert(0, "Image path (Use \"STEAM\" to use default image)")
    file=Entry(button)
    file.insert(0, "File path (Enter steam id for steam game)")
    x=Entry(button)
    x.insert(0, "X location")
    y=Entry(button)
    y.insert(0, "Y location")
    complete=Button(button, command=lambda : check(name, image, file, x, y), text="Create button")
    name.pack(side="top", fill="x")
    image.pack(side="top", fill="x")
    file.pack(side="top", fill="x")
    x.pack(side="top", fill="x")
    y.pack(side="top", fill="x")
    complete.pack(side="top", fill="x")
def check(name, image, file, x, y):
    name=str(name.get())
    image=str(image.get())
    file=str(file.get())
    x=str(x.get())
    y=str(y.get())
    if x.isdigit() and y.isdigit():
        if file.endswith(".exe") or file.isdigit() or file=="PLUGIN":
            if image.endswith("png") or image=="STEAM" or image=="PLUGIN":
                with open("config.json", "r") as f:
                    icons=json.load(f)["Icons"]["icons"]
                    icons.append([name, image, file, int(x), int(y)])
                    config["Icons"]["icons"]=icons
                with open("config.json", "w") as f:
                    json.dump(config, f, sort_keys=True, indent=2)
                reload_icons()
button_creator=Button(settings, text="Create button", command=lambda : create_button(settings))
button_creator.pack(side="top", fill="x")
# BUTTON DELETION HANDLER #
def delete_button(settings):
    button=Toplevel(settings)
    button_ans=StringVar(button)
    with open("config.json", "r") as f:
        buttons=json.load(f)["Icons"]["icons"]
        button_selector=OptionMenu(button, button_ans, *[bpart[0] for bpart in buttons])
    confirm=Button(button, text="Delete button", command=lambda : delete_check(button_ans))
    button_selector.pack(side="top", fill="x")
    confirm.pack(side="top", fill="x")
def delete_check(button_name):
    button_name=button_name.get()
    with open("config.json", "r") as f:
        icons=json.load(f)["Icons"]["icons"]
    icons.pop(icons.index([icon for icon in icons if icon[0]==button_name][0]))
    config["Icons"]["icons"]=icons
    with open("config.json", "w") as f:
        json.dump(config, f)
    reload_icons()
button_deletor=Button(settings, text="Delete button", command=lambda : delete_button(settings))
button_deletor.pack(side="top", fill="x")
# Main loop #
while True:
    if int(lasttime)+interval==int(time()) and config["Background"]["mode"]=="SLIDESHOW":
        lasttime=time()
        if len(slides)-1==current:
            current=0
        maincanv.itemconfig(bgId, image=slides[current])
        current+=1
    if not stop:
        main.update()
    else:
        break