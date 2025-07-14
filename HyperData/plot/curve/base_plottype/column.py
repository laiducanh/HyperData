from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from plot.curve.base_elements.collection import Poly3DCollection
from plot.curve.base_elements.line import Marker, Line, LineCollection
from plot.utilis import find_mpl_object
from plot.curve.base_plottype.base import PlotConfigBase
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import patches, colors, lines
from matplotlib.pyplot import colormaps
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as Poly3D
import numpy as np

DEBUG = False

class Column(PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        self.segment.addButton(text='Column', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Connecting lines', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label  = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.bottom = HLineEdit(
            label="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        self.barwidth = HTransparentDoubleSpinBox(
            label = 'Column Width',
            minimum = 0, maximum = 5, singleStep = 0.1,
            getter=self.get_barwidth,
            setter=self.set_barwidth,
            layout=self.general.addlayout
        )

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(rect)
        
        collection = LineCollection(f"_{self.gid.split('.')[0]}", self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)
        
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[patches.Rectangle],
            gid=self.gid
        )

    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
            self.plot.progressbar.changeColor()
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
    def set_bottom (self, value:str):
        try:
            self.plot.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.plot.props["bottom"])

    def set_barwidth (self, value:float):
        try: 
            self.plot.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.plot.props["width"]

class Column3D(PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Column', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["x","y","z"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.bottom = HLineEdit(
            label="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        self.dx = HTransparentDoubleSpinBox(
            label = 'Dx',
            minimum = 0, maximum = 5, singleStep = 0.1,
            getter=self.get_dx,
            setter=self.set_dx,
            layout=self.general.addlayout
        )

        self.dy = HTransparentDoubleSpinBox(
            label = "Dy",
            minimum = 0, maximum = 5, singleStep = 0.1,
            getter=self.get_dy,
            setter=self.set_dy,
            layout=self.general.addlayout
        )

        self.color = HColorDropdown(
            label = "Color", 
            getter=self.get_color,
            setter=self.set_color,
            layout=self.general.addlayout
        )

        self.shade = HToggle(
            label="Shade",
            getter=self.get_shade,
            setter=self.set_shade,
            layout=self.general.addlayout
        ) 

        collection = Poly3DCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)
    
    def find_object (self) -> list[Poly3D]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[Poly3D],
            gid=self.gid
        )
        
    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.plot.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.plot.props["bottom"])

    def set_dx (self, value:float):
        try: 
            self.plot.props.update(Dx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dx (self) -> float:
        return self.plot.props["Dx"]
    
    def set_dy(self, value:float):
        try:
            self.plot.props.update(Dy = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dy(self) -> float:
        return self.plot.props["Dy"]
    
    def set_color(self, value:str):
        try:
            self.plot.props.update(color = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_color(self) -> str:
        _color = self.plot.props["color"]
        if not _color:
            color = np.max(self.find_object()[0].get_facecolor(),axis=0)
            return colors.to_hex(color)
        return _color
    
    def set_shade(self, value:bool):
        try:
            self.plot.props.update(shade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_shade(self) -> bool:
        return self.plot.props["shade"]
    
class Dot(PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.bottom = HLineEdit(
            label="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        marker = Marker(self.gid, self.canvas)
        marker.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(marker)

        alpha = HTransparentSpinBox(
            label = 'Transparent',
            singleStep = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=marker.vlayout
        )

    def find_object(self):
        return find_mpl_object(
            self.canvas.figure,
            [lines.Line2D],
            gid=self.gid
        )
    
    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.plot.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.plot.props["bottom"])
    
    def set_alpha(self, value:int):
        for obj in self.find_object():
            obj.set_alpha(value/100)
        self._onChange()
        self.canvas.draw_idle()
    
    def get_alpha(self) -> int:
        if not self.find_object()[0].get_alpha():
            return 100
        return int(self.find_object()[0].get_alpha()*100)

class ClusteredColumn(Column):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):

        self.segment.addButton(text='Column', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.bottom = HLineEdit(
            label="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        self.barwidth = HTransparentDoubleSpinBox(
            label = 'Bar Width',
            minimum = 0, maximum = 5, singleStep = 0.1,
            getter=self.get_barwidth,
            setter=self.set_barwidth,
            layout=self.general.addlayout
        )

        self.distance = HTransparentSpinBox(
            minimum = 0, maximum = 100, singleStep = 10, 
            label = "Distance",
            getter=self.get_distance,
            setter=self.set_distance,
            layout=self.general.addlayout
        )

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(rect)
    
    def set_distance(self, value:int):
        try:
            self.plot.props.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.plot.props["distance"]*100)

class ClusteredDot(Dot):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.bottom = HLineEdit(
            label="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        self.distance = HTransparentSpinBox(
            minimum = 0, maximum = 100, singleStep = 10,
            label = "Distance",
            getter=self.get_distance,
            setter=self.set_distance,
            layout=self.general.addlayout
        )

        marker = Marker(self.gid, self.canvas)
        marker.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(marker)

        alpha = HTransparentSpinBox(
            label = 'Transparent',
            singleStep = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=marker.vlayout
        )
    
    def set_distance(self, value:int):
        try:
            self.plot.props.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.plot.props["distance"]*100)

class Dumbbell(PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
        if "." in gid:
            self.gid = gid.split(".")[0]
        else: self.gid = gid
    
        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Head 1', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.addButton(text='Head 2', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment.setCurrentIndex(0)
        self.segment.setCurrentIndex(0)
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        line = Line(f"{self.gid}/0", self.canvas)
        line.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(line)

        head1 = Marker(f"_{self.gid}/1", self.canvas)
        head1.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(head1)

        head2 = Marker(f"_{self.gid}/2", self.canvas)
        head2.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(head2)

    def find_object(self):
        return find_mpl_object(self.canvas.figure, [lines.Line2D], self.gid)

    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]

class Marimekko(PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Column', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(rect)
        
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[patches.Rectangle],
            gid=self.gid
        )
    
    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_orientation(self) -> str:
        return self.plot.props["orientation"]

class Treemap (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        self.segment.addButton(text='Column', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.rounded = HTransparentDoubleSpinBox(
            label="Rounding factor",
            getter=self.get_rounded,
            setter=self.set_rounded,
            layout=self.general.addlayout
        )

        self.pad = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 20, singleStep = 0.5,
            label = "Padding",
            getter=self.get_pad,
            setter=self.set_pad,
            layout=self.general.addlayout
        )

        self.cmap_on = HToggle(
            label="Use colormap",
            getter=self.get_cmap_on,
            setter=self.set_cmap_on,
            layout=self.general.addlayout
        )

        self.cmap = HTransparentComboBox(
            items = colormaps(), 
            label = "Colormap",
            getter=self.get_cmap,
            setter=self.set_cmap,
            layout=self.general.addlayout
        )

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(rect)
    
    def find_object(self) -> list[patches.FancyBboxPatch]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[patches.FancyBboxPatch],
            gid=self.gid,
        )
    
    def set_rounded(self, value:float):
        try:
            self.plot.props.update(rounded=value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rounded(self) -> float:
        return self.plot.props["rounded"]
    
    def set_pad(self, value:float):
        try:
            self.plot.props.update(pad = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_pad(self) -> float:
        return float(self.plot.props["pad"])
    
    def set_cmap_on(self, value:bool):
        try:
            self.plot.props.update(cmap_on=value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cmap_on(self) -> bool:
        return self.plot.props["cmap_on"]
          
    def set_cmap(self, value:str):
        try:
            self.plot.props.update(cmap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_cmap(self) -> str:
        return self.plot.props["cmap"]

class WaterFall (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        self.segment.addButton(text='Positive Columns', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Negative Columns', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.addButton(text='Connecting lines', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment.setCurrentIndex(0)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.bottom = HLineEdit(
            label="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        self.barwidth = HTransparentDoubleSpinBox(
            label = 'Bar Width',
            minimum = 0, maximum = 5, singleStep = 0.1,
            getter=self.get_barwidth,
            setter=self.set_barwidth,
            layout=self.general.addlayout
        )

        pbars = Rectangle(f"{self.gid}/positive", self.canvas)
        pbars.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(pbars)

        nbars = Rectangle(f"{self.gid}/negative", self.canvas)
        nbars.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(nbars)

        cline = LineCollection(f"_{self.gid}/line", self.canvas)
        cline.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(cline)
    
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[patches.Rectangle],
            gid=self.gid
        )
    
    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
            self.plot.progressbar.changeColor()
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
    def set_bottom (self, value:str):
        try:
            self.plot.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.plot.props["bottom"])

    def set_barwidth (self, value:float):
        try: 
            self.plot.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.plot.props["width"]