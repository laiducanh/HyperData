from PySide6.QtWidgets import QVBoxLayout
from config.settings import logger, GLOBAL_DEBUG
from config.settings import config as global_config
from ui.base_widgets.button import HTransparentComboBox, HTransparentPushButton
from ui.base_widgets.frame import Frame
from ui.base_widgets.text import BodyLabel
from plot.utilis import complementary_color
from node_editor.node.statistics.one_sample_test.base import TestBase, ResultDialogBase
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, samples, dist, result, parent=None):
        super().__init__(samples=samples, result=result, parent=parent)

        self._result = result
        self.dist = dist
        self.plot()

    def initStats(self, result):
        HTransparentPushButton(
            label='Statistic',
            label2='Maximum distance between empirical CDF and theoretical CDF',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            label2='Probability of observing that large a difference if null is true',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='Statistic location',
            label2='The distance between the empirical CDF and theoretical CDF',
            getter=lambda: str(result.statistic_location),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='Statistic sign',
            getter=lambda: 'positive' if result.statistic_sign == 1 else 'negative',
            layout=self.main_layout
        )
    
    def plot(self):
        super().plot()

        title = f"One-sample Kolmogorov-Smirnov test"

        # Compute ECDF and CDF
        ecdf = ECDF(self.samples)
        x = np.linspace(np.min(self.samples), np.max(self.samples), 500)
        cdf = self.dist.cdf(x)

        ecdf_line = self.ax.plot(
            x, ecdf(x),
            linewidth=2.0,
            marker='none',
            label='Empirical CDF'
        )
        cdf_line = self.ax.plot(
            x, cdf, 
            linewidth=2.0,
            marker='none',
            color=complementary_color(ecdf_line[0].get_color()),
            label='Theoretical CDF'
        )
        self.ax2.set_axis_off()
        self.axleg.legend(handles=[ecdf_line[0], cdf_line[0]])
        self.ax.set_title(title)
        self.canvas.draw_idle()
            
class Kolmogorov(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
            method = "auto",
        )
        else: self._config = config

        frame = Frame()
        frame.backgroundColor = global_config['themecolor']
        framelayout = QVBoxLayout(frame)
        self.vlayout.addWidget(frame)

        framelayout.addWidget(BodyLabel(
            "Note: this statistical test requires probability distribution."
        ))

        self.alternative = HTransparentComboBox(
            items=["two-sided","less","greater"], 
            label="Alternative hypothesis",
            getter=lambda: self._config["alternative"],
            layout=self.vlayout
        )

        self.method = HTransparentComboBox(
            items=["auto","exact","approx","asymp"], 
            label="Method",
            getter=lambda: self._config["method"],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            method = self.method.button.currentText(),
            alternative = self.alternative.button.currentText()
        )
       
    def result_dialog(self, samples, dist, result):
        dialog = ResultDialog(samples, dist, result)
        dialog.exec()