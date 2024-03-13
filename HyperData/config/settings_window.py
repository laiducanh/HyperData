from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QDockWidget, QStackedLayout
from PyQt6.QtCore import QSize, Qt

from ui.base_widgets.button import _ComboBox
from ui.base_widgets.color import _ColorDropdown
from ui.base_widgets.text import _LineEdit
from config.settings import config
import qfluentwidgets

class Theme (qfluentwidgets.CardWidget):
    def __init__(self, parent:QMainWindow=None):
        super().__init__(parent)

        self._parent = parent

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(qfluentwidgets.BodyLabel("Theme"))

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        self.auto = qfluentwidgets.RadioButton("Auto")
        self.auto.clicked.connect(self.setAuto)
        button_layout.addWidget(self.auto)

        self.light = qfluentwidgets.RadioButton("Light")
        self.light.clicked.connect(self.setLight)
        button_layout.addWidget(self.light)

        self.dark = qfluentwidgets.RadioButton("Dark")
        self.dark.clicked.connect(self.setDark)
        button_layout.addWidget(self.dark)

        self.setInit()
    
    def setInit (self):
        if config["theme"] == 'Light':
            self.light.setChecked(True)
            self.setLight()
        elif config["theme"] == "Dark":
            self.dark.setChecked(True)
            self.setDark()
        else:
            self.auto.setChecked(True)
            self.setAuto()

    def setAuto (self):
        qfluentwidgets.setTheme(qfluentwidgets.Theme.AUTO)
        config["theme"] = "Auto"
        self.setBackgroundColor()

    def setLight (self):
        qfluentwidgets.setTheme(qfluentwidgets.Theme.LIGHT)
        config["theme"] = "Light"
        self.setBackgroundColor()
    
    def setDark (self):
        qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK)  
        config["theme"] = "Dark"
        self.setBackgroundColor()
    
    def setBackgroundColor (self):
        if qfluentwidgets.isDarkTheme():
            self._parent.setStyleSheet("QMainWindow,QMenuBar {background-color:rgb(32, 32, 32);color:white}")
        else:
            self._parent.setStyleSheet("QMainWindow,QMenuBar {background-color:rgb(243, 243, 243);color:black}")

class ThemeColor (qfluentwidgets.CardWidget):
    def __init__(self, parent:QDockWidget=None):
        super().__init__(parent=parent)

        self.setInit()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self._parent = parent

        layout.addWidget(qfluentwidgets.BodyLabel("Theme Color"))
        button = _ColorDropdown(config["theme color"], parent)
        button.colorChanged.connect(self.setColor)
        layout.addWidget(button)
    
    def setInit (self):
        qfluentwidgets.setThemeColor(config["theme color"])
    
    def setColor (self, color):
        qfluentwidgets.setThemeColor(color)
        config["theme color"] = color

class DockWidget_Position (qfluentwidgets.CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(qfluentwidgets.BodyLabel("Panel Position"))
        button = _ComboBox(items=["left","right","top","bottom"])
        button.currentTextChanged.connect(self.setPos)
        button.setCurrentText(config["dock area"].title())
        layout.addWidget(button)
    
    def setPos (self, pos):
        config["dock area"] = pos.lower()
    
class SettingsWindow (QMainWindow):
    def __init__(self, parent:QMainWindow=None):
        super().__init__(parent)

        self.sidebar = qfluentwidgets.ListWidget()
        self.sidebar.addItems(["Appearance","Shortcuts"])
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
        appearance_layout.addWidget(ThemeColor(parent))

        shortcut = QWidget()
        shortcut_layout = QVBoxLayout()
        shortcut.setLayout(shortcut_layout)
        layout.addWidget(shortcut)

        
