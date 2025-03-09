from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import ComboBox
from plot.canvas import Canvas
from scipy.stats._continuous_distns import norm_gen
import numpy as np

class DistBase (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)   

        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        self._config = dict()
        self.dist = None
        self.set_config(config=None)
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def set_config(self, config=None):
        self.clear_layout()
    
    def update_config(self):
        pass

    def result_dialog(self):
        pass

class ResultDialog(Dialog):
    def __init__(self, dist:norm_gen, title:str, parent=None):
        super().__init__(parent)

        self.dist = dist
        self.title = title
        self.main_layout.addWidget(BodyLabel(f"Median {self.dist.median()}"))
        self.main_layout.addWidget(BodyLabel(f"Mean {self.dist.mean()}"))
        self.main_layout.addWidget(BodyLabel(f"Standard deviation {self.dist.std()}"))
        self.main_layout.addWidget(BodyLabel(f"95% Confidence interval {self.dist.interval(0.95)}"))
        self.pl = ComboBox(items=["Probability density function","Log of the probability density function",
                                  "Cumulative distribution function","Log of the cumulative distribution function",
                                  "Survival function","Log of the survival function"], 
                                  text="Probability function")
        self.pl.button.currentTextChanged.connect(self.plot)
        self.main_layout.addWidget(self.pl)
        self.canvas = Canvas()
        for _ax in self.canvas.fig.axes: _ax.remove()
        self.plot()
        self.main_layout.addWidget(self.canvas)
        
    def plot(self):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        ax = self.canvas.fig.add_subplot()
        axleg = self.canvas.fig.add_subplot()
        axleg.set_axis_off()
        ax2 = ax.twinx()

        x = np.linspace(self.dist.ppf(0.01), self.dist.ppf(0.99), 1000)
        fn = self.pl.button.currentText()
        if fn == "Probability density function":
            line = ax2.plot(x, self.dist.pdf(x), label=fn, color="r", marker='', lw=2)
        elif fn == "Log of the probability density function":
            line = ax2.plot(x, self.dist.logpdf(x), label=fn, color="r", marker='', lw=2)
        elif fn == "Cumulative distribution function":
            line = ax2.plot(x, self.dist.cdf(x), label=fn, color='r', marker='', lw=2)
        elif fn == "Log of the cumulative distribution function":
            line = ax2.plot(x, self.dist.logcdf(x), label=fn, color='r', marker='', lw=2)
        elif fn == "Survival function":
            line = ax2.plot(x, self.dist.sf(x), label=fn, color='r', marker='', lw=2)
        elif fn == "Log of the survival function":
            line = ax2.plot(x, self.dist.logsf(x), label=fn, color='r', marker='', lw=2)
        
        hist = ax.hist(self.dist.rvs(1000), label="Sample points", bins='auto', histtype='stepfilled', alpha=0.2)
        
        axleg.legend(handles=[line[0], hist[-1][0]])
        ax.set_xlim([x[0], x[-1]])
        ax.set_title(self.title)
        self.canvas.draw_idle()