from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QSizePolicy
from PySide6.QtCore import Signal, QTimer
from plot.insert_plot.insert_plot import InsertPlot
from plot.canvas import Canvas
from ui.base_widgets.button import SegmentedWidget, TransparentComboBox, Toggle
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import TransparentSpinBox
from node_editor.node_node import Node
from plot.utilis import find_mpl_object
from plot.insert_plot.utilis import plotting
from plot.plotting.plotting import set_legend, get_legend
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import artist

AXES = 0
AXES_Y2 = 1
AXES_X2 = 2
AXES_PIE = 3

class PlotConfigBase (QWidget):
    onChanged = Signal()
    def __init__(self, gid:str, canvas:Canvas, node:Node, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.node = node

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
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
        plotting()
        self.onChanged.emit()
    
    def _onChange(self):
        self.onChanged.emit()
        self.general.update_legend()

class AxesPlot(QWidget):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.ax = self.canvas.fig.axes.index(self.find_obj()[0].axes)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.choose_axis1 = TransparentComboBox(
            text="Horizontal Axis",
            items=["Bottom","Top"],
            setter=self.set_ax,
            getter=lambda: self.get_ax()[0],
            layout=layout
        )
        
        self.choose_axis2 = TransparentComboBox(
            text="Vertical Axis",
            items=["Left","Right"],
            setter=self.set_ax,
            getter=lambda: self.get_ax()[1],
            layout=layout
        )
    
    def find_obj(self):
        return find_mpl_object(
            source=self.canvas.fig,
            match=[artist.Artist],
            gid=self.gid,
        )
    
    def get_ax(self):
        if self.ax == AXES:
            return ["Bottom","Left"]
        elif self.ax == AXES_X2:
            return ["Top","Left"]
        elif self.ax == AXES_Y2:
            return ["Bottom","Right"]
    
    def set_ax(self):
        _ax1 = self.choose_axis1.button.currentText()
        _ax2 = self.choose_axis2.button.currentText()
        if _ax1 == "Bottom" and _ax2 == "Left":
            for obj in self.find_obj():
                self.canvas.axes.add_artist(obj)
                obj.remove()
        elif _ax1 == "Bottom" and _ax2 == "Right":
            for obj in self.find_obj():
                self.canvas.axes.add_artist(obj)
                obj.remove()
        # elif _ax1 == "Top" and _ax2 == "Left":
        #     self.plot.plotting(_ax=AXES_X2)
        # elif _ax1 == "Top" and _ax2 == "Right":
        #     self.plot.plotting(_ax=AXES)

class GeneralPlot(QWidget):
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)

    # Timer for updating legend
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.set_label)
    
    # Legend
        self.legend = LineEdit(text='Legend')
        self.legend.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.legend.button.setText(self.get_label())
        self.legend.button.textChanged.connect(lambda: self.timer.start(300))
        self.vlayout.addWidget(self.legend)
        self.vlayout.addWidget(SeparateHLine())

        clip = Toggle(
            text="Clipping",
            setter=self.set_clip,
            getter=self.get_clip,
            layout=self.vlayout
        )

        zorder = TransparentSpinBox(
            text="Z-order",
            setter=self.set_zorder,
            getter=self.get_zorder,
            layout=self.vlayout
        )

        self.vlayout.addWidget(SeparateHLine())
    
    def find_obj(self):
        return find_mpl_object(
            source=self.canvas.fig,
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
            set_legend(self.canvas)
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
            if get_legend(self.canvas): set_legend(self.canvas)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)

    def set_clip(self, bool):
        for obj in self.find_obj():
            obj.set_clip_on(bool)
    
    def get_clip(self) -> bool:
        return self.find_obj()[0].get_clip_on()

    def get_zorder(self) -> int:
        return int(self.find_obj()[0].get_zorder())
    
    def set_zorder(self, value:float):
        for obj in self.find_obj():
            obj.set_zorder(value)
            value += 1