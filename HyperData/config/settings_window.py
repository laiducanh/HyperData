from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize

from config.settings import config
from ui.base_widgets.button import ComboBox
from ui.base_widgets.color import ColorDropdown
import qfluentwidgets

class SettingsWindow (QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setFixedSize(QSize(700,500))

        theme = ComboBox(items=["Auto","Light","Dark"], text='Theme')
        theme.button.setCurrentText(config.value("theme"))
        layout.addWidget(theme)
        theme.button.currentTextChanged.connect(self.setTheme)  

        dockwidget_pos = ComboBox(items=["left","right","top","bottom"],text='panel position')
        layout.addWidget(dockwidget_pos)
        dockwidget_pos.button.setCurrentText(config.value("dock area").title())
        dockwidget_pos.button.currentTextChanged.connect(self.setPanelPosition)

        themecolor = ColorDropdown(text="theme color", color=config.value("theme color"), parent=parent)
        themecolor.button.colorChanged.connect(self.setThemeColor)
        layout.addWidget(themecolor)


    def setTheme(self, theme:str):
        config.setValue("theme", theme)
        if theme == "Auto":
            qfluentwidgets.setTheme(qfluentwidgets.Theme.AUTO)
        elif theme == "Light":
            qfluentwidgets.setTheme(qfluentwidgets.Theme.LIGHT)
        elif theme == "Dark":
            qfluentwidgets.setTheme(qfluentwidgets.Theme.DARK)     
    
    def setThemeColor(self, color):
        qfluentwidgets.setThemeColor(color)
    def setPanelPosition(self, pos:str):
        config.setValue("dock area",pos.lower())