from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, HTransparentPushButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from plot.utilis import complementary_color
from node_editor.node.statistics.one_sample_test.base import TestBase, ResultDialogBase
from scipy.stats._result_classes import TtestResult
import numpy as np

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, samples, popmean, result:TtestResult, parent=None):
        super().__init__(samples=samples, result=result, parent=parent)

        self._result = result
        self.popmean = popmean
        self.plot()

    def initStats(self, result:TtestResult):
        HTransparentPushButton(
            label='The t-statistic',
            label2='How far the sample mean is from the population mean, in standard errors',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            label2='Probability of observing this result (or more extreme) if null hypothesis is true',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout

        )
        HTransparentPushButton(
            label='Degrees of freedom',
            label2='The number of degrees of freedom used in the calculation of the t-statistic',
            getter=lambda: str(result.df),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='95% Confidence interval',
            label2='The confidence interval around the population mean',
            getter=lambda: f"[{result.confidence_interval().low}, {result.confidence_interval().high}]",
            layout=self.main_layout
        )
    
    def plot(self):
        super().plot()

        title = "One sample T-test"
        hist = self.ax.hist(
            self.samples, 
            label="Samples", 
            bins='auto', 
            histtype='stepfilled', 
            alpha=0.2
        )
        true_mean = self.ax.axvline(
            np.mean(self.samples),
            marker='none',
            linestyle='dashed',
            linewidth=2.0,
            label=f'Sample mean = {np.mean(self.samples):.5f}'
        )
        null_mean = self.ax.axvline(
            self.popmean,
            marker='none',
            linestyle='dashed',
            linewidth=2.0,
            color=complementary_color(true_mean.get_color()),
            label=f'Population mean {self.popmean:.5f}'
        )
    
        self.ax2.set_axis_off()
        self.axleg.legend(handles=[hist[-1][0], true_mean, null_mean])
        self.ax.set_title(title)
        self.canvas.draw_idle()
        
class Ttest1samp(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            popmean = 0,
            alternative = "two-sided"
        )
        else: self._config = config
    
        self.popmean = HTransparentDoubleSpinBox(
            minimum=-100000, maximum=100000, decimals=5, 
            label="Population mean",
            label2="Expected value in null hypothesis",
            getter=lambda: self._config["popmean"],
            layout=self.vlayout
        )

        self.alternative = HTransparentComboBox(
            items=["two-sided","less","greater"], 
            label="Alternative hypothesis",
            getter=lambda: self._config["alternative"],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            popmean = self.popmean.button.value(),
            alternative = self.alternative.button.currentText()
        )
       
    def result_dialog(self, samples, dist, result:TtestResult):
        dialog = ResultDialog(samples, self.popmean.get_value(), result)
        dialog.exec()
