from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QSizePolicy, QWidget, QStackedLayout
from plot.canvas import Canvas
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.line_edit import _TextEdit
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.base_widgets.button import ComboBox, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox, Slider
from ui.base_widgets.color import ColorDropdown
from plot.utilis import find_mpl_object
from plot.label.base import FontStyle
from config.settings import font_lib
from matplotlib.axis import XAxis, YAxis
from matplotlib.text import Text

class AxesLabelBase (QScrollArea):
    def __init__(self, axis, canvas:Canvas, parent=None):
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
        self.axis = axis
        self.ax = self.find_axis()

        self.title = _TextEdit()
        self.title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.title.setPlaceholderText(f"Enter the {axis} axis' label")
        self.title.textChanged.connect(self.set_label)
        self.title.setText(self.get_title())
        self.title.setFixedHeight(100)
        layout.addWidget(self.title)

        layout.addSpacing(10)

        font = ComboBox(items=font_lib,text='Font')
        font.button.currentTextChanged.connect(self.set_fontname)
        font.button.setCurrentText(self.get_fontname())
        layout.addWidget(font)

        size = DoubleSpinBox(text='font size',min=1,max=100,step=1)
        size.button.valueChanged.connect(self.set_fontsize)
        size.button.setValue(self.get_fontsize())
        layout.addWidget(size)

        style = FontStyle(obj=[self.text], canvas=self.canvas)
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

        alpha = Slider(text='transparency')
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)
      
    def find_axis(self) -> XAxis | YAxis:
        return find_mpl_object(self.canvas.fig,[XAxis, YAxis], self.axis)[0]

    def set_label(self):
        self.text: Text = self.ax.set_label_text(label=self.title.toPlainText())
        self.canvas.draw()
    
    def get_title(self) -> str:
        return self.ax.get_label_text()
    
    def set_fontname (self, font:str):
        self.text.set_fontfamily(font)
        self.canvas.draw()
    
    def get_fontname(self):
        return self.text.get_fontname()
    
    def set_fontsize(self, value):
        self.text.set_fontsize(value)
        self.canvas.draw()
    
    def get_fontsize(self):
        return self.text.get_fontsize()
    
    def set_color (self, color):
        self.text.set_color(color)
        self.canvas.draw()
    
    def get_color (self):
        return self.text.get_color()

    def set_backgroundcolor (self, color):
        self.text.set_backgroundcolor(color)
        self.canvas.draw()
    
    def get_backgroundcolor(self):
        if self.text.get_bbox_patch() != None:
            return self.text.get_bbox_patch().get_facecolor()
        return 'white'
    
    def set_edgecolor (self, color):
        self.text.set_bbox({"edgecolor":color,
                           "facecolor":self.backgroundcolor.button.color.name()})
        self.canvas.draw()
    
    def get_edgecolor(self):
        if self.text.get_bbox_patch() != None:
            return self.text.get_bbox_patch().get_edgecolor()
        return 'white'
    
    def set_alpha (self, value):
        self.text.set_alpha(value/100)
        self.canvas.draw()
    
    def get_alpha (self):
        if self.text.get_alpha() != None:
            return int(self.text.get_alpha()*100)
        return 100

class AxesLabel2D (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        choose_axis = SegmentedWidget()
        layout.addWidget(choose_axis)

        choose_axis.addButton(text='Bottom', func=lambda: self.stackedlayout.setCurrentIndex(0))
        choose_axis.addButton(text='Left', func=lambda: self.stackedlayout.setCurrentIndex(1))
        choose_axis.addButton(text='Top', func=lambda: self.stackedlayout.setCurrentIndex(2))
        choose_axis.addButton(text='Right', func=lambda: self.stackedlayout.setCurrentIndex(3))

        choose_axis.setCurrentWidget('Bottom')

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        self.bot = AxesLabelBase('bottom', canvas, parent)
        self.stackedlayout.addWidget(self.bot)
        self.left = AxesLabelBase('left', canvas, parent)
        self.stackedlayout.addWidget(self.left)
        self.top = AxesLabelBase('top', canvas, parent)
        self.stackedlayout.addWidget(self.top)
        self.right = AxesLabelBase('right', canvas, parent)
        self.stackedlayout.addWidget(self.right)