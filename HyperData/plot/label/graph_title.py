from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QDialog
from plot.canvas import Canvas
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.frame import ScrollArea
from plot.label.base import FontStyle
from config.settings import font_lib
from matplotlib import colors

DEBUG = False

class GraphTitle(QDialog):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Graph Title')
        self.canvas = canvas
        self.obj = self.canvas.axes.set_title(self.get_title())
            
        layout = QVBoxLayout(self)
        scrollarea = ScrollArea()
        layout.addWidget(scrollarea)

        label = HLineEdit(
            label='Label',
            getter=self.get_title,
            setter=self.set_title,
            layout=scrollarea.vlayout
        )
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        font = HTransparentComboBox(
            items = font_lib,
            label  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=scrollarea.vlayout
        )

        size = HTransparentDoubleSpinBox(
            label = 'Font size',
            minimum = 1, maximum = 100, singleStep = 2,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=scrollarea.vlayout
        )
        
        style = FontStyle(
            obj = [self.obj], 
            canvas = self.canvas,
            layout=scrollarea.vlayout
        )

        color = HColorDropdown(
            label  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=scrollarea.vlayout
        )

        # self.backgroundcolor = ColorDropdown(
        #     text  = 'Background color',
        #     getter=self.get_backgroundcolor,
        #     setter=self.set_backgroundcolor,
        #     layout=layout
        # )

        # edgecolor = ColorDropdown(
        #     text  = 'Edge color',
        #     getter=self.get_edgecolor,
        #     setter=self.set_edgecolor,
        #     layout=layout
        # )

        # #align = FontAlignment(type='graph')
        # #align.sig.connect(lambda: self.sig.emit())
        # #layout.addWidget(align)
        
        # #pad = DoubleSpinBox(text='label pad',min=-100,max=100,step=5)
        # #pad.button.valueChanged.connect(lambda: self.sig.emit())
        # #layout.addWidget(pad)

        alpha = HTransparentDoubleSpinBox(
            label = 'Transparency',
            singleStep = 10, minimum = 0, maximum = 100,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=scrollarea.vlayout
        )
    
    def set_title (self, title:str):
        self.canvas.axes.set_title(title) 
        self.canvas.draw_idle()
    
    def get_title(self):
        return self.canvas.axes.get_title()

    def set_fontname (self, font:str):
        self.obj.set_fontname(font.lower())
        self.canvas.draw_idle()
    
    def get_fontname(self):
        return self.obj.get_fontname().title()

    def set_fontsize(self, value):
        self.obj.set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        return self.obj.get_fontsize()

    def set_color (self, color):
        self.obj.set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        return colors.to_hex(self.obj.get_color())

    def set_backgroundcolor (self, color):
        self.obj.set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.obj.get_bbox_patch():
            return colors.to_hex(self.obj.get_bbox_patch().get_facecolor())
        return 'white'

    def set_edgecolor (self, color):
        self.obj.set_bbox(
            {"edgecolor" : color}
        )
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.obj.get_bbox_patch():
            return colors.to_hex(self.obj.get_bbox_patch().get_edgecolor())
        return 'white'

    def set_pad (self, value):
        pass

    def get_pad (self):
        pass

    def set_alpha (self, value):
        self.obj.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.obj.get_alpha():
            return int(self.obj.get_alpha()*100)
        return 100