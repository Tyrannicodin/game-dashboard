# Imports and set directory #
from tkinter import TclError, Tk, Canvas, Toplevel
from PIL import Image, ImageFont, ImageDraw
from os import listdir, chdir, startfile
from PIL.ImageTk import PhotoImage
from webbrowser import open as op
from yaml import safe_load
from requests import get
from time import time
from sys import path
chdir(path[0])

# Config #
defaultconfig={
    "Background":{
        "path":"LOCAL",
        "mode":"SLIDESHOW",
        "COMMENT":"Only required if slideshow",
        "interval":60,
        "COMMENT":"Only required if static image, otherwise all .png files from the folder are taken",
        "Location":"background.png"
    },
    "Icons":{
        "font":"arial.pil",
        "icons":[]
    }
}
if "config.yml" in listdir():
    with open("config.yml", "r") as f:
        config=safe_load(f)
else:
    with open("config.yml", "w") as f:
        for section in list(defaultconfig.items()):
            f.write(section[0]+":\n")
            if type(section[1])==dict:
                for part in list(section[1].items()):
                    if not part[0]=="COMMENT":
                        f.write("  "+str(part[0])+": "+str(part[1])+"\n")
                    else:
                        f.write("  #"+str(part[1])+"\n")
            elif type(section[1])==list:
                for part in section[1]:
                    f.write("  "+str(part)+"\n")
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
i=1
for icon in config["Icons"]["icons"]:
    if len(icon)>=5:
        i+=1
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
        icons.append(bgTk)
        canvBut=maincanv.create_image(icon[3]*100, icon[4]*115, image=bgTk, anchor="nw")
        maincanv.tag_bind(canvBut, "<Button-1>", ret_command(icon))

# Settings button
settings_open=True
settings=Toplevel(main)
settings.title("Settings")
settings.geometry("200x200-0+0")
def toggle_settings(event):
    global settings_open
    global settings
    if not settings_open:
        settings_open=True
        settings.deiconify()
    else:
        settings_open=False
        try:
            settings.withdraw()
        except TclError:
            settings=Toplevel(main)
            settings.geometry("200x200-0+0")
            settings.title("Settings")
            settings.withdraw()
cog=Image.open("cog.png")
cog=cog.resize((50, 50))
cogTk=PhotoImage(cog)
icons.append(cogTk)
setbut=maincanv.create_image(main.winfo_width(), 0, image=cogTk, anchor="ne")
maincanv.tag_bind(setbut, "<Button-1>", toggle_settings)
toggle_settings("")

# Main loop #
while True:
    if int(lasttime)+interval==int(time()) and config["Background"]["mode"]=="SLIDESHOW":
        lasttime=time()
        if len(slides)-1==current:
            current=0
        maincanv.itemconfig(bgId, image=slides[current])
        current+=1
    if settings_open:
        settings.update()
    if not stop:
        main.update()
    else:
        break