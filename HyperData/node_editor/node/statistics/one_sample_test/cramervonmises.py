from PySide6.QtWidgets import QVBoxLayout
from config.settings import logger, GLOBAL_DEBUG
from config.settings import config as global_config
from ui.base_widgets.button import HTransparentPushButton
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
            label2='Cramér-von Mises statistic',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            label2='Probability of observing this result (or more extreme) if null hypothesis is true',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
    
    def plot(self):
        super().plot()

        title = "One-sample Cramér-von Mises test"
        # Create ECDF
        ecdf = ECDF(self.samples)
        x = np.linspace(np.min(self.samples), np.max(self.samples), 500)
        cdf = self.dist.cdf(x)  # CDF of N(0, 1)
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
            
            
class CramervonMises(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config

        frame = Frame()
        frame.backgroundColor = global_config['themecolor']
        framelayout = QVBoxLayout(frame)
        self.vlayout.addWidget(frame)

        framelayout.addWidget(BodyLabel(
            "Note: this statistical test requires probability distribution."
        ))
       
    def result_dialog(self, samples, dist, result):
        dialog = ResultDialog(samples, dist, result)
        dialog.exec()
