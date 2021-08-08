#Error handling

from pyautogui import alert


class unknown_button_type:
    def __init__(self, info):
        self.throw(info)

    def throw(self, info):
        throw("Unknown button type", info)

class incorrect_argument:
    def __init__(self, info):
        self.throw(info)

    def throw(self, info):
        throw("Incorrect arguments", info)

def throw(etype, info):
    alert(info, etype)