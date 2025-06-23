from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QStackedLayout, QDialog
from plot.canvas import Canvas
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.button import TransparentComboBox, SegmentedWidget, Toggle
from ui.base_widgets.spinbox import TransparentDoubleSpinBox, TransparentSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.frame import ScrollArea
from plot.plotting.plotting import set_legend, get_legend
from config.settings import font_lib, logger
import matplotlib.pyplot as plt

DEBUG = False

class LegendBase(ScrollArea):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

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
        
        font = TransparentComboBox(
            items = font_lib,
            text  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=self.vlayout
        )

        size = TransparentDoubleSpinBox(
            text = 'Font size',
            min = 1, max = 100, step = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=self.vlayout
        )

        # # style = FontStyle(obj=self.obj.get_texts(), canvas=self.canvas)
        # # layout.addWidget(style)

        color = ColorDropdown(
            text  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        markerscale = TransparentDoubleSpinBox(
            text = 'Marker scale',
            min = 0, max = 5, step = 0.1,
            setter=self.set_markerscale,
            getter=self.get_markerscale,
            layout=self.vlayout
        )

        ncols = TransparentSpinBox(
            text = 'Number of columns',
            min = 1, max = 10, step = 1,
            setter=self.set_ncols,
            getter=self.get_ncols,
            layout=self.vlayout
        )

        npoints = TransparentSpinBox(
            text = "Marker points",
            min = 1, max = 10, step = 1,
            setter=self.set_npoints,
            getter=self.get_npoints,
            layout=self.vlayout
        )

        columnspacing = TransparentDoubleSpinBox(
            text="Column spacing",
            setter=self.set_columnspacing,
            getter=self.get_columnspacing,
            layout=self.vlayout
        )
    
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
    
    def get_npoints(self) -> int:
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

class LegendTitle(LegendBase):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(canvas, parent)

    def initUI(self):

        self.title = LineEdit(
            text='Label',
            setter=self.set_title,
            getter=self.get_title,
            layout=self.vlayout
        )
        self.title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        font = TransparentComboBox(
            items = font_lib,
            text  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=self.vlayout
        )

        size = TransparentDoubleSpinBox(
            text = 'Font size',
            min = 1, max = 100, step = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=self.vlayout
        )

        color = ColorDropdown(
            text  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.backgroundcolor = ColorDropdown(
            text  = 'Background color',
            getter=self.get_backgroundcolor,
            setter=self.set_backgroundcolor,
            layout=self.vlayout
        )

        edgecolor = ColorDropdown(
            text  = 'Edge color',
            getter = self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        align = TransparentComboBox(
            text  = "Alignment", 
            items = ["center","left","right"],
            setter=self.set_alignment,
            getter=self.get_alignment,
            layout=self.vlayout
        )
        
        # #pad = DoubleSpinBox(text='label pad',min=-100,max=100,step=5)
        # #pad.button.valueChanged.connect(lambda: self.sig.emit())
        # #layout.addWidget(pad)

        alpha = TransparentDoubleSpinBox(
            text = 'Transparency',
            step = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )

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

class LegendFrame(LegendBase):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(canvas, parent)
    
    def initUI(self):
    
        frameon = Toggle(
            text='Visible',
            setter=self.set_frameon,
            getter=self.get_frameon,
            layout=self.vlayout
        )

        shadow = Toggle(
            text='Shadow',
            setter=self.set_shadow,
            getter=self.get_shadow,
            layout=self.vlayout
        )

        facecolor = ColorDropdown(
            text  = 'Face Color', 
            getter=self.get_facecolor,
            setter=self.set_facecolor,
            layout=self.vlayout
        )

        edgecolor = ColorDropdown(
            text  = 'Edge Color', 
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=self.vlayout
        )

        alpha = TransparentDoubleSpinBox(
            text = 'Transparency',
            step = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )

        borderpad = TransparentDoubleSpinBox(
            text = 'Border pad',
            min = 0, max = 5, step = 0.1,
            setter=self.set_borderpad,
            getter=self.get_borderpad,
            layout=self.vlayout
        )

        handlelength = TransparentDoubleSpinBox(
            text = 'Handle length',
            min = 0, max = 10, step = 0.5,
            setter=self.set_handlelength,
            getter=self.get_handlelength,
            layout=self.vlayout
        )

        handleheight = TransparentDoubleSpinBox(
            text = 'Handle height',
            min = 0, max = 10, step = 0.5,
            setter=self.set_handleheight,
            getter=self.get_handleheight,
            layout=self.vlayout
        )

        handletextpad = TransparentDoubleSpinBox(
            text = 'Handle text pad',
            min = 0, max = 10, step = 0.5,
            setter=self.set_handletextpad,
            getter=self.get_handletextpad,
            layout=self.vlayout
        )
    
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
    
class LegendLabel(QDialog):
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