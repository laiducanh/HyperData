from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QWidget
from ui.base_widgets.frame import ScrollArea
from plot.canvas import Canvas

class ArtistConfigBase(ScrollArea):
    onChanged = Signal()
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(parent=parent)

        self.gid = gid
        self.canvas = canvas
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
        self.onChanged.emit()
        self.canvas.draw_idle()
