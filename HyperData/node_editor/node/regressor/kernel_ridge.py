from node_editor.node.regressor.base import RegressorBase
from sklearn import kernel_ridge
from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox, HTransparentDoubleSpinBox

class KernelRidge(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            alpha=1.0,
            kernel='linear',
            degree=3,
            coef0=1,
        )
        else: self._config = config
        self.estimator = kernel_ridge.KernelRidge(**self._config)

        self.alpha = HTransparentDoubleSpinBox(
            label='Regularization strength',
            label2='Constant that multiplies the L2 term',
            minimum=0, maximum=1000, singleStep=1,
            getter=lambda: self._config['alpha'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.kernel = HTransparentComboBox(
            items=['additive_chi2','chi2','linear','polynomial','poly','rbf',
                   'laplacian','sigmoid','cosine'],
            label='Kernel',
            getter=lambda: self._config['kernel'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.degree = HTransparentSpinBox(
            label='Degree',
            label2='Degree of the polynomial kernel, ignored by other kernels',
            getter=lambda: self._config['degree'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.coef0 = HTransparentDoubleSpinBox(
            label='Zero coefficient',
            label2='Effective to polynomial and sigmoid kernels',
            getter=lambda: self._config['coef0'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['alpha'] = self.alpha.get_value()
        self._config['kernel'] = self.kernel.get_value()
        self._config['degree'] = self.degree.get_value()
        self._config['coef0'] = self.coef0.get_value()
        self.estimator = kernel_ridge.KernelRidge(**self._config)