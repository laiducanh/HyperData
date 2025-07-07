from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox, TransparentPushButton
from plot.utilis import complementary_color
from node_editor.node.statistics.one_sample_test.base import TestBase, ResultDialogBase
from scipy.stats import norm, expon, logistic, gumbel_l, gumbel_r, weibull_min
import numpy as np

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, samples, dist, result, parent=None):
        super().__init__(samples=samples, result=result, parent=parent)

        self._result = result
        self.dist = dist
        self.plot()

    def initStats(self, result):
        TransparentPushButton(
            text='Statistic',
            text2='The Anderson-Darling test statistic',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='Critical values',
            text2='The critical values for this distribution',
            getter=lambda: str(result.critical_values),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='Significance level',
            text2='The significance levels for the corresponding critical values in percents',
            getter=lambda: str(result.significance_level),
            layout=self.main_layout
        )
    
    def plot(self):
        super().plot()

        title = "Anderson-Darling test"
        hist = self.ax.hist(
            self.samples, 
            label="Samples", 
            bins='auto', 
            histtype='stepfilled', 
            alpha=0.2
        )

        x = np.linspace(np.min(self.samples), np.max(self.samples), 100)
        if self.dist == 'norm':
            pdf = norm.pdf(x, *self._result.fit_result.params)
        elif self.dist == 'expon':
            pdf = expon.pdf(x, *self._result.fit_result.params)
        elif self.dist == 'logistic':
            pdf = logistic.pdf(x, *self._result.fit_result.params)
        elif self.dist == 'gumbel':
            pdf = gumbel_l.pdf(x, *self._result.fit_result.params)
        elif self.dist == 'gumbel_r':
            pdf = gumbel_r.pdf(x, *self._result.fit_result.params)
        elif self.dist == 'weibull_min':
            pdf = weibull_min.pdf(x, *self._result.fit_result.params)
        line = self.ax2.plot(
            x, pdf, 
            linewidth=2.0,
            marker='none',
            color=complementary_color(hist[-1][0].get_facecolor()),
            label=f'PDF'
        )
    
        self.axleg.legend(handles=[hist[-1][0], line[0]])
        self.ax.set_title(title)
        self.canvas.draw_idle()
            

class Anderson(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            dist = "norm"
        )
        else: self._config = config
    
        self.dist = ComboBox(
            items=["norm","expon","logistic","gumbel","gumbel_r","weibull_min"], 
            text="Distribution",
            text2="The type of distribution to test against",
            getter=lambda: self._config["dist"],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            dist = self.dist.button.currentText()
        )
       
    def result_dialog(self, samples, dist, result):
        dialog = ResultDialog(samples, self.dist.get_value(), result)
        dialog.exec()
