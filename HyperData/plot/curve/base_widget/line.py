from PyQt6.QtWidgets import QVBoxLayout, QWidget
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, Slider
from ui.base_widgets.color import ColorPicker
from config.settings import linestyle_lib
from plot.canvas import Canvas
from matplotlib.lines import Line2D

class LineBase (QWidget):
    def __init__(self, gid:str, canvas:Canvas):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        #self.setStyleSheet('LineBase {background-color:white}')
        layout.setContentsMargins(0,0,0,0)   

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()        
        
        style = ComboBox(text='line style',items=linestyle_lib.values())
        style.button.currentTextChanged.connect(self.set_linestyle)
        style.button.setCurrentText(self.get_linestyle())
        layout.addWidget(style)

        width = DoubleSpinBox(text='line width',min=0,max=10,step=0.5)
        width.button.setValue(self.get_linewidth())
        width.button.valueChanged.connect(self.set_linewidth)
        layout.addWidget(width)

        color = ColorPicker(title='line color',text='color')
        color.button.colorChanged.connect(self.set_color)
        color.button.setColor(self.get_color())
        layout.addWidget(color)

        alpha = Slider(text='Transparency',min=0,max=100)
        alpha.button.setValue(self.get_alpha())
        alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(alpha)
    
    def find_object (self) -> Line2D:
        for obj in self.canvas.fig.findobj(match=Line2D):
            if obj._gid != None and obj._gid == self.gid:
                return obj

    def set_linestyle(self, value):
        self.obj.set_linestyle(value.lower())
        self.canvas.draw()
    
    def get_linestyle(self):
        return self.obj.get_linestyle().title()
    
    def set_linewidth(self, value):
        self.obj.set_linewidth(value)
        self.canvas.draw()
    
    def get_linewidth (self):
        return self.obj.get_linewidth()
    
    def set_alpha(self, value):
        self.obj.set_alpha(float(value/100))
        self.canvas.draw()
    
    def get_alpha (self):
        if self.obj.get_alpha() == None:
            return 100
        return float(self.obj.get_alpha()*100)

    def set_color(self, color):
        self.obj.set_color(color.name())
        self.canvas.draw()
    
    def get_color(self):
        return self.obj.get_color()
    
    def valueChange(self):
        pass