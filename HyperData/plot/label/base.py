from PyQt6.QtWidgets import QHBoxLayout, QWidget
from ui.base_widgets.button import _ComboBox, _ToggleToolButton
from ui.base_widgets.text import BodyLabel
from matplotlib.text import Text
from plot.canvas import Canvas

class FontStyle (QWidget):
    def __init__(self, obj:Text, canvas: Canvas, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.obj = obj
        self.canvas = canvas
    
        layout.addWidget(BodyLabel('Font Style'))
        style = _ToggleToolButton()
        style.clicked.connect(self.set_italic)
        style.setCheckable(True)
        style.setChecked(self.get_italic())
        style.setIcon("text-italic.svg")
        layout.addWidget(style)
        
        weight = _ToggleToolButton()
        weight.clicked.connect(self.set_bold)
        weight.setCheckable(True)
        weight.setChecked(self.get_bold())
        weight.setIcon("text-bold.svg")
        layout.addWidget(weight)
    
    def set_italic (self, bool):
        if bool: self.obj.set_fontstyle('italic')
        else: self.obj.set_fontstyle('normal')
        self.canvas.draw()
    
    def get_italic (self):
        if self.obj.get_fontstyle() == 'normal':
            return False
        return True

    def set_bold (self, bool):
        if bool: self.obj.set_fontweight('bold')
        else: self.obj.set_fontweight('normal')
        self.canvas.draw()
    
    def get_bold (self):
        if self.obj.get_fontweight() == 'normal':
            return False
        return True

class FontAlignment (QWidget):
    def __init__(self, obj: Text, canvas:Canvas, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.obj = obj
        self.canvas = canvas

        layout.addWidget(BodyLabel('Font Alignment'))
        self.btn = _ComboBox()
        if self.obj.get_rotation() in ['y left','y right']:
            self.btn.addItems(['Bottom','Center','Top'])
        else:
            self.btn.addItems(['Left','Center','Right'])
        layout.addWidget(self.btn)

    