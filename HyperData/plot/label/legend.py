from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QStackedLayout, QDialog
from plot.canvas import Canvas
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.button import HTransparentComboBox, SegmentedWidget, HToggle
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.frame import ScrollArea, VFrame, SeparateHLine
from plot.utilis import get_legend
from plot.copy_objects import update_legend
from config.settings import font_lib, logger, linestyle_lib
from matplotlib import rcParams, colors

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
        self.legend = get_legend(self.canvas.figure)
        if self.legend:
            self.handles = self.legend.legend_handles
            self.legend_title = self.legend.get_title()
            self.legend_texts = self.legend.get_texts()
    
    def paintEvent(self, arg__1):
        self.find_legend()
        return super().paintEvent(arg__1)

class LegendEntries(LegendBase):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(canvas, parent)

    def initUI(self):
        
        fr = VFrame(self.vlayout)

        font = HTransparentComboBox(
            items = font_lib,
            label  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=fr.vlayout
        )
        font.button.setMinimumWidth(300)

        size = HTransparentDoubleSpinBox(
            label = 'Font size',
            minimum = 1, maximum = 100, singleStep = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=fr.vlayout
        )

        # # style = FontStyle(obj=self.obj.get_texts(), canvas=self.canvas)
        # # layout.addWidget(style)

        color = HColorDropdown(
            label  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=fr.vlayout
        )

        fr = VFrame(self.vlayout)

        markerscale = HTransparentDoubleSpinBox(
            label = 'Marker Size',
            minimum = 0, maximum = 1000, singleStep = 5,
            setter=self.set_markerscale,
            getter=self.get_markerscale,
            layout=fr.vlayout
        )

        ncols = HTransparentSpinBox(
            label = 'Number of columns',
            minimum = 1, maximum = 10, singleStep = 1,
            setter=self.set_ncols,
            getter=self.get_ncols,
            layout=fr.vlayout
        )

        npoints = HTransparentSpinBox(
            label = "Marker points",
            minimum = 0, maximum = 10, singleStep = 1,
            setter=self.set_npoints,
            getter=self.get_npoints,
            layout=fr.vlayout
        )

        columnspacing = HTransparentDoubleSpinBox(
            label="Column spacing",
            setter=self.set_columnspacing,
            getter=self.get_columnspacing,
            layout=fr.vlayout
        )
    
    def set_fontname (self, font:str):
        if self.legend:
            try:
                for text in self.legend_texts:
                    text.set_fontname(font)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_fontname(self) -> str:
        if self.legend and self.legend_texts: 
            return self.legend_texts[0].get_fontname()
        return rcParams[f"font.{rcParams['font.family'][0]}"][0]
    
    def set_fontsize(self, value:float):
        if self.legend:
            try:
                for text in self.legend_texts:
                    text.set_fontsize(value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_fontsize(self):
        if self.legend and self.legend_texts: 
            return self.legend_texts[0].get_fontsize()
        return rcParams["font.size"]
    
    def set_color (self, color):
        if self.legend:
            try:
                for text in self.legend_texts:
                    text.set_color(color)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)            
    
    def get_color (self):
        if self.legend and self.legend_texts:   
            return self.legend_texts[0].get_color()
        return rcParams["legend.labelcolor"]
    
    def set_markerscale(self, value:float):
        if self.legend:
            try:
                for handle in self.handles:
                    handle.set_markersize(value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)            

    def get_markerscale(self) -> float:
        if self.legend:
            try: return self.handles[0].get_markersize()
            except: pass
        return rcParams["legend.markerscale"]
    
    def set_ncols(self, value:int):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, ncols=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_ncols(self) -> int:
        if self.legend: return self.legend._ncols
        return 1
    
    def set_npoints(self, value:int):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, numpoints=value, scatterpoints=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)            
    
    def get_npoints(self) -> int:
        if self.legend: return self.legend.numpoints
        return rcParams["legend.numpoints"]

    def set_columnspacing(self, value:float):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, columnspacing=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_columnspacing(self) -> float:
        if self.legend: return self.legend.columnspacing
        return rcParams["legend.columnspacing"]

class LegendTitle(LegendBase):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(canvas, parent)

    def initUI(self):

        self.title = HLineEdit(
            label='Label',
            setter=self.set_title,
            getter=self.get_title,
            layout=self.vlayout
        )
        self.title.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        self.vlayout.addWidget(SeparateHLine())

        fr = VFrame(self.vlayout)

        font = HTransparentComboBox(
            items = font_lib,
            label  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=fr.vlayout
        )
        font.button.setMinimumWidth(300)

        size = HTransparentDoubleSpinBox(
            label = 'Font size',
            minimum = 1, maximum = 100, singleStep = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=fr.vlayout
        )

        color = HColorDropdown(
            label  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=fr.vlayout
        )

        # self.backgroundcolor = ColorDropdown(
        #     text  = 'Background color',
        #     getter=self.get_backgroundcolor,
        #     setter=self.set_backgroundcolor,
        #     layout=self.vlayout
        # )

        # edgecolor = ColorDropdown(
        #     text  = 'Edge color',
        #     getter = self.get_edgecolor,
        #     setter=self.set_edgecolor,
        #     layout=self.vlayout
        # )

        align = HTransparentComboBox(
            label  = "Alignment", 
            items = ["center","left","right"],
            setter=self.set_alignment,
            getter=self.get_alignment,
            layout=fr.vlayout
        )
        
        # #pad = DoubleSpinBox(text='label pad',min=-100,max=100,step=5)
        # #pad.button.valueChanged.connect(lambda: self.sig.emit())
        # #layout.addWidget(pad)

        alpha = HTransparentSpinBox(
            label = 'Transparency',
            singleStep = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=fr.vlayout
        )

    def set_title (self, label:str):
        if self.legend:
            try:
                self.legend.set_title(label)
            except Exception as e:
                logger.exception(e)
        self.canvas.draw_idle()
    
    def get_title(self):
        if self.legend: return self.legend_title.get_text()

    def set_fontname (self, font:str):
        if self.legend:
            self.legend_title.set_fontname(font.lower())
        self.canvas.draw_idle()
    
    def get_fontname(self):
        if self.legend: return self.legend_title.get_fontname()
        return rcParams[f"font.{rcParams['font.family'][0]}"][0]

    def set_fontsize(self, value):
        if self.legend: self.legend_title.set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        if self.legend: return self.legend_title.get_fontsize()
        return rcParams["font.size"]

    def set_color (self, color):
        if self.legend: self.legend_title.set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        if self.legend: return self.legend_title.get_color()
        return rcParams["legend.labelcolor"]

    def set_backgroundcolor (self, color):
        if self.legend: self.legend_title.set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.legend: 
            if self.legend_title.get_bbox_patch():
                return self.legend_title.get_bbox_patch().get_facecolor()
        return 'white'

    def set_edgecolor (self, color):
        if self.legend:
            self.legend_title.set_bbox({"edgecolor":color,
                                "facecolor":self.backgroundcolor.button.color.name()})
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.legend:
            if self.legend_title.get_bbox_patch():
                return self.legend_title.get_bbox_patch().get_edgecolor()
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
            self.legend_title.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.legend:
            if self.legend_title.get_alpha():
                return int(self.legend_title.get_alpha()*100)
        return 100

class LegendFrame(LegendBase):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(canvas, parent)
    
    def initUI(self):
        
        fr = VFrame(self.vlayout)

        frameon = HToggle(
            label='Visible',
            setter=self.set_frameon,
            getter=self.get_frameon,
            layout=fr.vlayout
        )

        shadow = HToggle(
            label='Shadow',
            setter=self.set_shadow,
            getter=self.get_shadow,
            layout=fr.vlayout
        )

        fr = VFrame(self.vlayout)

        facecolor = HColorDropdown(
            label  = 'Face Color', 
            getter=self.get_facecolor,
            setter=self.set_facecolor,
            layout=fr.vlayout
        )

        edgecolor = HColorDropdown(
            label  = 'Edge Color', 
            getter=self.get_edgecolor,
            setter=self.set_edgecolor,
            layout=fr.vlayout
        )

        edgestyle = HTransparentComboBox(
            label  = 'Edge Style',
            items = linestyle_lib.values(),
            getter=self.get_edgestyle,
            setter=self.set_edgestyle,
            layout=fr.vlayout
        )

        edgewidth = HTransparentDoubleSpinBox(
            label = 'Edge Width',
            minimum = 0, maximum = 5, singleStep = 0.1,
            getter=self.get_edgewidth,
            setter=self.set_edgewidth,
            layout=fr.vlayout
        )

        alpha = HTransparentSpinBox(
            label = 'Transparency',
            singleStep = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=fr.vlayout
        )

        fr = VFrame(self.vlayout)

        borderpad = HTransparentDoubleSpinBox(
            label = 'Border pad',
            minimum = 0, maximum = 5, singleStep = 0.1,
            setter=self.set_borderpad,
            getter=self.get_borderpad,
            layout=fr.vlayout
        )

        handlelength = HTransparentDoubleSpinBox(
            label = 'Handle length',
            minimum = 0, maximum = 10, singleStep = 0.5,
            setter=self.set_handlelength,
            getter=self.get_handlelength,
            layout=fr.vlayout
        )

        handleheight = HTransparentDoubleSpinBox(
            label = 'Handle height',
            minimum = 0, maximum = 10, singleStep = 0.5,
            setter=self.set_handleheight,
            getter=self.get_handleheight,
            layout=fr.vlayout
        )

        handletextpad = HTransparentDoubleSpinBox(
            label = 'Handle text pad',
            minimum = 0, maximum = 10, singleStep = 0.5,
            setter=self.set_handletextpad,
            getter=self.get_handletextpad,
            layout=fr.vlayout
        )
    
    def set_frameon(self, value:bool):
        if self.legend:
            try:
                self.legend.set_frame_on(value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
        
    def get_frameon(self) -> bool:
        if self.legend: return self.legend.get_frame_on()
        return rcParams["legend.frameon"]

    def set_shadow(self, value:bool):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, shadow=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_shadow(self) -> bool:
        if self.legend: return self.legend.shadow
        return rcParams["legend.shadow"]

    def set_facecolor(self, color):
        if self.legend:
            try:
                self.legend.legendPatch.set_facecolor(color)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
        
    def get_facecolor(self):
        if self.legend: 
            return colors.to_hex(self.legend.legendPatch.get_facecolor())
        return rcParams["legend.facecolor"]

    def set_edgecolor(self, color):
        if self.legend:
            try:
                self.legend.legendPatch.set_edgecolor(color)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_edgecolor(self):
        if self.legend: 
            return colors.to_hex(self.legend.legendPatch.get_edgecolor())
        return rcParams["legend.edgecolor"]

    def set_edgestyle(self, value:str):
        if self.legend:
            try:
                self.legend.legendPatch.set_linestyle(value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_edgestyle(self) -> str:
        if self.legend:
            return self.legend.legendPatch.get_linestyle()
        return 'solid'
    
    def set_edgewidth(self, value:float):
        if self.legend:
            try:
                self.legend.legendPatch.set_linewidth(value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_edgewidth(self) -> float:
        if self.legend: return self.legend.legendPatch.get_linewidth()
        return 1.0

    def set_alpha(self, value):
        if self.legend:
            try:
                self.legend.legendPatch.set_alpha(value/100)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)

    def get_alpha(self):
        if self.legend: return int(self.legend.legendPatch.get_alpha()*100)
        return int(rcParams["legend.framealpha"]*100)

    def set_borderpad(self, value:float):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, borderpad=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_borderpad(self) -> float:
        if self.legend: return self.legend.borderpad
        return rcParams["legend.borderpad"]
    
    def set_handlelength(self, value:float):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, handlelength=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_handlelength(self) -> float:
        if self.legend: return self.legend.handlelength
        return rcParams["legend.handlelength"]
    
    def set_handleheight(self, value:float):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, handleheight=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_handleheight(self) -> float:
        if self.legend: return self.legend.handleheight
        return rcParams["legend.handleheight"]
    
    def set_handletextpad(self, value:float):
        if self.legend:
            try:
                update_legend(self.legend, self.canvas.axesleg, handletextpad=value)
                self.canvas.draw_idle()
            except Exception as e:
                logger.exception(e)
    
    def get_handletextpad(self) -> float:
        if self.legend: self.legend.handletextpad
        return rcParams["legend.handletextpad"]
    
class LegendLabel(QDialog):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.setMinimumWidth(500)

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