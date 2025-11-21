from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class Quantile(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            quantile=0.5,
            alpha=1,
            solver='highs',
        )
        else: self._config = config
        self.estimator = linear_model.QuantileRegressor(**self._config)

        self.quantile = HTransparentDoubleSpinBox(
            label='Quantile',
            label2='The quantile that the model tries to predict',
            minimum=0, maximum=1, singleStep=0.1,
            getter=lambda: self._config['quantile'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.alpha = HTransparentDoubleSpinBox(
            label='Regularization strength',
            label2='Constant that multiplies the L1 term',
            minimum=0, maximum=1000, singleStep=1,
            getter=lambda: self._config['alpha'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.solver = HTransparentComboBox(
            items=['highs-ds', 'highs-ipm', 'highs', 'interior-point', 'revised simplex'],
            label='Solver',
            getter=lambda: self._config['solver'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['alpha'] = self.alpha.get_value()
        self._config['quantile'] = self.quantile.get_value()
        self._config['solver'] = self.solver.get_value()
        self.estimator = linear_model.QuantileRegressor(**self._config)