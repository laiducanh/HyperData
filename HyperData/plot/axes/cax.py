from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QStackedLayout
from PySide6.QtGui import QColor
from ui.base_widgets.button import HTransparentComboBox, HToggle, SegmentedWidget, ToggleToolButton, HButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.frame import ScrollArea, HFrame, VFrame
from plot.utilis import find_mpl_object, grid
from plot.canvas import Canvas
from matplotlib import rcParams, colors, lines
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class ColorBar(ScrollArea):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        fr = VFrame(self.vlayout)

        HToggle(
            label="Visible",
            label2="Whether to draw colorbar",
            layout=fr.vlayout
        )
    