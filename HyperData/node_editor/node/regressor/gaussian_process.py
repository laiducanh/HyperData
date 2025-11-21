from node_editor.node.regressor.base import RegressorBase
from sklearn import gaussian_process
from ui.base_widgets.button import HTransparentComboBox, HToggle, HGroupRadioButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class GaussianProcess(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            n_restarts_optimizer=0,
            normalize_y=False
        )
        else: self._config = config
        self.estimator = gaussian_process.GaussianProcessRegressor(**self._config)

        self.n_restarts_optimizer = HTransparentSpinBox(
            label='Number of retarts',
            getter=lambda: self._config['n_restarts_optimizer'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.normalize_y = HToggle(
            label='Normalize targets',
            label2='Whether to normalize the target values',
            getter=lambda: self._config['normalize_y'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['radin_restarts_optimizerus'] = self.n_restarts_optimizer.get_value()
        self._config['normalize_y'] = self.normalize_y.get_value()
        self.estimator = gaussian_process.GaussianProcessRegressor(**self._config)