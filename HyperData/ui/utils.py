from PyQt6.QtGui import QIcon
from config.settings import config

import os, darkdetect

def icon(fileName:str) -> QIcon:
    if isDark():
        return QIcon(os.path.join("ui","icons","white",fileName))
    return QIcon(os.path.join("ui","icons","black",fileName))

def isDark() -> bool:
    
    if config["theme"] == "Dark":
        return True
    elif config["theme"] == "Light":
        return False
    else: 
        # if theme is AUTO
        # then theme is determined by system
        return darkdetect.isDark()