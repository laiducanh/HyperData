import qfluentwidgets
from PyQt6.QtWidgets import QMenu

class Menu (qfluentwidgets.RoundMenu):
    def __init__(self, text:str=None, parent=None):
        super().__init__(title=text, parent=parent)