#First time setup and config parsing

from os import mkdir, listdir
from yaml import safe_load

def setup():
    buttons, blueprints, playlists, config = [False, False, True, False]
    for fil in listdir():
        if fil=="buttons":
            buttons=True
        elif fil=="blueprints":
            blueprints=True
        elif fil=="playlists":
            playlists=True
        elif fil=="config.config":
            config=True
    if not buttons:
        mkdir("buttons")
    if not blueprints:
        mkdir("blueprints")
    if not playlists:
        mkdir("playlists")
    if not config:
        create_config()
    with open("blueprints\\last.txt", "a") as f:
        pass
    with open("config.yml", "r") as f:
        config=safe_load(f)
    last=config["Blueprints"]["default"]
    with open(f"blueprints\\{last}.txt", "r") as f:
        return config, f.readlines()

def create_config():
    with open("config.yml", "w") as f:
        f.write("""Background:
  path: LOCAL\images
  mode: SLIDESHOW
  #Only required if static image, otherwise all .png files from the folder are taken
  interval: 60
  Location: background.png
Blueprints:
  default: last""")