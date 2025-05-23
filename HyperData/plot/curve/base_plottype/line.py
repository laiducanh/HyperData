from plot.curve.base_elements import line
from ui.base_widgets.button import Toggle, ComboBox, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.list import TreeWidget, TreeWidgetItem
from matplotlib.collections import Collection
from matplotlib import lines, collections
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import SingleColorCollection
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Line (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)

        line2d = TreeWidgetItem(self.treeview)
        self.treeview.addTopLevelItem(line2d)
        line2d.setText(0, 'Line')
        line.Line(gid, canvas, treeview, line2d)
        marker = TreeWidgetItem(self.treeview)
        marker.setText(0, 'Marker')
        line.Marker(gid, canvas, treeview, marker)

class Step (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)
        
        step = TreeWidgetItem(self.treeview)
        step.setText(0, 'Step')

        self.where = ComboBox(items=['pre', 'post', 'mid'], text="Where")
        self.where.button.setCurrentText(self.get_where())
        self.where.button.currentTextChanged.connect(self.set_where)
        self.treeview.addItemWidget(step, 0, self.where)
        line.Line(gid, canvas, treeview, step)

        marker = TreeWidgetItem(self.treeview)
        marker.setText(0, 'Marker')
        line.Marker(gid, canvas, treeview, marker)
    
    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D],
            gid=self.gid,
        )

    def set_where (self, value:str):
        try:
            self.props.update(where = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_where (self) -> str:
        return self.find_object()[0].where

class Stem (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)

        self.initUI()

    def initUI(self):

        stem = TreeWidgetItem(self.treeview)
        stem.setText(0, 'Stemline')

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self.treeview.addItemWidget(stem, 0, self.orientation)
        line.LineCollection(f"{self.gid}/stemlines", self.canvas, self.treeview, stem)
        line.Marker(f"{self.gid}/markerline", self.canvas, self.treeview, stem)

        baseline = TreeWidgetItem(self.treeview)
        baseline.setText(0, 'Baseline')

        self.bottom = DoubleSpinBox(text="Bottom")
        self.bottom.button.setValue(self.get_bottom())
        self.bottom.button.valueChanged.connect(self.set_bottom)
        self.treeview.addItemWidget(baseline, 0, self.bottom)
        line.Line(f"{self.gid}/baseline", self.canvas, self.treeview, baseline)
    
    def find_object(self):
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D, collections.LineCollection],
            gid=self.gid
        )

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation
    
    def set_bottom(self, value:float):
        try:
            self.props.update(bottom = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom(self) -> float:
        return self.find_object()[0].bottom

class Stem3d (Stem):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)
    
        self.props.update(orientation = "z")
        self.orientation.button.blockSignals(True)
        self.orientation.button.clear()
        self.orientation.button.addItems(["x","y","z"])
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.blockSignals(False)

class Area (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)

        self.initUI()

    def initUI(self):
        area = TreeWidgetItem(self.treeview)
        area.setText(0, 'Area')

        self.step = ComboBox(text='Step',items=['pre','post','mid','none'])
        self.step.button.setCurrentText(self.get_step())
        self.step.button.currentTextChanged.connect(self.set_step)
        self.treeview.addItemWidget(area, 0, self.step)

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self.treeview.addItemWidget(area, 0, self.orientation)

        SingleColorCollection(self.gid, self.canvas, self.treeview, area)

    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Collection],
            gid=self.gid
        )
    
    def set_step(self, value:str):
        try:
            self.props.update(step = value.lower())
            if value == "none": self.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        return self.find_obj()[0].step

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_obj()[0].orientation
    
class StackedArea (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)

        self.initUI()

    def initUI(self):

        area = TreeWidgetItem(self.treeview)
        area.setText(0, 'Area')

        self.baseline = ComboBox(text='Baseline',items=['zero','sym','wiggle','weighted_wiggle'])
        self.baseline.button.setCurrentText(self.get_baseline())
        self.baseline.button.currentTextChanged.connect(self.set_baseline)
        self.treeview.addItemWidget(area, 0, self.baseline)

        self.step = ComboBox(text='Step',items=['pre','post','mid','none'])
        self.step.button.setCurrentText(self.get_step())
        self.step.button.currentTextChanged.connect(self.set_step)
        self.treeview.addItemWidget(area, 0, self.step)

        SingleColorCollection(self.gid, self.canvas, self.treeview, area)
    
    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Collection],
            gid=self.gid
        )
    
    def set_step(self, value:str):
        try:
            self.props.update(step = value.lower())
            if value == "none": self.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        return self.find_obj()[0].step

    def set_baseline(self, value:str):
        try:
            self.props.update(baseline = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_baseline(self) -> str:
        return self.find_obj()[0].baseline

class StackedArea100 (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(gid, canvas, plot, treeview)

        self.initUI()

    def initUI(self):

        area = TreeWidgetItem(self.treeview)
        area.setText(0, 'Area')

        SingleColorCollection(self.gid, self.canvas, self.treeview, area)