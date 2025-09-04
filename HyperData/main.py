import sys, os, json, logging

# forcing software-based backend on MacOS
# because of Bus error 10
os.environ["QT_QUICK_BACKEND"] = "software"

from PySide6.QtCore import QThreadPool, Qt, QDir
from PySide6.QtWidgets import (QWidget, QStackedLayout, QApplication, QMainWindow, QStyleFactory, 
                               QFileDialog, QVBoxLayout, QTextBrowser)
from PySide6.QtGui import (QCloseEvent, QGuiApplication, QKeyEvent, QMouseEvent, QPaintEvent)

from plot.plot_view import PlotView, PlotViewMultiFig
from node_editor.node_view import NodeView, NodeUserDefine
from node_editor.node_node import Node, Figure2D, Figure3D, MultiFigure, UserDefine
from window.menu_bar import MenuBar
from ui.base_widgets.window import FileDialog
from ui.base_widgets.text import TextEditLogger
from config.settings import GLOBAL_DEBUG, config, logger
from ui.utils import get_path

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
except ImportError as e:
    logger.exception(e)

__version__ = config["version"]

DEBUG = True

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()
        self.stack_scene = list()
           
        ### Adjust the main window's size
        #self.setMinimumSize(int(self.screen_size[2]*0.55),int(self.screen_size[3]*0.55)) # set minimum size for display

        menu_bar = MenuBar(self)
        self.setMenuBar(menu_bar)

        self.central_widget = QWidget()
        self.vlayout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        widget = QWidget()
        self.mainlayout = QStackedLayout(widget)
        self.vlayout.addWidget(widget)            

        if GLOBAL_DEBUG or DEBUG: self.debug()
        
        # show Node view as default
        self.add_node_view()
    
    def debug(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        text = QTextBrowser()
        text.setMinimumHeight(200)
        log_handler = TextEditLogger(text)
        log_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        logger.addHandler(log_handler)
        self.vlayout.addWidget(text)

    def add_node_view (self):
        self.node_view = NodeView(self)
        self.mainlayout.addWidget(self.node_view)
        self.node_view.sig.connect(self.node_signal)        
        self.mainlayout.setCurrentIndex(0)
    
    def node_signal (self, node:Node):
        if isinstance(node.content, (Figure2D)):
            self.to_plot_view(node)
        elif isinstance(node.content, UserDefine):
            self.to_graphics_view(node)
    
    def to_plot_view (self, node: Node):
        if node.id in self.stack_scene:
            self.mainlayout.setCurrentIndex(self.stack_scene.index(node.id)+1)
        else:
            if isinstance(node.content, MultiFigure):
                plot_view = PlotViewMultiFig(node, node.content.canvas, self)
            elif isinstance(node.content, Figure3D):
                plot_view = PlotView(node, node.content.canvas, self)
            elif isinstance(node.content, Figure2D):
                plot_view = PlotView(node, node.content.canvas, self)

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
    
    def saveToFile(self):
        dialog = FileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        # dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        if dialog.exec():
            try:
                dir = dialog.selectedFiles()[0]
                config['save_path'] = dir
                self.serialize()
                with open(os.path.join(dir, 'config.json.txt'), "w") as file:
                    file.write(json.dumps(config, indent=4))
                logger.info(f"saving to {dir} was successfull.")
                config['save_path'] = str()
            except Exception as e:
                logger.exception(e)
    
    def loadFromFile(self):
        dialog = FileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        if dialog.exec():
            dir = dialog.selectedFiles()[0]
            config['save_path'] = dir
            with open(os.path.join(dir, 'config.json.txt'), "r") as file:
                raw_data = file.read()
                data = json.loads(raw_data)
                self.deserialize(data)
            config['save_path'] = str()
    
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        return super().mouseMoveEvent(a0)

    def paintEvent(self, a0: QPaintEvent) -> None: 
        return super().paintEvent(a0)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.serialize()
        with open(os.path.join(config["root_path"], "config.json.txt"), 'w') as file:
            file.write(json.dumps(config, indent=4))
        return super().closeEvent(a0)

    def serialize(self):

        config.update(
            id=id(self),
            screen_size=QGuiApplication.primaryScreen().geometry().getRect(),
            node_view=self.node_view.serialize(),
        )
        
    def deserialize(self, data:dict, hashmap={}):
        
        config = data.copy()
        while self.mainlayout.count() > 1:
            self.mainlayout.takeAt(1)
            self.stack_scene.pop(0)
        self.node_view.deserialize(config["node_view"], hashmap={})
        
     

if __name__ == "__main__":
        
    logger.info(f"Path: {get_path()}.")
    QDir.addSearchPath('ui', os.path.join(get_path(), 'ui'))

    # QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)

    # Set Windows style for all platforms
    app.setStyle(QStyleFactory.create("Windows"))
    
    main_window = Main()
    main_window.show()

    sys.exit(app.exec())
