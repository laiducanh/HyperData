from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPaintEvent
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib.artist import Artist

class ArtistConfigBase(QWidget):
    onChange = Signal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.obj = self.find_object()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_plot)

        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
    
    def find_object (self) -> list[Artist]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Artist],
            gid=self.gid
        )

    def update_props(self):
        pass

    def prepare_update(self, wait_time=300):
        #self.timer.start(wait_time)
        self.update_plot()
    
    def update_plot(self):
        self.onChange.emit()
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()            
        return super().paintEvent(a0)
