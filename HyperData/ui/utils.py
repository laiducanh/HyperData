from PySide6.QtGui import QIcon
from config.settings import config, logger

import os, darkdetect, sys

def icon(fileName:str) -> QIcon:
    
    if isDark():
        return QIcon(os.path.join(get_path(),"ui","icons","white",fileName))
    return QIcon(os.path.join(get_path(),"ui","icons","black",fileName))

def isDark() -> bool:
    if config["theme"] == "Dark":
        return True
    elif config["theme"] == "Light":
        return False
    else: 
        # if theme is AUTO
        # then theme is determined by system
        return darkdetect.isDark()

def get_path():
    try:
        return os.path.join(os.getcwd(), sys._MEIPASS)
    except Exception as e:
        logger.error(e)
        return os.getcwd()
        