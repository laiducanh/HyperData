from PySide6.QtWidgets import QDialog, QVBoxLayout
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.frame import VFrame, ScrollArea
from plot.canvas import Canvas
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class ColorBar(QDialog):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle('Colorbar')
        self.setMinimumWidth(500)
        self.canvas = canvas
            
        layout = QVBoxLayout(self)
        scrollarea = ScrollArea()
        layout.addWidget(scrollarea)

        self.canvas = canvas
        fr = VFrame(scrollarea.vlayout)

        HToggle(
            label="Visible",
            label2="Whether to draw colorbar",
            setter=self.set_visible,
            getter=self.get_visible,
            layout=fr.vlayout
        )

        HTransparentSpinBox(
            label="Size",
            label2="Width of the colorbar",
            minimum = 0, maximum = 100, singleStep=1,
            setter=self.set_size,
            getter=self.get_size,
            layout=fr.vlayout
        )

        HTransparentSpinBox(
            label="Padding",
            minimum = 0, maximum = 100, singleStep=1,
            label2="The space between labels and colorbar",
            setter=self.set_pad,
            getter=self.get_pad,
            layout=fr.vlayout
        )

        HTransparentComboBox(
            label="Location",
            label2="Where to draw colorbar",
            items=["left","bottom","right"],
            setter=self.set_loc,
            getter=self.get_loc,
            layout=fr.vlayout
        )

    def set_visible(self, value):
        self.canvas._config["cbar"]["visible"] = value
        self.canvas.colorbar()
    
    def get_visible(self):
        return self.canvas._config["cbar"]["visible"]

    def set_size(self, value):
        self.canvas._config["cbar"]["size"] = value/100
        self.canvas.colorbar()
    
    def get_size(self):
        return int(self.canvas._config["cbar"]["size"]*100)
    
    def set_pad(self, value):
        self.canvas._config["cbar"]["pad"] = value/100
        self.canvas.colorbar()
    
    def get_pad(self):
        return int(self.canvas._config["cbar"]["pad"]*100)

    def set_loc(self, value):
        self.canvas._config["cbar"]["loc"] = value
        self.canvas.colorbar()
    
    def get_loc(self):
        return self.canvas._config["cbar"]["loc"]