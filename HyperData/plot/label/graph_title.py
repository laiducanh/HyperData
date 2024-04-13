from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QSizePolicy
from plot.canvas import Canvas
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.line_edit import _TextEdit
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import SpinBox, Slider
from ui.base_widgets.color import ColorDropdown
from plot.label.base import FontStyle
from config.settings import font_lib

class GraphTitle (QScrollArea):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        widget = Frame()
        widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        layout = QVBoxLayout()
        layout.setContentsMargins(10,0,10,15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget.setLayout(layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setValue(1900)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.canvas = canvas
        
        layout.addWidget(TitleLabel("Graph Title"))
        layout.addWidget(SeparateHLine())

        self.title = _TextEdit()
        self.title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.title.setPlaceholderText("Enter the Graph's Title")
        self.title.textChanged.connect(self.set_title)
        self.title.setText(self.get_title())
        self.title.setFixedHeight(100)
        layout.addWidget(self.title)

        layout.addSpacing(10)
        
        font = ComboBox(items=font_lib,text='Font')
        font.button.currentTextChanged.connect(self.set_fontname)
        font.button.setCurrentText(self.get_fontname())
        layout.addWidget(font)

        size = SpinBox(text='font size',min=1,max=100,step=2)
        size.button.valueChanged.connect(self.set_fontsize)
        size.button.setValue(self.get_fontsize())
        layout.addWidget(size)
        
        style = FontStyle(obj=self.obj, canvas=self.canvas)
        layout.addWidget(style)

        color = ColorDropdown(text='font color',color=self.get_color())
        color.button.colorChanged.connect(self.set_color)
        layout.addWidget(color)

        self.backgroundcolor = ColorDropdown(text='background color',color=self.get_backgroundcolor())
        self.backgroundcolor.button.colorChanged.connect(self.set_backgroundcolor)
        layout.addWidget(self.backgroundcolor)

        edgecolor = ColorDropdown(text='edge color',color=self.get_edgecolor())
        edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(edgecolor)

        # #align = FontAlignment(type='graph')
        # #align.sig.connect(lambda: self.sig.emit())
        # #layout.addWidget(align)
        
        # #pad = DoubleSpinBox(text='label pad',min=-100,max=100,step=5)
        # #pad.button.valueChanged.connect(lambda: self.sig.emit())
        # #layout.addWidget(pad)

        alpha = Slider(text='transparency')
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)

        # #self.layout.addStretch()

    def set_title (self):
        self.obj = self.canvas.axes.set_title(label=self.title.toPlainText())   
        self.canvas.draw()
    
    def get_title(self):
        return self.canvas.axes.get_title()

    def set_fontname (self, font:str):
        self.obj.set_fontname(font.lower())
        self.canvas.draw()
    
    def get_fontname(self):
        return self.obj.get_fontname().title()

    def set_fontsize(self, value):
        self.obj.set_fontsize(value)
        self.canvas.draw()
    
    def get_fontsize(self):
        return int(self.obj.get_fontsize())

    def set_color (self, color):
        self.obj.set_color(color)
        self.canvas.draw()
    
    def get_color (self):
        return self.obj.get_color()

    def set_backgroundcolor (self, color):
        self.obj.set_backgroundcolor(color)
        self.canvas.draw()
    
    def get_backgroundcolor(self):
        if self.obj.get_bbox_patch() != None:
            return self.obj.get_bbox_patch().get_facecolor()
        return 'white'

    def set_edgecolor (self, color):
        self.obj.set_bbox({"edgecolor":color,
                           "facecolor":self.backgroundcolor.button.color.name()})
        self.canvas.draw()
    
    def get_edgecolor(self):
        if self.obj.get_bbox_patch() != None:
            return self.obj.get_bbox_patch().get_edgecolor()
        return 'white'

    def set_pad (self, value):
        pass

    def get_pad (self):
        pass

    def set_alpha (self, value):
        self.obj.set_alpha(value/100)
        self.canvas.draw()
    
    def get_alpha (self):
        if self.obj.get_alpha() != None:
            return int(self.obj.get_alpha()*100)
        return 100