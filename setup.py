#First time setup

from os import mkdir, listdir
from blueprints import load


def setup(root):
    buttons, blueprints, playlists = [False, False, True]
    for fil in listdir():
        if fil=="buttons":
            buttons=True
        elif fil=="blueprints":
            blueprints=True
        elif fil=="playlists":
            playlists=True
    if not buttons:
        mkdir("buttons")
    if not blueprints:
        mkdir("blueprints")
    if not playlists:
        mkdir("playlists")
    with open("blueprints\\last.txt", "a") as f:
        pass
    with open("blueprints\\last.txt", "r") as f:
        load(f.readlines(), root)