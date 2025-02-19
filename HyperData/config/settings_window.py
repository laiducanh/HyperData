from PySide6.QtGui import QKeyEvent, QAction, QIcon, QColor
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, 
                               QDockWidget, QStackedLayout, QApplication, QGraphicsScene)
from PySide6.QtCore import QSize, Qt
import matplotlib.figure
import matplotlib.pyplot
import matplotlib.style

from ui.base_widgets.button import _ComboBox, ComboBox, Toggle
from ui.base_widgets.color import ColorPickerButton
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import Frame
from ui.base_widgets.list import ListWidget
from ui.base_widgets.spinbox import SpinBox
from ui.utils import get_path
from config.settings import config
import os, darkdetect, sys, matplotlib, itertools, cycler, numpy

class Theme (Frame):
    def __init__(self, parent:QMainWindow=None):
        super().__init__(parent)

        self._parent = parent
        self.app = QApplication.instance()

        layout = QHBoxLayout()
        self.setLayout(layout)

        theme = ComboBox(items=["Auto","Light","Dark"], text="Appearance", 
                         text2="Customize how app looks on your device", parent=parent)
        theme.button.currentTextChanged.connect(self.setTheme)
        theme.button.setCurrentText(self.get_theme())
        layout.addWidget(theme)

        self.setTheme(config["theme"])


    def setTheme (self, theme):
        config["theme"] = theme
        if theme == "Auto":
            theme = darkdetect.theme()
        self._setStyleSheet(theme.lower())
    
    def get_theme(self) -> str:
        return config["theme"]
        
    def _setStyleSheet (self, theme=["light","dark"]):
        string = str()
        path = os.path.join(get_path(), "ui","qss", theme)
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r') as f:
                string += f.read()
        self.app.setStyleSheet(string)
        # for widget in self.app.allWidgets():
        #     if widget.isVisible():
        #         try: widget.update()
        #         except: pass

class DockWidget_Position (Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(BodyLabel("Panel Position"))
        button = _ComboBox(items=["Left","Right","Top","Bottom"])
        button.currentTextChanged.connect(self.setPos)
        button.setCurrentText(config["dock area"])
        layout.addWidget(button)
    
    def setPos (self, pos):
        config["dock area"] = pos

class Figure_Tooltip(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        button = Toggle(text="Show Tooltip")
        button.button.setChecked(config["plot_tooltip"])
        button.button.checkedChanged.connect(lambda s: config.update(plot_tooltip=s))
        layout.addWidget(button)

class Figure_Dpi(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        button = SpinBox(text="DPI", min=50,max=3000,step=50)
        button.button.setValue(config["plot_dpi"])
        button.button.valueChanged.connect(lambda s: config.update(plot_dpi=s))
        layout.addWidget(button)

class Figure_Style(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._parent: QMainWindow = parent
        layout = QHBoxLayout()
        self.setLayout(layout)
        style_list = ["default", "matplotlib default"] + matplotlib.style.available
        button = ComboBox(items=style_list, text="Style")
        button.button.currentTextChanged.connect(self.changeStyle)
        button.button.setCurrentText(config["plot_style"])
        layout.addWidget(button)

        self.changeStyle(button.button.currentText())
    
    def changeStyle(self, value:str):
        config.update(plot_style = value)
        if value == "default":
            matplotlib.pyplot.style.use(os.path.join("config/style.mplstyle"))
        elif value == "matplotlib default":
            matplotlib.pyplot.style.use("default")
        else:
            matplotlib.pyplot.style.use(value)
        # for scene in self._parent.findChildren(QGraphicsScene):
        #     scene: QGraphicsScene
        #     for item in scene.items():
        #         if isinstance(item, Node):
        #             try: 
        #                 item.content.canvas.draw()
        #             except: pass
 
class Figure_Colors(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.palette_dict = {
            "red": ["#03071e","#6a040f","#d00000","#e85d04","#faa307"], 
            "blue": ["#03045e","#0077b6","#00b4d8","#90e0ef","#caf0f8"],
            "black": ["#212529","#343a40","#495057","#6c757d","#adb5bd"],
            "white": ["#f8f9fa","#e9ecef","#dee2e6","#ced4da","#adb5bd"],
            "gray": ["#595959","#7f7f7f","#a5a5a5","#cccccc","#f2f2f2"],
            "yellow": ["#ffba08","#faa307","#f48c06","#e85d04","#dc2f02"],
            "brown": ["#522500","#713200","#8f3e00","#a85311","#c06722"],
            "green": ["#004b23","#006400","#007200","#008000","#38b000"],
            "violet": ["#240046","#3c096c","#5a189a","#7b2cbf","#9d4edd"],
            "pink": ["#ff4d6d","#ff758f","#ff8fa3","#ffb3c1","#ffccd5"],
            "dark red": ["#250902","#38040e","#640d14","#800e13","#ad2831"],
            "dark blue": ["#02010a","#04052e","#140152","#22007c","#0d00a4"],
            "dark pink": ["#590d22","#800f2f","#a4133c","#c9184a","#ff4d6d"],
            "custom": [],

        }

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)
        self._palette = ComboBox(text="Color Palette", items=self.palette_dict.keys())
        self._palette.button.setCurrentText("custom")
        for key, value in self.palette_dict.items():
            if config["plot_palette"] == value:
                self._palette.button.setCurrentText(key)
        self._palette.button.currentTextChanged.connect(self.changePalette)
        layout1.addWidget(self._palette)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)
        for idx in range(5):
            btn = ColorPickerButton(QColor(config["plot_palette"][idx]))
            btn.setFixedSize(80, 32)
            btn.colorChanged.connect(lambda color, i=idx: self.changeColor(color, i))
            layout2.addWidget(btn)
        
        self.createPalette()

    def changePalette(self, palette:str):
        palette = self.palette_dict[palette].copy()
        if palette:
            config.update(plot_palette = palette)
            for color, btn in zip(palette, self.findChildren(ColorPickerButton)):
                btn: ColorPickerButton
                btn.setColor(color)
        else:
            palette = [None]*5
            for idx, btn in enumerate(self.findChildren(ColorPickerButton)):
                btn: ColorPickerButton
                palette[idx] = matplotlib.colors.to_hex(btn.color.getRgbF())
            config.update(plot_palette = palette)
        self.createPalette()
        
    def changeColor(self, color:str, idx:int):
        custom = self.palette_dict[self._palette.button.currentText()].copy()
        custom[idx] = color
        self.palette_dict.update(custom = custom)
        config.update(plot_palette = custom)
        self._palette.button.setCurrentText("custom")
    
    def createPalette(self):
        color_lib = config["plot_palette"].copy()
        for i in range(3):
            for point in range(len(color_lib)-1):
                if point < len(color_lib) - 1:
                    c = ([matplotlib.colors.to_rgb(color_lib[point]),
                        matplotlib.colors.to_rgb(color_lib[point+1])])
                    c = matplotlib.colors.to_hex(numpy.mean(c, axis=0))
                color_lib.append(c)
        color_lib = list(dict.fromkeys(color_lib))
        matplotlib.rcParams["axes.prop_cycle"] = cycler.cycler(color=color_lib)
    
class SettingsWindow (QMainWindow):
    def __init__(self, parent:QMainWindow=None):
        super().__init__(parent)

        self.sidebar = ListWidget()
        self.sidebar.addItems(["Appearance","Figure"])
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(lambda: layout.setCurrentIndex(self.sidebar.currentRow()))

        layout = QStackedLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setFixedSize(QSize(700,500))

        self.dock = QDockWidget('sidebar')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dock.setWidget(self.sidebar)
        self.dock.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

        appearance = QWidget()
        appearance_layout = QVBoxLayout()
        appearance.setLayout(appearance_layout)
        layout.addWidget(appearance)

        appearance_layout.addWidget(Theme(parent))
        appearance_layout.addWidget(DockWidget_Position(parent))
        appearance_layout.addStretch()

        figure = QWidget()
        figure_layout = QVBoxLayout(figure)
        layout.addWidget(figure)

        figure_layout.addWidget(Figure_Tooltip(parent))
        figure_layout.addWidget(Figure_Dpi(parent))
        figure_layout.addWidget(Figure_Style(parent))
        figure_layout.addWidget(Figure_Colors(parent))
        figure_layout.addStretch()