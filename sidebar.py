#Manage sidebar and sidebar functions

from tkinter import Tk, Label, Button, Entry, OptionMenu, StringVar, RIGHT, Frame
from functools import partial
from os import listdir
from app import delete_file
from blueprints import load, blueprint_file, delete_bp


def sidebar(root, home):
    frame=Frame(root)
    frame.pack_propagate(False)
    Button(frame, text="Create button", command=create_button).grid(column=0, row=0)
    Button(frame, text="Delete button", command=delete_button).grid(column=0, row=1)
    Label(frame).grid(column=0, row=2)
    Button(frame, text="Create blueprint", command=create_blueprint).grid(column=0, row=3)
    Button(frame, text="Load blueprint", command=partial(ask_load, home)).grid(column=0, row=4)
    Button(frame, text="Edit blueprint", command=ask_edit).grid(column=0, row=5)
    frame.pack(side=RIGHT)

def delete_button():
    wm=Tk()
    wm.title("Delete button")
    Label(wm, text="Delete button").grid(column=0, row=0)
    options=listdir("buttons")
    variable=StringVar(wm)
    OptionMenu(wm, variable, *options).grid(column=0, row=1)
    Button(wm, text="confirm", command=partial(delete_file, variable, wm)).grid(column=2, row=2)
    wm.mainloop()


def create_button():
    wm=Tk()
    wm.title("Create button")
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

def ask_load(home):
    wm = Tk()
    wm.title("Load/Reload blueprints")
    options=[]
    for filee in listdir("blueprints"):
        options.append(filee.split(".")[0])
    Label(wm, text="Select blueprint").grid(column=0, row=0)
    variable=StringVar(wm)
    variable.set("last")
    OptionMenu(wm, variable, *options).grid(column=1, row=0)
    Button(wm, text="Load blueprint", command=partial(reloadscreen, variable, home, wm)).grid(column=2, row=2)
    wm.mainloop()

def reloadscreen(variable, home, destroy):
    with open(f"blueprints\\{variable.get()}.txt", "r") as f:
        load(f.readlines(), home)
    destroy.destroy()

def create_blueprint():
    wm = Tk()
    wm.title("Create new blueprint")
    options=["None"]
    for option in listdir("buttons"):
        options.append(option.split(".")[0])
    Label(wm, text="Select position for button").grid(column=0, columnspan=10, row=0)
    maxx,y=[10,5]
    variables=[]
    for i in range(y):
        x=0
        rowlist=[]
        while x<maxx:
            variable=StringVar(wm)
            variable.set("None")
            OptionMenu(wm, variable, *options).grid(row=i+1, column=x)
            rowlist.append(variable)
            x+=1
        variables.append(rowlist)
    Label(wm, text="Select name").grid(row=i+2, column=x-1)
    name=Entry(wm)
    name.grid(row=i+2, column=x)
    Button(wm, text="Create blueprint", command=partial(blueprint_file, variables, name, wm)).grid(row=i+3, column=x)
    wm.mainloop()

def ask_edit():
    wm = Tk()
    wm.title("Edit blueprints")
    options=[]
    for filee in listdir("blueprints"):
        options.append(filee.split(".")[0])
    Label(wm, text="Select blueprint").grid(column=0, row=0)
    variable=StringVar(wm)
    variable.set("last")
    OptionMenu(wm, variable, *options).grid(column=1, row=0)
    Button(wm, text="Edit blueprint", command=partial(file_blueprint, variable, wm)).grid(column=2, row=2)
    wm.mainloop()

def file_blueprint(name, destroy):
    name=name.get()
    filename=f"blueprints\\{name}.txt"
    result=[]
    for a in range(5):
        d2=[]
        for b in range(10):
            d2.append("None")
        result.append(d2)
    with open(filename, "r") as f:
        for line in f.readlines():
            coords=line.split("--")[0].split(",")
            coords[0],coords[1]=int(coords[0])-1,int(coords[1])-1
            result[coords[1]][coords[0]]=line.split("--")[1]
    destroy.destroy()
    load_blueprint_editor(result, name)

def load_blueprint_editor(lists, bpname):
    wm = Tk()
    wm.title("Edit blueprint")
    options=["None"]
    for option in listdir("buttons"):
        options.append(option.split(".")[0])
    Label(wm, text="Select position for button").grid(column=0, columnspan=10, row=0)
    variables=[]
    i=0
    for listed in lists:
        rowlst=[]
        j=0
        for item in listed:
            variable=StringVar(wm)
            variable.set(item)
            OptionMenu(wm, variable, *options).grid(row=i+1, column=j)
            rowlst.append(variable)
            j+=1
        i+=1
        variables.append(rowlst)
    Label(wm, text="Select name").grid(row=i+2, column=j-1)
    name=Entry(wm)
    name.insert(0, bpname)
    name.grid(row=i+2, column=j)
    Button(wm, text="Confirm edit", command=partial(blueprint_file, variables, name, wm)).grid(row=i+3, column=j)
    wm.mainloop()

def delete_blueprint():
    wm=Tk()
    wm.title("Delete button")
    Label(wm, text="Delete button").grid(column=0, row=0)
    options=listdir("buttons")
    variable=StringVar(wm)
    OptionMenu(wm, variable, *options).grid(column=0, row=1)
    Button(wm, text="confirm", command=partial(delete_bp, variable, wm)).grid(column=2, row=2)
    wm.mainloop()