from PySide6.QtWidgets import QVBoxLayout, QWidget, QDialog, QStackedLayout
from ui.base_widgets.button import HTransparentComboBox, HToggle, SegmentedWidget
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.frame import ScrollArea, SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.canvas import Canvas3D
from matplotlib import colors
import numpy as np
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class Margin3D(ScrollArea):
    def __init__(self, canvas:Canvas3D, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        top = HTransparentDoubleSpinBox(
            label  = 'Margin top',
            label2 = "The position of the top edge",
            minimum = 0, maximum = 1, singleStep = 0.05,
            getter=self.get_top,
            setter=self.set_top,
            layout=self.vlayout
        )

        bottom = HTransparentDoubleSpinBox(
            label  = 'Margin bottom',
            label2 = 'The position of the bottom edge',
            minimum = 0, maximum = 1, singleStep = 0.05,
            getter=self.get_bottom,
            setter=self.set_bottom,
            layout=self.vlayout
        )

        left = HTransparentDoubleSpinBox(
            label  = 'Margin left',
            label2 ='The position of the left edge',
            minimum = 0, maximum = 1, singleStep = 0.05,
            setter=self.set_left,
            getter=self.get_left,
            layout=self.vlayout
        )

        right = HTransparentDoubleSpinBox(
            label  = 'Margin right',
            label2 = 'The position of the right edge',
            minimum = 0, maximum = 1, singleStep = 0.05,
            setter=self.set_right,
            getter=self.get_right,
            layout=self.vlayout
        )
    
    def set_top(self,value):
        self.canvas.figure.subplots_adjust(top=value)
        self.canvas.draw_idle()
    
    def get_top(self):
        return self.canvas.figure.subplotpars.top
    
    def set_bottom(self,value):
        self.canvas.figure.subplots_adjust(bottom=value)
        self.canvas.draw_idle()
    
    def get_bottom(self):
        return self.canvas.figure.subplotpars.bottom
    
    def set_left(self,value):
        self.canvas.figure.subplots_adjust(left=value)
        self.canvas.draw_idle()
    
    def get_left(self):
        return self.canvas.figure.subplotpars.left
    
    def set_right(self,value):
        self.canvas.figure.subplots_adjust(right=value)
        self.canvas.draw_idle()
    
    def get_right(self):
        return self.canvas.figure.subplotpars.right
    
class Grid3D(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas3D, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        
        if   axis == 'XY Pane': self.axinfo = self.canvas.axes.zaxis._axinfo['grid']
        elif axis == 'YZ Pane': self.axinfo = self.canvas.axes.xaxis._axinfo['grid']
        elif axis == 'XZ Pane': self.axinfo = self.canvas.axes.yaxis._axinfo['grid']

        self.linewidth = HTransparentDoubleSpinBox(
            label  = 'Line Width',
            label2 = 'Set the width of the grid lines',
            minimum = 0, maximum = 10, singleStep = 1,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=self.vlayout
        )

        self.linestyle = HTransparentComboBox(
            label  = 'Line Style',
            label2 = 'Set the style of the grid lines',
            items = linestyle_lib.values(),
            getter=self.get_linestyle,
            setter=self.set_linestyle,
            layout=self.vlayout
        )

        self.color = HColorDropdown(
            label  = 'Line Color',
            label2 = 'Set the color of the grid',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

    def set_linewidth(self, value:float):
        self.axinfo.update(linewidth = value)
        self.canvas.draw_idle()
    
    def get_linewidth(self) -> float:
        return self.axinfo.get("linewidth")
    
    def set_linestyle(self, value:str):
        self.axinfo.update(linestyle = value)
        self.canvas.draw_idle()

    def get_linestyle (self) -> str:
        return self.axinfo.get('linestyle')

    def set_color(self, color):
        self.axinfo.update(color = color)
        self.canvas.draw_idle()
       
    def get_color(self) -> str:
        return self.axinfo.get('color')


class Pane3D(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas3D, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        if   axis == 'XY Pane': self.axis = self.canvas.axes.zaxis.pane
        elif axis == 'XZ Pane': self.axis = self.canvas.axes.yaxis.pane
        elif axis == 'YZ Pane': self.axis = self.canvas.axes.xaxis.pane

        self.visible = HToggle(
            label  = 'Visible',
            label2 = 'Whether to show the color',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        self.facecolor = HColorDropdown(
            label  = 'Color',
            label2 = 'Set the color of the Pane',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.alpha = HTransparentDoubleSpinBox(
            label  = 'Transparency',
            label2 = 'Set the transparency of the Pane',
            singleStep  = 10, minimum = 0, maximum = 100,
            setter=self.set_patch_alpha,
            getter=self.get_patch_alpha,
            layout=self.vlayout
        )
    
    def set_visible(self, value:bool):
        self.axis.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.axis.get_visible()
    
    def set_color(self, color):
        self.axis.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        return colors.rgb2hex(self.axis.get_facecolor())

    def set_patch_alpha (self, value):
        self.axis.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_patch_alpha (self):
        if self.axis.get_alpha(): return int(self.axis.get_alpha()*100)
        else: return 100


class Axes3D(QDialog):
    def __init__(self, axis:str, canvas:Canvas3D, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"{axis} settings")
        layout = QVBoxLayout(self)

        self.choose_axis = SegmentedWidget()
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='Margins', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Grid', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Pane', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        margin = Margin3D(canvas, parent)
        self.stackedlayout.addWidget(margin)

        grid = Grid3D(axis, canvas, parent)
        self.stackedlayout.addWidget(grid)

        pane = Pane3D(axis, canvas, parent)
        self.stackedlayout.addWidget(pane)

class View3D(QDialog):
    def __init__(self, canvas:Canvas3D, parent=None):
        super().__init__(parent)

        self.canvas = canvas

        layout = QVBoxLayout(self)
        scrollarea = ScrollArea()
        layout.addWidget(scrollarea)

        scrollarea.vlayout.addWidget(TitleLabel('View'))
        scrollarea.vlayout.addWidget(SeparateHLine())

        self.elev = HTransparentDoubleSpinBox(
            minimum=-360, maximum=360, singleStep=10,
            label='Elevation angle',
            getter=lambda: self.canvas.axes.elev,
            setter=self.set_view,
            layout=scrollarea.vlayout
        )

        self.azim = HTransparentDoubleSpinBox(
            minimum=-360, maximum=360, singleStep=10,
            label='Azimuthal angle',
            getter=lambda: self.canvas.axes.azim,
            setter=self.set_view,
            layout=scrollarea.vlayout
        )

        self.roll = HTransparentDoubleSpinBox(
            minimum=-360, maximum=360, singleStep=10,
            label='Roll angle',
            getter=lambda: self.canvas.axes.roll,
            setter=self.set_view,
            layout=scrollarea.vlayout
        )     

        self.vertical_axis = HTransparentComboBox(
            items=["x","y","z"],
            label='Vertical axis',
            label2='Azimuthal angle rotates about this axis',
            setter=self.set_view,
            getter=lambda: ["x","y","z"][self.canvas.axes._vertical_axis],
            layout=scrollarea.vlayout
        )

        scrollarea.vlayout.addWidget(TitleLabel('Projection'))
        scrollarea.vlayout.addWidget(SeparateHLine())

        self.proj_type = HTransparentComboBox(
            items=["persp","ortho"],
            label='Projection type',
            label2='Set the projection type',
            setter=self.set_proj_type,
            getter=self.get_proj_type,
            layout=scrollarea.vlayout
        ) 

        self.focal_length = HTransparentDoubleSpinBox(
            minimum=1, maximum=1000, singleStep=1,
            label='Focal length',
            label2="Focal length of the virtual camera used for a projection type of 'persp'",
            setter=self.set_proj_type,
            getter=self.get_focal_length,
            layout=scrollarea.vlayout
        )
    
    def set_view(self):
        try: 
            self.canvas.axes.view_init(
                elev=self.elev.get_value(), 
                azim=self.azim.get_value(), 
                roll=self.roll.get_value(),
                vertical_axis=self.vertical_axis.get_value()
            )
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def set_proj_type(self):
        try:
            proj_type = self.proj_type.get_value()
            if proj_type == 'persp':
                focal_length = self.focal_length.get_value()
            else: # ortho
                focal_length = None
            self.canvas.axes.set_proj_type(
                proj_type=proj_type,
                focal_length=focal_length
            )
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def get_proj_type(self) -> str:
        if self.canvas.axes._focal_length in (None, np.inf):
            return 'ortho'
        return 'persp'
    
    def get_focal_length(self) -> float:
        if self.canvas.axes._focal_length in (None, np.inf):
            return 1
        else: return self.canvas.axes._focal_length