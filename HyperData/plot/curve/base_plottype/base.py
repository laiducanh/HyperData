from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QSizePolicy
from PySide6.QtCore import Signal, QTimer
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from ui.base_widgets.button import SegmentedWidget, HToggle, HButton, TransparentToolButton
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.frame import SeparateHLine, ScrollArea
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from plot.utilis import find_mpl_object, set_zorder
from plot.plotting.plotting import set_legend, get_legend
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import artist

class PlotConfigBase(QWidget):
    onChanged = Signal()
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.vlayout = QVBoxLayout(self)
        # self.vlayout.setContentsMargins(0,0,0,0)
        self.segment = SegmentedWidget(parent)
        self.vlayout.addWidget(self.segment)

        self.stackedlayout = QStackedLayout()
        self.vlayout.addLayout(self.stackedlayout)

        self.segment.addButton(text='General', func=lambda: self.stackedlayout.setCurrentIndex(0))

        self.general = GeneralPlot(gid, canvas, parent)
        self.stackedlayout.addWidget(self.general)
        
    def update_props(self):
        pass

    def update_plot(self):
        self.plot.plotting()
        self.onChanged.emit()
    
    def _onChange(self):
        self.onChanged.emit()
        self.general.update_legend()

class GeneralPlot(ScrollArea):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(parent=parent)

        self.gid = gid
        self.canvas = canvas

    # Timer for updating legend
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.set_label)
    
    # Legend
        self.legend = HLineEdit(label='Legend')
        self.legend.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.legend.button.setText(self.get_label())
        self.legend.button.textChanged.connect(lambda: self.timer.start(300))
        self.vlayout.addWidget(self.legend)
        self.vlayout.addWidget(SeparateHLine())

        self.addlayout = QVBoxLayout()
        self.addlayout.setContentsMargins(0,0,0,0)
        self.vlayout.addLayout(self.addlayout)

        clip = HToggle(
            label="Clipping",
            setter=self.set_clip,
            getter=self.get_clip,
            layout=self.vlayout
        )

        zorder = HButton(
            label="Arrange",
            layout=self.vlayout
        )
        TransparentToolButton(
            icon='bring_to_front.png',
            toolTip='Bring to Front',
            setter=lambda: self.set_zorder('Bring to Front'),
            layout=zorder.butn_layout
        )
        TransparentToolButton(
            icon='send_to_back.png',
            toolTip='Send to Back',
            setter=lambda: self.set_zorder('Send to Back'),
            layout=zorder.butn_layout
        )
        TransparentToolButton(
            icon='bring_forward.png',
            toolTip='Bring Forward',
            setter=lambda: self.set_zorder('Bring Forward'),
            layout=zorder.butn_layout
        )
        TransparentToolButton(
            icon='send_backward.png',
            toolTip='Send Backward',
            setter=lambda: self.set_zorder('Send Backward'),
            layout=zorder.butn_layout
        )
    
    def find_obj(self):
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[artist.Artist],
            gid=self.gid,
        )

    def set_label (self):
        try:
            if self.legend.button.text() == "":
                _label = "_"
            else: _label = self.legend.button.text()
            for obj in self.find_obj():
                if not obj.get_gid().startswith('_'):
                    obj.set_label(_label)
            set_legend(self.canvas.figure)
            self.canvas.draw_idle()
            
        except Exception as e:
            logger.exception(e)

    def get_label (self) -> str:
        # skip label starting with "_"
        for obj in self.find_obj():
            if obj.get_label().startswith("_"):
                return None
            return obj.get_label()
    
    def update_legend (self):
        try:
            if get_legend(self.canvas.figure): set_legend(self.canvas.figure)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)

    def set_clip(self, bool):
        try:
            for obj in self.find_obj():
                obj.set_clip_on(bool)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)   
    
    def get_clip(self) -> bool:
        return self.find_obj()[0].get_clip_on()
    
    def set_zorder(self, value:float):
        try:
            set_zorder(self.canvas.figure, self.gid, value)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)