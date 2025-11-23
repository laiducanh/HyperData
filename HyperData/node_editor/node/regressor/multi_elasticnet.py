from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HToggle
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class MultiElasticNet(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            alpha=1.0,
            l1_ratio=0.5,
            max_iter=1000,
            positive=False
        )
        else: self._config = config
        self.estimator = linear_model.ElasticNet(**self._config)

        self.alpha = HTransparentDoubleSpinBox(
            label='Alpha',
            label2='Constant that multiplies the penalty term',
            minimum=0, maximum=1000, singleStep=1,
            getter=lambda: self._config['alpha'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_iter = HTransparentSpinBox(
            label='Maximum iterations',
            minimum=1, maximum=100000, singleStep=1000,
            getter=lambda: self._config['max_iter'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.l1_ratio = HTransparentDoubleSpinBox(
            label='L1 ratio',
            label2='The ElasticNet mixing parameter',
            minimum=0, maximum=1, singleStep=0.1,
            getter=lambda: self._config['l1_ratio'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.positive = HToggle(
            label='Positive coefficients',
            label2='Whether to force the coefficients to be positive',
            getter=lambda: self._config['positive'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['alpha'] = self.alpha.get_value()
        self._config['max_iter'] = self.max_iter.get_value()
        self._config['l1_ratio'] = self.l1_ratio.get_value()
        self._config['positive'] = self.positive.get_value()
        self.estimator = linear_model.ElasticNet(**self._config)