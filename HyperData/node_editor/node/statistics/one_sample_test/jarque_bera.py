from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentPushButton
from plot.utilis import complementary_color
from node_editor.node.statistics.one_sample_test.base import TestBase, ResultDialogBase
import numpy as np
from scipy.stats import norm

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, samples, result, parent=None):
        super().__init__(samples=samples, result=result, parent=parent)
    
        self._result = result
        self.plot()

    def initStats(self, result):
        HTransparentPushButton(
            label='Statistic',
            label2='The test statistic',
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

        title = "Cramér-von Mises test"
        hist = self.ax.hist(
            self.samples, 
            label="Samples", 
            bins='auto', 
            histtype='stepfilled', 
            alpha=0.2
        )

        # Fit parameters of normal distribution (MLE)
        mu, sigma = np.mean(self.samples), np.std(self.samples, ddof=1)
        x = np.linspace(np.min(self.samples), np.max(self.samples), 100)
        pdf = norm.pdf(x, loc=mu, scale=sigma)
        line = self.ax2.plot(
            x, pdf, 
            linewidth=2.0,
            marker='none',
            color=complementary_color(hist[-1][0].get_facecolor()),
            label=f'Normal PDF\nμ={mu:.2f}, σ={sigma:.2f}'
        )
    
        self.axleg.legend(handles=[hist[-1][0], line[0]])
        self.ax.set_title(title)
        self.canvas.draw_idle()
            
class JarqueBera(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
       
    def result_dialog(self, samples, dist, result):
        dialog = ResultDialog(samples, result)
        dialog.exec()
