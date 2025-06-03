from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import Toggle
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Wedge, MultiWedges
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import patches
from typing import List

DEBUG = False

class Pie (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):   
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Pie'))
        layout.addWidget(SeparateHLine())

        self.explode = LineEdit(text="Explode")
        self.explode.button.setText(self.get_explode())
        self.explode.button.textChanged.connect(self.set_explode)
        layout.addWidget(self.explode)

        self.labels = LineEdit(text="Labels")
        self.labels.button.setText(self.get_labels())
        self.labels.button.textChanged.connect(self.set_labels)
        layout.addWidget(self.labels)

        self.startangle = DoubleSpinBox(
            min  = 0,
            max  = 360, 
            step = 30,
            text = "Start angle"
        )
        self.startangle.button.setValue(self.get_startangle())
        self.startangle.button.valueChanged.connect(self.set_startangle)
        layout.addWidget(self.startangle)

        self.radius = DoubleSpinBox(
            text = "Radius",
            step = 0.2
        )
        self.radius.button.setValue(self.get_radius())
        self.radius.button.valueChanged.connect(self.set_radius)
        layout.addWidget(self.radius)

        self.counterclock = Toggle(text="Counterclock")
        self.counterclock.button.setChecked(self.get_counterclock())
        self.counterclock.button.checkedChanged.connect(self.set_counterclock)
        layout.addWidget(self.counterclock)

        self.rotatelabels = Toggle(text="Rotate Labels")
        self.rotatelabels.button.setChecked(self.get_rotatelabels())
        self.rotatelabels.button.checkedChanged.connect(self.set_rotatelabels)
        layout.addWidget(self.rotatelabels)

        self.normalize = Toggle(text="Normalize")
        self.normalize.button.setChecked(self.get_normalize())
        self.normalize.button.checkedChanged.connect(self.set_normalize)
        layout.addWidget(self.normalize)

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self.onChanged.emit)
        layout.addWidget(wedge)
    
    def find_object (self) -> List[patches.Wedge]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Wedge],
            gid=self.gid
        )

    def set_explode(self, value:str) -> None:
        try:
            if value == "": value = None
            else: value = [float(i) for i in value.split(",")]
            self.props.update(explode = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_explode(self) -> str:
        if not self.find_object()[0].explode:
            return str()
        else: return str(self.find_object()[0].explode)
    
    def set_labels(self, value:str) -> None:
        try:
            if value == "": value = None
            else: value = value.split(",")
            self.props.update(labels = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_labels(self) -> str:
        if not self.find_object()[0].labels:
            return str()
        else: return str(self.find_object()[0].labels)
    
    def set_startangle(self, value:float) -> None:
        try:
            self.props.update(startangle = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_startangle(self) -> float:
        return float(self.find_object()[0].startangle)
    
    def set_radius(self, value:float) -> None:
        try:
            self.props.update(radius = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_radius(self) -> float:
        return float(self.find_object()[0].r)
    
    def set_counterclock(self, value:bool) -> None:
        try:
            self.props.update(counterclock = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_counterclock(self) -> bool:
        return self.find_object()[0].counterclock

    def set_rotatelabels(self, value:bool) -> None:
        try:
            self.props.update(rotatelabels = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rotatelabels(self) -> bool:
        return self.find_object()[0].rotatelabels
    
    def set_normalize(self, value:bool) -> None:
        try:
            self.props.update(normalize = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_normalize(self) -> bool:
        return self.find_object()[0].normalize

class Coxcomb (Pie):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):   

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Coxcomb'))
        layout.addWidget(SeparateHLine())

        self.explode = LineEdit(text="Explode")
        self.explode.button.setText(self.get_explode())
        self.explode.button.textChanged.connect(self.set_explode)
        layout.addWidget(self.explode)

        self.labels = LineEdit(text="Labels")
        self.labels.button.setText(self.get_labels())
        self.labels.button.textChanged.connect(self.set_labels)
        layout.addWidget(self.labels)

        self.startangle = DoubleSpinBox(
            min  = 0,
            max  = 360, 
            step = 30,
            text = "Start angle"
        )
        self.startangle.button.setValue(self.get_startangle())
        self.startangle.button.valueChanged.connect(self.set_startangle)
        layout.addWidget(self.startangle)

        self.radius = DoubleSpinBox(text="Radius",step=0.2)
        self.radius.button.setValue(self.get_radius())
        self.radius.button.valueChanged.connect(self.set_radius)
        layout.addWidget(self.radius)

        self.counterclock = Toggle(text="Counterclock")
        self.counterclock.button.setChecked(self.get_counterclock())
        self.counterclock.button.checkedChanged.connect(self.set_counterclock)
        layout.addWidget(self.counterclock)

        self.rotatelabels = Toggle(text="Rotate Labels")
        self.rotatelabels.button.setChecked(self.get_rotatelabels())
        self.rotatelabels.button.checkedChanged.connect(self.set_rotatelabels)
        layout.addWidget(self.rotatelabels)

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self.onChanged.emit)
        layout.addWidget(wedge)

class Doughnut (Pie):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Doughnut'))
        layout.addWidget(SeparateHLine())

        self.wedgewidth = DoubleSpinBox(
            min  = 0,
            max  = 1, 
            step = 0.1,
            text = "Width"
        )
        self.wedgewidth.button.setValue(self.get_wedgewidth())
        self.wedgewidth.button.valueChanged.connect(self.set_wedgewidth)
        layout.addWidget(self.wedgewidth)

        self.explode = LineEdit(text="Explode")
        self.explode.button.setText(self.get_explode())
        self.explode.button.textChanged.connect(self.set_explode)
        layout.addWidget(self.explode)

        self.labels = LineEdit(text="Labels")
        self.labels.button.setText(self.get_labels())
        self.labels.button.textChanged.connect(self.set_labels)
        layout.addWidget(self.labels)

        self.startangle = DoubleSpinBox(
            min  = 0,
            max  = 360, 
            step = 30,
            text = "Start angle"
        )
        self.startangle.button.setValue(self.get_startangle())
        self.startangle.button.valueChanged.connect(self.set_startangle)
        layout.addWidget(self.startangle)

        self.radius = DoubleSpinBox(
            text = "Radius",
            step = 0.2
        )
        self.radius.button.setValue(self.get_radius())
        self.radius.button.valueChanged.connect(self.set_radius)
        layout.addWidget(self.radius)

        self.counterclock = Toggle(text="Counterclock")
        self.counterclock.button.setChecked(self.get_counterclock())
        self.counterclock.button.checkedChanged.connect(self.set_counterclock)
        layout.addWidget(self.counterclock)

        self.rotatelabels = Toggle(text="Rotate Labels")
        self.rotatelabels.button.setChecked(self.get_rotatelabels())
        self.rotatelabels.button.checkedChanged.connect(self.set_rotatelabels)
        layout.addWidget(self.rotatelabels)

        self.normalize = Toggle(text="Normalize")
        self.normalize.button.setChecked(self.get_normalize())
        self.normalize.button.checkedChanged.connect(self.set_normalize)
        layout.addWidget(self.normalize)

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self.onChanged.emit)
        layout.addWidget(wedge)
    
    def set_wedgewidth(self, value:float):
        try:
            self.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_wedgewidth(self) -> float:
        return self.find_object()[0].width

class SemicircleDoughnut (Doughnut):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Semicircle Doughnut'))
        layout.addWidget(SeparateHLine())

        self.explode = LineEdit(text="Explode")
        self.explode.button.setText(self.get_explode())
        self.explode.button.textChanged.connect(self.set_explode)
        layout.addWidget(self.explode)

        self.labels = LineEdit(text="Labels")
        self.labels.button.setText(self.get_labels())
        self.labels.button.textChanged.connect(self.set_labels)
        layout.addWidget(self.labels)

        self.radius = DoubleSpinBox(
            text = "Radius",
            step = 0.2
        )
        self.radius.button.setValue(self.get_radius())
        self.radius.button.valueChanged.connect(self.set_radius)
        layout.addWidget(self.radius)

        self.startangle = DoubleSpinBox(
            min  = 0,
            max  = 360, 
            step = 30,
            text = "Start angle"
        )
        self.startangle.button.setValue(self.get_startangle())
        self.startangle.button.valueChanged.connect(self.set_startangle)
        layout.addWidget(self.startangle)

        self.counterclock = Toggle(text="Counterclock")
        self.counterclock.button.setChecked(self.get_counterclock())
        self.counterclock.button.checkedChanged.connect(self.set_counterclock)
        layout.addWidget(self.counterclock)

        self.rotatelabels = Toggle(text="Rotate Labels")
        self.rotatelabels.button.setChecked(self.get_rotatelabels())
        self.rotatelabels.button.checkedChanged.connect(self.set_rotatelabels)
        layout.addWidget(self.rotatelabels)

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self.onChanged.emit)
        layout.addWidget(wedge)
    
class MultilevelDoughnut (Doughnut):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Multilevel Doughnut'))
        layout.addWidget(SeparateHLine())

        self.wedgewidth = DoubleSpinBox(
            min  = 0,
            max  = 1, 
            step = 0.1,
            text = "Width"
        )
        self.wedgewidth.button.setValue(self.get_wedgewidth())
        self.wedgewidth.button.valueChanged.connect(self.set_wedgewidth)
        layout.addWidget(self.wedgewidth)

        self.explode = LineEdit(text="Explode")
        self.explode.button.setText(self.get_explode())
        self.explode.button.textChanged.connect(self.set_explode)
        layout.addWidget(self.explode)

        self.labels = LineEdit(text="Labels")
        self.labels.button.setText(self.get_labels())
        self.labels.button.textChanged.connect(self.set_labels)
        layout.addWidget(self.labels)

        self.startangle = DoubleSpinBox(
            min  = 0,
            max  = 360, 
            step = 30,
            text = "Start angle"
        )
        self.startangle.button.setValue(self.get_startangle())
        self.startangle.button.valueChanged.connect(self.set_startangle)
        layout.addWidget(self.startangle)

        self.radius = DoubleSpinBox(
            text = "Radius",
            step = 0.2
        )
        self.radius.button.setValue(self.get_radius())
        self.radius.button.valueChanged.connect(self.set_radius)
        layout.addWidget(self.radius)

        self.counterclock = Toggle(text="Counterclock")
        self.counterclock.button.setChecked(self.get_counterclock())
        self.counterclock.button.checkedChanged.connect(self.set_counterclock)
        layout.addWidget(self.counterclock)

        self.rotatelabels = Toggle(text="Rotate Labels")
        self.rotatelabels.button.setChecked(self.get_rotatelabels())
        self.rotatelabels.button.checkedChanged.connect(self.set_rotatelabels)
        layout.addWidget(self.rotatelabels)

        self.normalize = Toggle(text="Normalize")
        self.normalize.button.setChecked(self.get_normalize())
        self.normalize.button.checkedChanged.connect(self.set_normalize)
        layout.addWidget(self.normalize)

        self.pad = DoubleSpinBox(
            min  = 0,
            max  = 1,
            step = 0.01,
            text = "Padding"
        )
        self.pad.button.setValue(self.get_pad())
        self.pad.button.valueChanged.connect(self.set_pad)
        layout.addWidget(self.pad)
        
        mw = MultiWedges(self.gid, self.canvas)
        mw.onChanged.connect(self.onChanged.emit)
        layout.addWidget(mw)
    
    def set_pad(self, pad:float):
        try:
            self.props.update(pad=pad)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_pad(self) -> float:
        return self.find_object()[0].pad