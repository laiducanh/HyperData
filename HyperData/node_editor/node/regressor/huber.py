from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class Huber(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            epsilon=1.35,
            alpha=1e-4,
            max_iter=100,
        )
        else: self._config = config
        self.estimator = linear_model.HuberRegressor(**self._config)

        self.epsilon = HTransparentDoubleSpinBox(
            label='Epsilon',
            label2='The parameter controls the number of samples that should be classified as outliers',
            getter=lambda: self._config['epsilon'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_iter = HTransparentSpinBox(
            label='Maximum iterations',
            minimum=1, maximum=100000, singleStep=100,
            getter=lambda: self._config['max_iter'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.alpha = HTransparentDoubleSpinBox(
            label='Regularization strength',
            label2='Constant that multiplies the L2 term',
            minimum=0, maximum=1000, singleStep=1e-4, decimals=5,
            getter=lambda: self._config['alpha'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['alpha'] = self.alpha.get_value()
        self._config['max_iter'] = self.max_iter.get_value()
        self._config['epsilon'] = self.epsilon.get_value()
        self.estimator = linear_model.HuberRegressor(**self._config)