from PySide6.QtGui import QKeyEvent, QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QDockWidget, QStackedLayout, QApplication
from PySide6.QtCore import QSize, Qt

from ui.base_widgets.button import _ComboBox, ComboBox, Toggle
from ui.base_widgets.color import ColorPickerButton
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import Frame
from ui.base_widgets.list import ListWidget
from ui.utils import get_path
from config.settings import config
import os, darkdetect, sys

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

        figure = QWidget()
        figure_layout = QVBoxLayout(figure)
        layout.addWidget(figure)

        figure_layout.addWidget(Figure_Tooltip(parent))

        
