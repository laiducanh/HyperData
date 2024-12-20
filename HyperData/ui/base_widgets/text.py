from PySide6.QtWidgets import QLabel

class BodyLabel (QLabel):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)
        if text: self.setText(text)

class InfoLabel (QLabel):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)
        if text: self.setText(text)

class TitleLabel (QLabel):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)
        if text: self.setText(text)
     