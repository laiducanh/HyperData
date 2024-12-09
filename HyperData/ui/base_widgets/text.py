from PyQt6.QtWidgets import QLabel

class BodyLabel (QLabel):
    def __init__(self, text:str=None, parent=None):
        super().__init__(text, parent)

class InfoLabel (QLabel):
    def __init__(self, text:str=None, parent=None):
        super().__init__(text, parent)

class TitleLabel (QLabel):
    def __init__(self, text:str=None, parent=None):
        super().__init__(text, parent)
     