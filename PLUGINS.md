# Plugin creation and use guide
1. [Use](#use)
2. [Creation](#Creation)

# Use of plugins
1. Download the plugin from the author.
2. Put the folder in the plugins directory.
3. To your config.json file, add a new part with the name as the plugin name (exactly as in the folder name). The other values can be whatever you like apart from the last two values which are the x and y, as usual.

# Creation of plugins
1. Create a folder with the following files:
    - meta.json
    - main.py
2. In meta.json, create squiggly brackets and in them create a dictionary-like structure with the following values
    - Name:string
    - Description:string
    - Author:string
    - Major version:integer
    - Minor version:float
    - Width:integer
    - Height:integer
3. In main.py, create a function called main that takes a canvas object and a path string. Your plugin should modify this canvas object.