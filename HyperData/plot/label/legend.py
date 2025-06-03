from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QStackedLayout, QDialog
from plot.canvas import Canvas
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.button import ComboBox, SegmentedWidget, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.color import ColorDropdown
from plot.plotting.plotting import set_legend, get_legend
from config.settings import font_lib, logger
import matplotlib.pyplot as plt

DEBUG = False

class LegendBase (QWidget):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Legend settings')
        self.canvas = canvas
        self.find_legend()
        self.initUI()
    
    def initUI(self):
        pass

    def find_legend(self):
        self.legend = get_legend(self.canvas)
        if self.legend:
            self.handles = self.legend.legend_handles
            self.legend_text = self.legend.get_title()
        
    def showEvent(self, event):
        self.find_legend()
        #self.update()
        return super().showEvent(event)

class LegendEntries(LegendBase):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(canvas, parent)

    def initUI(self):

        layout = QVBoxLayout(self)
        
        font = ComboBox(
            items = font_lib,
            text  = 'Font'
        )
        font.button.currentTextChanged.connect(self.set_fontname)
        font.button.setCurrentText(self.get_fontname())
        layout.addWidget(font)

        size = DoubleSpinBox(
            text = 'Font size',
            min = 1, max = 100, step = 1
        )
        size.button.valueChanged.connect(self.set_fontsize)
        size.button.setValue(self.get_fontsize())
        layout.addWidget(size)

        # # style = FontStyle(obj=self.obj.get_texts(), canvas=self.canvas)
        # # layout.addWidget(style)

        color = ColorDropdown(
            text  = 'Font color',
            color = self.get_color()
        )
        color.button.colorChanged.connect(self.set_color)
        layout.addWidget(color)

        markerscale = DoubleSpinBox(
            text = 'Marker scale',
            min = 0, max = 5, step = 0.1
        )
        markerscale.button.valueChanged.connect(self.set_markerscale)
        markerscale.button.setValue(self.get_markerscale())
        layout.addWidget(markerscale)

        ncols = SpinBox(
            text = 'Number of columns',
            min = 1, max = 10, step = 1
        )
        ncols.button.valueChanged.connect(self.set_ncols)
        ncols.button.setValue(self.get_ncols())
        layout.addWidget(ncols)

        npoints = SpinBox(
            text = "Marker points",
            min = 1, max = 10, step = 1
        )
        npoints.button.valueChanged.connect(self.set_npoints)
        npoints.button.setValue(self.get_npoins())
        layout.addWidget(npoints)

        columnspacing = DoubleSpinBox(text="Column spacing")
        columnspacing.button.valueChanged.connect(self.set_columnspacing)
        columnspacing.button.setValue(self.get_columnspacing())
        layout.addWidget(columnspacing)
    
    def set_fontname (self, font:str):
        if self.legend:
            try:
                plt.rcParams["font.family"] = font
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()
    
    def get_fontname(self) -> str:
        if self.legend: return self.legend_text.get_fontname()
        return plt.rcParams["font.family"][0]
    
    def set_fontsize(self, value:float):
        if self.legend:
            try:
                plt.rcParams["font.size"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()
    
    def get_fontsize(self):
        if self.legend: return self.legend_text.get_fontsize()
        return plt.rcParams["font.size"]
    
    def set_color (self, color):
        if self.legend:
            try:
                plt.rcParams["legend.labelcolor"] = color 
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()
    
    def get_color (self):
        return plt.rcParams["legend.labelcolor"]
    
    def set_markerscale(self, value:float):
        if self.legend:
            try:
                plt.rcParams["legend.markerscale"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()

    def get_markerscale(self) -> float:
        return plt.rcParams["legend.markerscale"]
    
    def set_ncols(self, value:int):
        if self.legend:
            try:
                self.legend.set_ncols(value)
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()
    
    def get_ncols(self) -> int:
        if self.legend: return self.legend._ncols
        return 1
    
    def set_npoints(self, value:int):
        if self.legend:
            try:
                plt.rcParams["legend.numpoints"] = value
                plt.rcParams["legend.scatterpoints"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()
    
    def get_npoins(self) -> int:
        return plt.rcParams["legend.numpoints"]

    def set_columnspacing(self, value:float):
        if self.legend:
            try:
                plt.rcParams["legend.columnspacing"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
            self.canvas.draw_idle()
    
    def get_columnspacing(self) -> float:
        return plt.rcParams["legend.columnspacing"]

class LegendTitle (LegendBase):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(canvas, parent)

    def initUI(self):

        layout = QVBoxLayout(self)

        self.title = LineEdit(text='Label')
        self.title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.title.button.textChanged.connect(self.set_title)
        self.title.setText(self.get_title())
        layout.addWidget(self.title)

        font = ComboBox(
            items = font_lib,
            text  = 'Font'
        )
        font.button.currentTextChanged.connect(self.set_fontname)
        font.button.setCurrentText(self.get_fontname())
        layout.addWidget(font)

        size = DoubleSpinBox(
            text = 'Font size',
            min = 1, max = 100, step = 1
        )
        size.button.valueChanged.connect(self.set_fontsize)
        size.button.setValue(self.get_fontsize())
        layout.addWidget(size)

        color = ColorDropdown(
            text  = 'Font color',
            color = self.get_color()
        )
        color.button.colorChanged.connect(self.set_color)
        layout.addWidget(color)

        self.backgroundcolor = ColorDropdown(
            text  = 'Background color',
            color = self.get_backgroundcolor()
        )
        self.backgroundcolor.button.colorChanged.connect(self.set_backgroundcolor)
        layout.addWidget(self.backgroundcolor)

        edgecolor = ColorDropdown(
            text  = 'Edge color',
            color = self.get_edgecolor()
        )
        edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(edgecolor)

        align = ComboBox(
            text  = "Alignment", 
            items = ["center","left","right"]
        )
        align.button.currentTextChanged.connect(self.set_alignment)
        align.button.setCurrentText(self.get_alignment())
        layout.addWidget(align)
        
        # #pad = DoubleSpinBox(text='label pad',min=-100,max=100,step=5)
        # #pad.button.valueChanged.connect(lambda: self.sig.emit())
        # #layout.addWidget(pad)

        alpha = DoubleSpinBox(
            text = 'transparency',
            step = 10
        )
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)

    def set_title (self, label:str):
        if self.legend:
            try:
                self.legend.set_title(label)
            except Exception as e:
                logger.exception(e)
        self.canvas.draw_idle()
    
    def get_title(self):
        if self.legend: return self.legend_text.get_text()

    def set_fontname (self, font:str):
        if self.legend:
            self.legend_text.set_fontname(font.lower())
        self.canvas.draw_idle()
    
    def get_fontname(self):
        if self.legend: return self.legend_text.get_fontname()
        return plt.rcParams["font.family"][0]

    def set_fontsize(self, value):
        if self.legend: self.legend_text.set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        if self.legend: return self.legend_text.get_fontsize()
        return plt.rcParams["font.size"]

    def set_color (self, color):
        if self.legend: self.legend_text.set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        if self.legend: return self.legend_text.get_color()
        return plt.rcParams["legend.labelcolor"]

    def set_backgroundcolor (self, color):
        if self.legend: self.legend_text.set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.legend: 
            if self.legend_text.get_bbox_patch():
                return self.legend_text.get_bbox_patch().get_facecolor()
        return 'white'

    def set_edgecolor (self, color):
        if self.legend:
            self.legend_text.set_bbox({"edgecolor":color,
                                "facecolor":self.backgroundcolor.button.color.name()})
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.legend:
            if self.legend_text.get_bbox_patch():
                return self.legend_text.get_bbox_patch().get_edgecolor()
        return 'white'
    
    def set_alignment(self, value:str):
        if self.legend:
            try:
                self.legend.set_alignment(value)
            except Exception as e:
                logger.exception(e)
        self.canvas.draw_idle()
    
    def get_alignment(self) -> str:
        if self.legend: return self.legend.get_alignment()
        return "center"

    def set_pad (self, value):
        pass

    def get_pad (self):
        pass

    def set_alpha (self, value):
        if self.legend:
            self.legend_text.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.legend:
            if self.legend_text.get_alpha():
                return int(self.legend_text.get_alpha()*100)
        return 100

class LegendFrame (LegendBase):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(canvas, parent)
    
    def initUI(self):

        layout = QVBoxLayout(self)
    
        frameon = Toggle(text='Visible')
        frameon.button.checkedChanged.connect(self.set_frameon)
        frameon.button.setChecked(self.get_frameon())
        layout.addWidget(frameon)

        shadow = Toggle(text='Shadow')
        shadow.button.checkedChanged.connect(self.set_shadow)
        shadow.button.setChecked(self.get_shadow())
        layout.addWidget(shadow)

        facecolor = ColorDropdown(
            text  = 'Face Color', 
            color = self.get_facecolor()
        )
        facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(facecolor)

        edgecolor = ColorDropdown(
            text  = 'Edge Color', 
            color = self.get_edgecolor()
        )
        edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(edgecolor)

        alpha = DoubleSpinBox(
            text = 'Transparency',
            step = 10
        )
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)

        borderpad = DoubleSpinBox(
            text = 'border pad',
            min = 0, max = 5, step = 0.1
        )
        borderpad.button.valueChanged.connect(self.set_borderpad)
        borderpad.button.setValue(self.get_borderpad())
        layout.addWidget(borderpad)

        handlelength = DoubleSpinBox(
            text = 'handle length',
            min = 0, max = 10, step = 0.5
        )
        handlelength.button.valueChanged.connect(self.set_handlelength)
        handlelength.button.setValue(self.get_handlelength())
        layout.addWidget(handlelength)

        handleheight = DoubleSpinBox(
            text = 'handle height',
            min = 0, max = 10, step = 0.5
        )
        handleheight.button.valueChanged.connect(self.set_handleheight)
        handleheight.button.setValue(self.get_handleheight())
        layout.addWidget(handleheight)

        handletextpad = DoubleSpinBox(
            text = 'handle text pad',
            min = 0, max = 10, step = 0.5
        )
        handletextpad.button.valueChanged.connect(self.set_handletextpad)
        handletextpad.button.setValue(self.get_handletextpad())
        layout.addWidget(handletextpad)
    
    def set_frameon(self, value:bool):
        if self.legend:
            try:
                plt.rcParams["legend.frameon"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
        
    def get_frameon(self) -> bool:
        return plt.rcParams["legend.frameon"]

    def set_shadow(self, value:bool):
        if self.legend:
            try:
                plt.rcParams["legend.shadow"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
    
    def get_shadow(self) -> bool:
        return plt.rcParams["legend.shadow"]

    def set_facecolor(self, color):
        if self.legend:
            try:
                plt.rcParams["legend.facecolor"] = color
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
        
    def get_facecolor(self):
        return plt.rcParams["legend.facecolor"]

    def set_edgecolor(self, color):
        if self.legend:
            try:
                plt.rcParams["legend.edgecolor"] = color
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
    
    def get_edgecolor(self):
        return plt.rcParams["legend.edgecolor"]

    def set_alpha(self, value):
        if self.legend:
            try:
                plt.rcParams["legend.framealpha"] = value/100
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)

    def get_alpha(self):
        return int(plt.rcParams["legend.framealpha"]*100)

    def set_borderpad(self, value:float):
        if self.legend:
            try:
                plt.rcParams["legend.borderpad"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
    
    def get_borderpad(self) -> float:
        return plt.rcParams["legend.borderpad"]
    
    def set_handlelength(self, value:float):
        if self.legend:
            try:
                plt.rcParams["legend.handlelength"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
    
    def get_handlelength(self) -> float:
        return plt.rcParams["legend.handlelength"]
    
    def set_handleheight(self, value:float):
        if self.legend:
            try:
                plt.rcParams["legend.handleheight"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
    
    def get_handleheight(self) -> float:
        return plt.rcParams["legend.handleheight"]
    
    def set_handletextpad(self, value:float):
        if self.legend:
            try:
                plt.rcParams["legend.handletextpad"] = value
            except Exception as e:
                logger.exception(e)
            set_legend(self.canvas)
    
    def get_handletextpad(self) -> float:
        return plt.rcParams["legend.handletextpad"]
    
class LegendLabel (QDialog):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.canvas = canvas
    
        choose_axis = SegmentedWidget()
        layout.addWidget(choose_axis)

        choose_axis.addButton(text='Entries', func=lambda: self.stackedlayout.setCurrentIndex(0))
        choose_axis.addButton(text='Title', func=lambda: self.stackedlayout.setCurrentIndex(1))
        choose_axis.addButton(text='Frame', func=lambda: self.stackedlayout.setCurrentIndex(2))
        #choose_axis.addButton(text='Colorbar', func=lambda: self.stackedlayout.setCurrentIndex(3))

        choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        self.entries = LegendEntries(canvas, parent)
        self.stackedlayout.addWidget(self.entries)
        self.title = LegendTitle(canvas, parent)
        self.stackedlayout.addWidget(self.title)
        self.frame = LegendFrame(canvas, parent)
        self.stackedlayout.addWidget(self.frame)