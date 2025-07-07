from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox, TransparentPushButton
from ui.base_widgets.spinbox import DoubleSpinBox
from plot.utilis import complementary_color
from node_editor.node.statistics.one_sample_test.base import TestBase, ResultDialogBase
import numpy as np

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, samples, q, p, result, parent=None):
        super().__init__(samples=samples, result=result, parent=parent)

        self._result = result
        self.p = p
        self.q = q
        self.plot()

    def initStats(self, result):
        TransparentPushButton(
            text='Statistic',
            text2='Proportion of samples on the less extreme side of the hypothesized quantile',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='p-value',
            text2='Probability of observing this imbalace (or more extreme) under the null',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='95% Confidence interval',
            text2='The confidence interval around the population quantile',
            getter=lambda: f"[{result.confidence_interval().low}, {result.confidence_interval().high}]",
            layout=self.main_layout
        )
    
    def plot(self):
        super().plot()

        title = f"Quantile test p={self.p}"
        hist = self.ax.hist(
            self.samples, 
            label="Samples", 
            bins='auto', 
            histtype='stepfilled', 
            alpha=0.2
        )
        true = self.ax.axvline(
            np.quantile(self.samples, self.p),
            marker='none',
            linestyle='dashed',
            linewidth=2.0,
            label=f'Sample quantile = {np.quantile(self.samples, self.p):.5f}'
        )
        null = self.ax.axvline(
            self.q,
            marker='none',
            linestyle='dashed',
            linewidth=2.0,
            color=complementary_color(true.get_color()),
            label=f'Hypothesized quantile {self.q:.5f}'
        )
    
        self.ax2.set_axis_off()
        self.axleg.legend(handles=[hist[-1][0], true, null])
        self.ax.set_title(title)
        self.canvas.draw_idle()

class QuantileTest(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            q = 0.0,
            p = 0.5,
            alternative = "two-sided"
        )
        else: self._config = config
    
        self.q = DoubleSpinBox(
            text="Hypothesized value",
            text2='The hypothesized value of the quantile',
            decimals=5,
            getter=lambda: self._config["q"],
            layout=self.vlayout
        )

        self.p = DoubleSpinBox(
            max=1, min=0, step=0.1, 
            text="Probability of quantile",
            text2="The proportion of the population less than hypothesized value",
            getter=lambda: self._config["p"],
            layout=self.vlayout
        )

        self.alternative = ComboBox(
            items=["two-sided","less","greater"], 
            text="Alternative hypothesis",
            getter=lambda: self._config["alternative"],
            layout=self.vlayout
        )
        
    def update_config(self):
        self._config.update(
            q = self.q.button.value(),
            p = self.p.button.value(),
            alternative = self.alternative.button.currentText()
        )
       
    def result_dialog(self, samples, dist, result):
        dialog = ResultDialog(samples, self.q.get_value(), self.p.get_value(), result)
        dialog.exec()
