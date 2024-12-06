from PyQt6.QtWidgets import QMenuBar, QMainWindow, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal
from config.settings_window import SettingsWindow
from window.update import UpdateDialog


class MenuBar(QMenuBar):
    load = pyqtSignal()
    save = pyqtSignal()
    def __init__(self, parent:QMainWindow):
        super().__init__(parent)
    
        fileMenu = self.addMenu('File')
        action = QAction('Load',self)
        action.triggered.connect(self.loadFromFile)
        fileMenu.addAction(action)
        action = QAction('Save',self)
        action.triggered.connect(self.saveToFile)
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

    def saveToFile(self):
        dialog = QFileDialog(self)
        
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "w") as file:
                file.write( json.dumps( self.parent().serialize(), indent=4 ) )
            print("saving to", filename, "was successfull.")
    
    def loadFromFile(self):
        dialog = QFileDialog(self)
        
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "r") as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                self.parent().deserialize(data)