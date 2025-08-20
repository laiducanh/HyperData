from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QDialog, QSizePolicy
from ui.base_widgets.button import HTransparentComboBox, HToggle, SegmentedWidget, VGroupRadioButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.frame import ScrollArea, SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.label.base import FontStyle
from config.settings import logger, marker_lib, linestyle_lib, font_lib
from matplotlib import ticker, dates, spines, lines, colors, rcParams
from matplotlib.axis import Axis
from plot.canvas import Canvas

DEBUG = False

class TickBase(ScrollArea):
    def __init__(self, axis:str, canvas:Canvas, parent=None):
        super().__init__(parent=parent)

        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_obj()

        self.initUI()
    
    def initUI(self):

        HToggle(
            label  = "Visible",
            label2 = f"Toggle {self.axis} ticks' visibility",
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        HLineEdit(
            label  = "Min Value",
            label2 = f"Set {self.axis} axis view minimum",
            setter=self.set_min,
            getter=self.get_min,
            layout=self.vlayout
        )

        HLineEdit(
            label  = 'Max Value',
            label2 = f"Set {self.axis} axis view maximum",
            setter=self.set_max,
            getter=self.get_max,
            layout=self.vlayout
        )

        VGroupRadioButton(
            label='Scale',
            label2=f"Set {self.axis} axis' scale",
            items=['linear','log','symlog','logit','asinh'],
            setter=self.set_scale,
            getter=self.get_scale,
            layout=self.vlayout
        )
        
    def find_obj(self) -> Axis:
        return self.canvas.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self.axis
        )[0]
        
    def set_visible(self, value):
        self.obj.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.obj.get_visible()

    def set_min(self, value):
        value = None if value == "" else value
        try:
            if self.axis in ['bottom','top']:
                self.obj.axes.set_xlim(left=float(value))
            else:
                self.obj.axes.set_ylim(bottom=float(value))
        except Exception as e: logger.exception(e)
        
        self.canvas.draw_idle()
    
    def set_max (self, value):
        value = None if value == "" else value
        try:
            if self.axis in ['bottom','top']:
                self.obj.axes.set_xlim(right=float(value))
            else:
                self.obj.axes.set_ylim(top=float(value))
        except Exception as e: logger.exception(e)

        self.canvas.draw_idle()

    def get_min(self):
        if self.axis in ['bottom','top']: return str(round(self.obj.axes.get_xlim()[0],5))
        else: return str(round(self.obj.axes.get_ylim()[0],5))

    def get_max(self):
        if self.axis in ['bottom','top']: return str(round(self.obj.axes.get_xlim()[1],5))
        else: return str(round(self.obj.axes.get_ylim()[1],5))
    
    def set_scale (self, value:str):
        try:
            if self.axis in ['bottom','top']: self.obj.axes.set_xscale(value)
            else: self.obj.axes.set_yscale(value)
            self.canvas.draw_idle()
        except Exception as e: logger.exception(e)
    
    def get_scale (self):
        if self.axis in ['bottom','top']: return self.obj.axes.get_xscale()
        else: return self.obj.axes.get_yscale()

class TickBase2(TickBase):
    def __init__(self, axis:str, type:str, canvas: Canvas, parent=None):

        self.ticktype = type

        super().__init__(axis, canvas, parent)

    def initUI(self):

        self.vlayout.addWidget(TitleLabel('Tick Parameters'))
        self.vlayout.addWidget(SeparateHLine())

        self.ticklocator = HTransparentComboBox(
            items=['Auto','Interval','Fixed Values','Max Number','Linear Scale',
                   'Log Scale','Sym Log Scale','Logit Scale','Asinh Scale',
                   'Auto Date','Day','Month','Weekday','Year','Hour','Minute',
                   'Second','Microsecond','None'],
            label='Type',
            setter=self.set_tick,
            getter=self.get_ticklocator,
            layout=self.vlayout
        )

        self.nbins = HTransparentSpinBox(
            minimum=1, maximum=100, singleStep=1,
            label='Max interval',
            label2='Maximum number of intervals',
            getter=self.get_nbins,
            setter=self.set_tick,
            layout=self.vlayout
        )

        self.min_n_ticks = HTransparentSpinBox(
            minimum=0, maximum=100, singleStep=1,
            label='Min ticks',
            label2='Minimum number of tick marks',
            getter=self.get_min_n_ticks,
            setter=self.set_tick,
            layout=self.vlayout
        )

        self.basescale = HTransparentDoubleSpinBox(
            label='Base',
            label2='Base of the scale',
            setter=self.set_tick,
            getter=self.get_base,
            layout=self.vlayout
        )

        self.interval = HTransparentDoubleSpinBox(
            label='Interval',
            label2='Interval between ticks',
            decimals=5,
            setter=self.set_tick,
            getter=self.get_interval,
            layout=self.vlayout
        )

        self.thresh = HTransparentDoubleSpinBox(
            label='Thresh',
            label2='The threshold to be used in type: Sym Log Scale, Asinh Scale',
            setter=self.set_tick,
            getter=self.get_thresh,
            layout=self.vlayout,
        )

        self.value = HLineEdit(
            label='Fixed values',
            label2=f"Set {self.axis} axis' tick positions",
            setter=self.set_tick,
            getter=self.get_tickvalues,
            layout=self.vlayout
        )

        self.linear_width = HTransparentDoubleSpinBox(
            label='Asinh Scale parameter',
            label2='The scale parameter defining the extent of the quasi-linear region.',
            setter=self.set_tick,
            getter=self.get_linear_width,
            layout=self.vlayout
        )

        tick_direction = HTransparentComboBox(
            label  = 'Tick direction',
            label2 = f"Put {self.ticktype}ticks inside/outside {self.axis} axis, or both",
            items = ['In','Out','InOut'],
            setter=self.set_tickdir,
            getter=self.get_tickdir,
            layout=self.vlayout
        )

        tickcolor = HColorDropdown(
            label  = 'Tick color', 
            getter=self.get_tickcolor,
            setter=self.set_tickcolor,
            layout=self.vlayout
        )

        tick_length = HTransparentDoubleSpinBox(
            label = 'Tick length',
            minimum = 0, maximum = 50, singleStep = 0.5,
            setter=self.set_ticklength,
            getter=self.get_ticklength,
            layout=self.vlayout
        )

        tick_width = HTransparentDoubleSpinBox(
            label = 'Tick width',
            minimum = 0, maximum = 50, singleStep = 0.5,
            setter=self.set_tickwidth,
            getter=self.get_tickwidth,
            layout=self.vlayout
        )

        self.vlayout.addWidget(TitleLabel('Tick Labels'))
        self.vlayout.addWidget(SeparateHLine())

        self.label = HToggle(
            label='Label',
            label2=f"Toggle {self.axis} axis' {self.ticktype} tick label",
            getter=self.get_label,
            setter=self.set_tick,
            layout=self.vlayout
        )

        self.fmt = HLineEdit(
            label="Label format",
            label2='Define how tick values is formatted as a string',
            getter=self.get_fmt,
            setter=self.set_tick,
            layout=self.vlayout
        )

        tick_labelsize = HTransparentDoubleSpinBox(
            label  = 'Label size',
            label2 = f"Set {self.axis} axis' {self.ticktype} tick label size",
            minimum = 1, maximum = 100, singleStep = 1,
            setter=self.set_labelsize,
            getter=self.get_labelsize,
            layout=self.vlayout
        )

        font = HTransparentComboBox(
            items = font_lib,
            label  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=self.vlayout
        )

        tick_labelcolor = HColorDropdown(
            label  = 'Label color', 
            setter=self.set_labelcolor,
            getter=self.get_labelcolor,
            layout=self.vlayout
        )

        style = FontStyle(
            obj = self.obj.get_majorticklabels() if self.ticktype == 'major'
                else self.obj.get_minorticklabels(), 
            canvas = self.canvas,
            layout=self.vlayout
        )

        alpha = HTransparentSpinBox(
            label = 'Transparency',
            singleStep = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )

        tick_rotation = HTransparentDoubleSpinBox(
            label = 'Tick label rotation',
            minimum = -180, maximum = 180, singleStep = 10,
            setter=self.set_labelrotation,
            getter=self.get_labelrotation,
            layout=self.vlayout
        )

        tick_labelpad = HTransparentDoubleSpinBox(
            label = 'Tick labelpad',
            minimum = 0, maximum = 50, singleStep = 0.5,
            setter=self.set_tickpadding,
            getter=self.get_tickpadding,
            layout=self.vlayout
        )

    def set_tick(self):
        try:
            locator = self.ticklocator.get_value()
            nbins = self.nbins.get_value()
            min_n_ticks = self.min_n_ticks.get_value()
            base = self.basescale.get_value()
            interval = self.interval.get_value()
            thresh = self.thresh.get_value()
            linear_width = self.linear_width.get_value()
            label = self.label.get_value()
            fmt = self.fmt.get_value()

            if locator == 'Auto':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.AutoLocator())
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.ScalarFormatter())
                else:
                    self.obj.set_minor_locator(ticker.AutoMinorLocator())
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.ScalarFormatter())
            elif locator == 'Interval':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.MultipleLocator(interval))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.ScalarFormatter())
                else:
                    self.obj.set_minor_locator(ticker.MultipleLocator(interval))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.ScalarFormatter())
            elif locator == 'Fixed Values':
                value = [float(i) for i in self.value.get_value().split(',')]
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.FixedLocator(value,nbins))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.FixedFormatter(value))
                else:
                    self.obj.set_minor_locator(ticker.FixedLocator(value,nbins))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.FixedFormatter(value))
            elif locator == 'Max Number':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.MaxNLocator(nbins,min_n_ticks=min_n_ticks))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.ScalarFormatter())
                else:
                    self.obj.set_minor_locator(ticker.MaxNLocator(nbins,min_n_ticks=min_n_ticks))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.ScalarFormatter())
            elif locator == 'Linear Scale':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.LinearLocator(nbins+1))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.ScalarFormatter())
                else:
                    self.obj.set_minor_locator(ticker.LinearLocator(nbins+1))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.ScalarFormatter())
            elif locator == 'Log Scale':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.LogLocator(base=base,numticks=nbins+1))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.LogFormatter(base))
                else:
                    self.obj.set_minor_locator(ticker.LogLocator(base=base, numticks=nbins+1))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.LogFormatter(base))
            elif locator == 'Sym Log Scale':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.SymmetricalLogLocator(base=base,linthresh=thresh))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.LogFormatter(base=base,linthresh=thresh))
                else:
                    self.obj.set_minor_locator(ticker.SymmetricalLogLocator(base=base,linthresh=thresh))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.LogFormatter(base=base,linthresh=thresh))
            elif locator == 'Logit Scale':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.LogitLocator(
                        minor=False, nbins=nbins, min_n_ticks=min_n_ticks))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.LogitFormatter(minor=False))
                else:
                    self.obj.set_minor_locator(ticker.LogitLocator(
                        minor=True, nbins=nbins, min_n_ticks=min_n_ticks))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.LogitFormatter(minor=True))
            elif locator == 'Asinh Scale':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.AsinhLocator(
                        linear_width=linear_width, base=base, symthresh=thresh))
                    if fmt: self.obj.set_major_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_major_formatter(ticker.ScalarFormatter())
                else:
                    self.obj.set_minor_locator(ticker.AsinhLocator(
                        linear_width=linear_width, base=base, symthresh=thresh))
                    if fmt: self.obj.set_minor_formatter(ticker.StrMethodFormatter(fmt))
                    else: self.obj.set_minor_formatter(ticker.ScalarFormatter())
            elif locator == 'Auto Date':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.AutoDateLocator(
                        maxticks=nbins+1, minticks=min_n_ticks))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.AutoDateLocator(
                        maxticks=nbins+1, minticks=min_n_ticks))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Day':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.DayLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.DayLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Hour':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.HourLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.HourLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Minute':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.MinuteLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.MinuteLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Month':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.MonthLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.MonthLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Second':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.SecondLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.SecondLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Weekday':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.WeekdayLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.WeekdayLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.set_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Year':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.YearLocator(base=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.YearLocator(base=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'Microsecond':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(dates.MicrosecondLocator(interval=int(interval)))
                    if fmt: self.obj.set_major_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_major_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_major_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_major_locator()
                    ))
                else:
                    self.obj.set_minor_locator(dates.MicrosecondLocator(interval=int(interval)))
                    if fmt: self.obj.set_minor_formatter(dates.AutoDateFormatter(
                        locator=self.obj.get_minor_locator(),
                        defaultfmt=fmt
                    ))
                    else: self.obj.set_minor_formatter(dates.ConciseDateFormatter(
                        locator=self.obj.get_minor_locator()
                    ))
            elif locator == 'None':
                if self.ticktype == 'major':
                    self.obj.set_major_locator(ticker.NullLocator())
                else:
                    self.obj.set_minor_locator(ticker.NullLocator())
            
            if not label:
                if self.ticktype == 'major':
                    self.obj.set_major_formatter(ticker.NullFormatter())
                else:
                    self.obj.set_minor_formatter(ticker.NullFormatter())

            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)

    def get_ticklocator(self) -> str:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
           
            if isinstance(locator, (ticker.AutoLocator, ticker.AutoMinorLocator)):
                return 'Auto'
            elif isinstance(locator, ticker.MultipleLocator):
                return 'Interval'
            elif isinstance(locator, ticker.FixedLocator):
                return 'Fixed Values'
            elif isinstance(locator, ticker.MaxNLocator):
                return 'Max Number'
            elif isinstance(locator, ticker.LinearLocator):
                return 'Linear Scale'
            elif isinstance(locator, ticker.LogLocator):
                return 'Log Scale'
            elif isinstance(locator, ticker.SymmetricalLogLocator):
                return 'Sym Log Scale'
            elif isinstance(locator, ticker.LogitLocator):
                return 'Logit Scale'
            elif isinstance(locator, ticker.AsinhLocator):
                return 'Asinh Scale'
            elif isinstance(locator, dates.AutoDateLocator):
                return 'Auto Date'
            elif isinstance(locator, dates.DayLocator):
                return 'Day'
            elif isinstance(locator, dates.HourLocator):
                return 'Hour'
            elif isinstance(locator, dates.MinuteLocator):
                return 'Minute'
            elif isinstance(locator, dates.MonthLocator):
                return "Month"
            elif isinstance(locator, dates.SecondLocator):
                return "Second"
            elif isinstance(locator, dates.WeekdayLocator):
                return 'Weekday'
            elif isinstance(locator, dates.YearLocator):
                return 'Year'
            elif isinstance(locator, dates.MicrosecondLocator):
                return 'Microsecond'
            elif isinstance(locator, ticker.NullLocator):
                return 'None'
        except Exception as e:
            logger.exception(e)
    
    def get_nbins(self) -> int:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            return int(locator._nbins)
        except Exception as e: return 10
    
    def get_min_n_ticks(self) -> int:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            return int(locator._min_n_ticks)
        except Exception as e: return 2
    
    def get_base(self) -> float:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            return float(locator._base)
        except Exception as e: return 10.0
    
    def get_interval(self) -> float:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            return float(locator._edge.step)
        except Exception as e: return 1.0
    
    def get_thresh(self) -> float:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            if isinstance(locator, ticker.SymmetricalLogLocator):
                return float(locator._linthresh)
            else:
                return float(locator.symthresh)
        except Exception as e: return 0.2

    def get_linear_width(self) -> float:
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            return float(locator.linear_width)
        except Exception as e: return 1.0

    def get_tickvalues(self):
        try:
            if self.ticktype == 'major':
                locator = self.obj.get_major_locator()
            elif self.ticktype == 'minor':
                locator = self.obj.get_minor_locator()
            return ', '.join(str(f'{x:g}') for x in locator.locs)
        except Exception as e: return
    
    def get_label(self) -> bool:
        if self.ticktype == 'major':
            return not isinstance(self.obj.get_major_formatter(), ticker.NullFormatter)
        else:
            return not isinstance(self.obj.get_minor_formatter(), ticker.NullFormatter)
    
    def get_fmt(self) -> str:
        if self.ticktype == 'major':
            try: return self.obj.get_major_formatter().fmt
            except: return
        else:
            try: return self.obj.get_minor_formatter().fmt
            except: return
        
    def set_labelsize (self, value):
        self.obj.set_tick_params(which=self.ticktype,labelsize=value)
        self.canvas.draw_idle()
    
    def get_labelsize (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklabels()[0].get_fontsize()
            else: 
                return self.obj.get_minorticklabels()[0].get_fontsize() 
        except: return self.obj.get_majorticklabels()[0].get_fontsize()
        
    def set_tickdir (self,value):
        self.obj.set_tick_params(which=self.ticktype,direction=value.lower())
        self.canvas.draw_idle()

    def get_tickdir (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_major_ticks()[0].get_tickdir().title()
            else: 
                return self.obj.get_minor_ticks()[0].get_tickdir().title()
        except: return rcParams['xtick.direction'].title()
    
    def set_labelcolor(self, color):
        self.obj.set_tick_params(which=self.ticktype,labelcolor=color)
        self.canvas.draw_idle()
    
    def get_labelcolor(self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklabels()[0].get_color()
            else: 
                return self.obj.get_minorticklabels()[0].get_color()
        except: return self.get_tickcolor()
    
    def set_fontname (self, font:str):
        if self.ticktype == 'major':
            for label in self.obj.get_majorticklabels():
                label.set_fontname(font)
        else:
            for label in self.obj.get_minorticklabels():
                label.set_fontname(font)
    
    def get_fontname(self):
        if self.ticktype == 'major':
            for label in self.obj.get_majorticklabels():
                return label.get_fontname()
        else:
            for label in self.obj.get_minorticklabels():
                return label.get_fontname()
        return rcParams[f"font.{rcParams['font.family'][0]}"][0]

    def set_alpha (self, value):
        if self.ticktype == 'major':
            for label in self.obj.get_majorticklabels():
                label.set_alpha(value/100)
        else:
            for label in self.obj.get_minorticklabels():
                label.set_alpha(value/100)
    
    def get_alpha (self):
        if self.ticktype == 'major':
            for label in self.obj.get_majorticklabels():
                if label.get_alpha(): 
                    return int(label.get_alpha()*100)
        else:
            for label in self.obj.get_minorticklabels():
                if label.get_alpha(): 
                    return int(label.get_alpha()*100)
        return 100

    def set_tickcolor(self, color):
        self.obj.set_tick_params(which=self.ticktype,color=color)
        self.canvas.draw_idle()
    
    def get_tickcolor(self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklines()[0].get_color()
            else: 
                return self.obj.get_minorticklines()[0].get_color()
        except: return rcParams['xtick.color']
    
    def set_labelrotation (self,value):
        self.obj.set_tick_params(which=self.ticktype,labelrotation=value)
        self.canvas.draw_idle()
    
    def get_labelrotation (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_majorticklabels()[0].get_rotation()
            else: 
                return self.obj.get_minorticklabels()[0].get_rotation()
        except: return 0
    
    def set_tickpadding (self,value):
        self.obj.set_tick_params(which=self.ticktype,pad=value)
        self.canvas.draw_idle()
    
    def get_tickpadding (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_major_ticks()[0].get_tick_padding()
            else: 
                return self.obj.get_minor_ticks()[0].get_tick_padding()
        except: return rcParams[f'xtick.{self.ticktype}.pad']
    
    def set_ticklength (self,value):
        self.obj.set_tick_params(which=self.ticktype,length=value)
        self.canvas.draw_idle()
    
    def get_ticklength (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_major_ticks()[0]._size
            else: 
                return self.obj.get_minor_ticks()[0]._size
        except: return rcParams[f'xtick.{self.ticktype}.size']
    
    def set_tickwidth (self,value):
        self.obj.set_tick_params(which=self.ticktype,width=value)
        self.canvas.draw_idle()
    
    def get_tickwidth (self):
        try:
            if self.ticktype == 'major': 
                return self.obj.get_major_ticks()[0]._width
            else: 
                return self.obj.get_minor_ticks()[0]._width
        except: return rcParams[f'xtick.{self.ticktype}.width']

class SpineBase(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.axis = axis
        self.canvas = canvas
        self.spines, self.arrows = self.find_object()

        self.initUI()

    def initUI(self):

        visible = HToggle(
            label='Spine visible',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        arrow = HTransparentComboBox(
            label  = 'Arrow Style',
            items = marker_lib.values(),
            setter=self.set_arrow,
            getter=self.get_arrow,
            layout=self.vlayout
        )

        color = HColorDropdown(
            label='Spine color',
            setter=self.set_color,
            getter=self.get_color,
            layout=self.vlayout
        )
        
        arrowcolor = HColorDropdown(
            label="Arrow color",
            setter=self.set_arrowcolor,
            getter=self.get_arrowcolor,
            layout=self.vlayout
        )

        alpha = HTransparentSpinBox(
            label ='Transparent',
            minimum = 0, maximum = 100, singleStep = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )

        linestyle = HTransparentComboBox(
            label  = 'Line style',
            items = linestyle_lib.values(),
            setter=self.set_linestyle,
            getter=self.get_linestyle,
            layout=self.vlayout
        )

        linewidth = HTransparentDoubleSpinBox(
            label = 'Line width',
            minimum = 0, maximum = 20, singleStep = 0.5,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=self.vlayout
        )

    def find_object (self) -> tuple[list[spines.Spine], list[lines.Line2D]]:
        s = self.canvas.figure.findobj(
            lambda a: isinstance(a, spines.Spine) and a.get_gid() \
            and a.get_gid() == f"spine {self.axis}"
        )
        a = self.canvas.figure.findobj(
            lambda a: isinstance(a, lines.Line2D) and a.get_gid() \
            and a.get_gid() == f"spine {self.axis}"
        )
        return s, a
    
    def set_visible (self, value:bool):
        for obj in self.spines+self.arrows:
            obj.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible (self):
        return self.spines[0].get_visible()  

    def set_arrow(self, marker):
        try:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
            for obj in self.arrows:
                obj.set_marker(marker)
        except Exception as e:
            logger.exception(e)
        self.canvas.draw_idle()
    
    def get_arrow(self):
        return marker_lib[self.arrows[0].get_marker()]
    
    def set_alpha (self, value):
        for obj in self.spines+self.arrows:
            obj.set_alpha(float(value/100))
        self.canvas.draw_idle()
    
    def get_alpha(self):
        if self.spines[0].get_alpha() == None:
            return 100
        return self.spines[0].get_alpha()*100
    
    def set_linestyle(self, value):
        for obj in self.spines:
            obj.set_linestyle(value)
        self.canvas.draw_idle()
    
    def get_linestyle(self):
        return self.spines[0].get_linestyle()

    def set_linewidth(self, value):
        for obj in self.spines+self.arrows:
            obj.set_linewidth(value)
        self.canvas.draw_idle()
    
    def get_linewidth (self):
        return self.spines[0].get_linewidth()

    def set_color(self, color):
        for obj in self.spines+self.arrows:
            obj.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        return colors.rgb2hex(self.spines[0].get_edgecolor())

    def set_arrowcolor(self, color):
        for obj in self.arrows:
            obj.set_markerfacecolor(color)
        self.canvas.draw_idle()
    
    def get_arrowcolor(self):
        return colors.rgb2hex(self.arrows[0].get_markerfacecolor())

class AxisLabel(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        self.axis = axis
        self.ax = self.find_axis()
        self.text = self.ax.get_label()

        self.initUI()
    
    def initUI(self):

        label = HLineEdit(
            label='Label',
            getter=self.get_label,
            setter=self.set_label,
            layout=self.vlayout
        )
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        font = HTransparentComboBox(
            items = font_lib,
            label  = 'Font',
            setter=self.set_fontname,
            getter=self.get_fontname,
            layout=self.vlayout
        )

        size = HTransparentDoubleSpinBox(
            label = 'Font size',
            minimum = 1, maximum = 100, singleStep = 1,
            setter=self.set_fontsize,
            getter=self.get_fontsize,
            layout=self.vlayout
        )

        style = FontStyle(
            obj = [self.text], 
            canvas = self.canvas,
            layout=self.vlayout
        )

        color = HColorDropdown(
            label  = 'Font color',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        # self.backgroundcolor = ColorDropdown(
        #     text  = 'Background color',
        #     getter=self.get_backgroundcolor,
        #     setter=self.set_backgroundcolor,
        #     layout=layout
        # )

        # edgecolor = ColorDropdown(
        #     text  = 'Edge color',
        #     getter=self.get_edgecolor,
        #     setter=self.set_edgecolor,
        #     layout=layout
        # )

        alpha = HTransparentSpinBox(
            label = 'Transparency',
            singleStep = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )
    
    def find_axis(self) -> Axis:
        return self.canvas.figure.findobj(
            lambda a: isinstance(a, Axis) and a.get_gid() \
            and a.get_gid() == self.axis
        )[0]
        
    def set_label(self, value:str):
        self.ax.set_label_text(value)
        self.canvas.draw_idle()
    
    def get_label(self) -> str:
        return self.ax.get_label_text()

    def set_fontname (self, font:str):
        self.text.set_fontname(font)
        self.canvas.draw_idle()
    
    def get_fontname(self):
        return self.text.get_fontname()
    
    def set_fontsize(self, value):
        self.text.set_fontsize(value)
        self.canvas.draw_idle()
    
    def get_fontsize(self):
        return self.text.get_fontsize()
    
    def set_color (self, color):
        self.text.set_color(color)
        self.canvas.draw_idle()
    
    def get_color (self):
        return self.text.get_color()

    def set_backgroundcolor (self, color):
        self.text.set_backgroundcolor(color)
        self.canvas.draw_idle()
    
    def get_backgroundcolor(self):
        if self.text.get_bbox_patch() != None:
            return self.text.get_bbox_patch().get_facecolor()
        return 'white'
    
    def set_edgecolor (self, color):
        self.text.set_bbox({"edgecolor":color,
                           "facecolor":self.backgroundcolor.button.color.name()})
        self.canvas.draw_idle()
    
    def get_edgecolor(self):
        if self.text.get_bbox_patch():
            return self.text.get_bbox_patch().get_edgecolor()
        return 'white'
    
    def set_alpha (self, value):
        self.text.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_alpha (self):
        if self.text.get_alpha() != None:
            return int(self.text.get_alpha()*100)
        return 100
    
class Tick2D(QDialog):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f'{axis.title()} Axis')
        layout = QVBoxLayout(self)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget(parent)
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='General', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Major', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Minor', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.choose_axis.addButton(text='Spine', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.choose_axis.addButton(text='Label', func=lambda: self.stackedlayout.setCurrentIndex(4))

        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        base = TickBase(axis, canvas, parent)
        self.stackedlayout.addWidget(base)

        major = TickBase2(axis, 'major', canvas, parent)
        self.stackedlayout.addWidget(major)

        minor = TickBase2(axis, 'minor', canvas, parent)
        self.stackedlayout.addWidget(minor)

        spine = SpineBase(axis, canvas, parent)
        self.stackedlayout.addWidget(spine)

        label = AxisLabel(axis, canvas, parent)
        self.stackedlayout.addWidget(label)
