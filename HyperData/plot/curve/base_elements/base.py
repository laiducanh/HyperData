from PySide6.QtCore import QTimer, QObject
from PySide6.QtWidgets import QWidget
from ui.base_widgets.list import TreeWidget, TreeWidgetItem
from plot.canvas import Canvas

class ArtistConfigBase (QWidget):
    def __init__(self, gid:str, canvas:Canvas, treeview:TreeWidget, parent:TreeWidgetItem):
        super().__init__(treeview)

        self.gid = gid
        self.canvas = canvas
        self.treeview = treeview
        self.parent = parent
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_plot)
    
    def find_object (self):
        pass

    def update_props(self):
        pass

    def prepare_update(self, wait_time=300):
        #self.timer.start(wait_time)
        self.update_plot()
    
    def update_plot(self):
        self.treeview.sig_onChange.emit()
        self.canvas.draw_idle()
