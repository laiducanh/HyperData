import sys, qfluentwidgets, os, json

from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtWidgets import (QWidget, QMenuBar, QVBoxLayout, QStackedLayout, QApplication, QFileDialog, QSplashScreen,
                             QMainWindow)
from PyQt6.QtGui import QCloseEvent, QGuiApplication, QKeyEvent, QMouseEvent, QPaintEvent, QPixmap, QAction, QColor

from plot.plot_view import PlotView
from node_editor.node_view import NodeView
from node_editor.node_node import Node
from config.settings_window import SettingsWindow
from config.settings import config
from config.threadpool import Worker

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

except ImportError:
    pass

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()
        self.list_figure = list()
        self.settings_window = SettingsWindow(self)
           
        ### Adjust the main window's size
        #self.setMinimumSize(int(self.screen_size[2]*0.55),int(self.screen_size[3]*0.55)) # set minimum size for display
            
        self.setupMenuBar()

        self.central_widget = QWidget(self)
        self.mainlayout = QStackedLayout()
        self.central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.central_widget)

        self.add_node_view()
        
        self.btn = qfluentwidgets.PushButton()
        self.btn.clicked.connect(self.func)
        #self.mainlayout.addWidget(self.btn)
        print(self.threadpool)
    
    def func(self):
        import pandas as pd
        worker = Worker(pd.read_csv, r"F:\Box\Study at SMU\Course\Fall 2023\CADD\pdb_total.csv")
        worker.signals.finished.connect(lambda: print('load data done'))
        self.threadpool.start(worker)
        
    def setupMenuBar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        fileMenu = menu_bar.addMenu('&File')
        action = QAction('&Load',self)
        action.triggered.connect(self.loadFromFile)
        fileMenu.addAction(action)
        action = QAction('&Save',self)
        action.triggered.connect(self.saveToFile)
        fileMenu.addAction(action)
        action = QAction('&Settings',self)
        action.triggered.connect(self.settings_window.show)
        fileMenu.addAction(action)
        fileMenu.addSeparator()
        action = QAction('&Quit', self)
        action.triggered.connect(self.close)
        fileMenu.addAction(action)        
        
    def add_plot_view (self, node: Node):
        
        plot_view = PlotView( node, node.content.canvas, self)
        self.list_figure.append(node.id)
        plot_view.sig_back_to_grScene.connect(lambda: self.mainlayout.setCurrentIndex(0))
        self.mainlayout.addWidget(plot_view)
        self.mainlayout.setCurrentWidget(plot_view)

    def add_node_view (self):
        self.node_view = NodeView(self)
        self.mainlayout.addWidget(self.node_view)
        self.node_view.sig.connect(self.node_signal)        
        self.mainlayout.setCurrentIndex(0)
    
    def node_signal (self, node:Node):
        if node.title == 'Figure':
            self.to_plot_view(node)
    
    def to_plot_view (self, node: Node):
        if node.id in self.list_figure:
            self.mainlayout.setCurrentIndex(self.list_figure.index(node.id)+1)
        else:
            self.add_plot_view(node)
        
    def keyPressEvent(self, event:QKeyEvent) -> None:

        if event.key() == Qt.Key.Key_S and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.saveToFile()
        elif event.key() == Qt.Key.Key_L and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.loadFromFile()
        else:
            super().keyPressEvent(event)
    
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        return super().mouseMoveEvent(a0)

    def saveToFile(self):
        dialog = QFileDialog(self)
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "w") as file:
                file.write( json.dumps( self.serialize(), indent=4 ) )
            print("saving to", filename, "was successfull.")
    
    def loadFromFile(self):
        dialog = QFileDialog(self)
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            with open(filename, "r") as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                self.deserialize(data)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        with open("config.json.txt", "w") as file:
            file.write( json.dumps(config, indent=4 ) )
        return super().closeEvent(a0)

    def serialize(self):
        return {"id":id(self),
                "screen size":QGuiApplication.primaryScreen().geometry().getRect(),
                "graphic Scene":self.node_view.grScene.serialize()}
        
    def deserialize(self, data, hashmap={}):
        print("deserializating data")
        self.node_view.grScene.deserialize(data["graphic Scene"], hashmap={})
     

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    
    app = QApplication(sys.argv)
    pixmap = QPixmap(os.path.join('UI','Icons','app-icon.png'))
    splashScreen = QSplashScreen(pixmap)
    splashScreen.show()
    splashScreen.showMessage('Loading modules ...',alignment=Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignCenter)
    app.processEvents()
    app.setStyle('Fusion')
    main_window = Main()
    main_window.show()
    splashScreen.close()
    
    sys.exit(app.exec())
