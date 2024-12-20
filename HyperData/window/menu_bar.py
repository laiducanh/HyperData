from PySide6.QtWidgets import QMenuBar, QMainWindow
from PySide6.QtGui import QAction
from config.settings_window import SettingsWindow
from window.update import UpdateDialog


class MenuBar(QMenuBar):
    def __init__(self, parent:QMainWindow):
        super().__init__(parent)

        # parent is the Main
    
        fileMenu = self.addMenu('File')
        action = QAction('Load',self)
        action.triggered.connect(self.parent().loadFromFile)
        fileMenu.addAction(action)
        action = QAction('Save',self)
        action.triggered.connect(self.parent().saveToFile)
        fileMenu.addAction(action)
        action = QAction('\0Settings',self)
        action.triggered.connect(self.setting_onClick)
        fileMenu.addAction(action)
        fileMenu.addSeparator()
        action = QAction('\0Quit', self)
        action.triggered.connect(parent.close)
        fileMenu.addAction(action)       

        aboutMenu = self.addMenu('About')
        action = QAction('Check update',self)
        action.triggered.connect(self.checkupdate_onClick)
        aboutMenu.addAction(action)       
    
        self.settings_window = SettingsWindow(parent)
        self.updateDialog = UpdateDialog(parent=parent)

    def setting_onClick(self):
        self.settings_window.show()
    
    def checkupdate_onClick(self):
        self.updateDialog.exec()