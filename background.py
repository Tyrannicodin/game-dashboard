from tkinter import Label, PhotoImage
from os import listdir

def create_background(config, root):
    from sys import path
    path=config["path"].replace("LOCAL", path[0])
    if config["mode"]=="SLIDESHOW":
        images=list(image for image in listdir(path) if image.split(".")[-1]=="png")
        slides=[]
        for image in images:
            slides.append(PhotoImage(file=path+"\\"+image))
        current=0
        try:
            background=Label(root, image=slides[current])
            background.image=slides[current]
            current+=1
        except:
            raise IndexError("Target folder must have one or more images in")
    background.place(x=0, y=0, relwidth=1, relheight=1)
    return background, slides, current