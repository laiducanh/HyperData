import sys, os, json

from PyQt6.QtCore import QThreadPool, Qt
from PyQt6.QtWidgets import (QWidget, QMenuBar, QStackedLayout, QApplication, QFileDialog, QSplashScreen,
                             QMainWindow)
from PyQt6.QtGui import (QCloseEvent, QGuiApplication, QKeyEvent, QMouseEvent, QPaintEvent, QPixmap, 
                         QAction)

from plot.plot_view import PlotView
from node_editor.node_view import NodeView, NodeUserDefine
from node_editor.node_node import Node, Figure, UserDefine
from config.settings_window import SettingsWindow
from config.settings import config
from ui.base_widgets.button import ComboBox
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
        self.stack_scene = list()
        self.settings_window = SettingsWindow(self)
           
        ### Adjust the main window's size
        #self.setMinimumSize(int(self.screen_size[2]*0.55),int(self.screen_size[3]*0.55)) # set minimum size for display
            
        self.setupMenuBar()

        self.central_widget = QWidget(self)
        self.mainlayout = QStackedLayout()
        self.central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.central_widget)
        
        self.add_node_view()
        
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
        

    def add_node_view (self):
        self.node_view = NodeView(self)
        self.mainlayout.addWidget(self.node_view)
        self.node_view.sig.connect(self.node_signal)        
        self.mainlayout.setCurrentIndex(0)
    
    def node_signal (self, node:Node):
        if isinstance(node.content, Figure):
            self.to_plot_view(node)
        elif isinstance(node.content, UserDefine):
            self.to_graphics_view(node)
    
    def to_plot_view (self, node: Node):
        self.showMaximized()
        if node.id in self.stack_scene:
            self.mainlayout.setCurrentIndex(self.stack_scene.index(node.id)+1)
        else:
            plot_view = PlotView( node, node.content.canvas, self)
            self.stack_scene.append(node.id)
            plot_view.sig_back_to_grScene.connect(lambda: self.mainlayout.setCurrentIndex(0))
            self.mainlayout.addWidget(plot_view)
            self.mainlayout.setCurrentWidget(plot_view)
    
    def to_graphics_view (self, node: Node):
        if node.id in self.stack_scene:
            self.mainlayout.setCurrentIndex(self.stack_scene.index(node.id)+1)
        else:
            node_view = NodeUserDefine(main_node=node, parent=self)
            self.mainlayout.addWidget(node_view)
            self.mainlayout.setCurrentWidget(node_view)
            node_view.sig_back_to_grScene.connect(lambda: self.mainlayout.setCurrentIndex(0))
            self.stack_scene.append(node.id)
        
    def keyPressEvent(self, event:QKeyEvent) -> None:

        if event.key() == Qt.Key.Key_S and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.saveToFile()
        elif event.key() == Qt.Key.Key_L and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.loadFromFile()
        else:
            super().keyPressEvent(event)
    
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        return super().mouseMoveEvent(a0)

    def paintEvent(self, a0: QPaintEvent) -> None:
        
        return super().paintEvent(a0)
    
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
    
    
    app = QApplication(sys.argv)
    
    #pixmap = QPixmap(os.path.join('UI','Icons','app-icon.png'))
    #splashScreen = QSplashScreen(pixmap)
    #splashScreen.show()
    #splashScreen.showMessage('Loading modules ...',alignment=Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignCenter)
    #app.processEvents()
    main_window = Main()
    main_window.show()
    #splashScreen.close()

    sys.exit(app.exec())
