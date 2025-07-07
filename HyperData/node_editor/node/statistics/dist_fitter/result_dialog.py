from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import TransparentComboBox, TransparentPushButton
from plot.canvas import Canvas
from scipy.stats._continuous_distns import norm_gen
import numpy as np

class ResultDialog(Dialog):
    def __init__(self, data, dist:norm_gen, title:str, parent=None):
        super().__init__(parent)

        self.data = data
        self.dist = dist
        self.title = title
        TransparentPushButton(
            text='Median',
            getter=lambda: str(self.dist.median()),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='Mean',
            getter=lambda: str(self.dist.mean()),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='Standard deviation',
            getter=lambda: str(self.dist.std()),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='95% Confidence interval',
            getter=lambda: str(self.dist.interval(0.95)),
            layout=self.main_layout
        )
        self.pl = TransparentComboBox(items=["Probability density function","Log of the probability density function",
                                  "Cumulative distribution function","Log of the cumulative distribution function",
                                  "Survival function","Log of the survival function"], 
                                  text="Probability function")
        self.pl.button.currentTextChanged.connect(self.plot)
        self.main_layout.addWidget(self.pl)
        self.canvas = Canvas()
        for _ax in self.canvas.figure.axes: _ax.remove()
        self.plot()
        self.main_layout.addWidget(self.canvas)
        
    def plot(self):
        # clear plot
        self.canvas.figure.clear()

        # add axis
        ax = self.canvas.figure.add_subplot()
        ax2 = ax.twinx()
        axleg = self.canvas.figure.add_subplot()
        axleg.set_axis_off()

        x = np.linspace(np.min(self.data), np.max(self.data), 100)
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
        
        hist = ax.hist(self.data, label="Sample points", bins='auto', histtype='stepfilled', alpha=0.2)
        
        axleg.legend(handles=[line[0], hist[-1][0]])
        ax.set_xlim([x[0], x[-1]])
        ax.set_title(self.title)
        self.canvas.draw_idle()