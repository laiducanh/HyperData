from node_editor.node.regressor.base import RegressorBase
from sklearn import svm
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class NuSVR(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            kernel='rbf',
            degree=3,
            gamma='scale',
            coef0=0,
            C=1.0,
            nu=0.5,
            shrinking=True,
        )
        else: self._config = config
        self.estimator = svm.NuSVR(**self._config)

        self.kernel = HTransparentComboBox(
            items=['linear','poly','rbf','sigmoid'],
            label='Kernel',
            getter=lambda: self._config['kernel'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.degree = HTransparentSpinBox(
            label='Degree',
            label2='Degree of the polynomial kernel function',
            getter=lambda: self._config['degree'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.gamma = HTransparentComboBox(
            items=['scale','auto'],
            label='Kernel coefficient',
            getter=lambda: self._config['gamma'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.coef0 = HTransparentDoubleSpinBox(
            label='Independent term',
            label2="Only significant in 'poly' and 'sigmoid' kernel",
            getter=lambda: self._config['coef0'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.c = HTransparentDoubleSpinBox(
            label='Regularization parameter',
            getter=lambda: self._config['C'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.nu = HTransparentDoubleSpinBox(
            label='Nu',
            label2='An upper bound on the fraction of training errors and a lower bound of the fraction of support vectors',
            minimum=0, maximum=1, singleStep=0.1,
            getter=lambda: self._config['nu'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.shrinking = HToggle(
            label='Shrinking',
            label2='Whether to use the shrinking heuristic',
            getter=lambda: self._config['shrinking'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['kernel'] = self.kernel.get_value()
        self._config['degree'] = self.degree.get_value()
        self._config['gamma'] = self.gamma.get_value()
        self._config['coef0'] = self.coef0.get_value()
        self._config['C'] = self.c.get_value()
        self._config['nu'] = self.nu.get_value()
        self._config['shrinking'] = self.shrinking.get_value()
        self.estimator = svm.NuSVR(**self._config)