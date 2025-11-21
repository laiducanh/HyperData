from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class Poisson(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            alpha=1.0,
            solver='lbfgs',
            max_iter=100,
        )
        else: self._config = config
        self.estimator = linear_model.PoissonRegressor(**self._config)

        self.alpha = HTransparentDoubleSpinBox(
            label='Regularization strength',
            label2='Constant that multiplies the L2 term',
            minimum=0, maximum=1000, singleStep=1,
            getter=lambda: self._config['alpha'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.solver = HTransparentComboBox(
            items=['lbfgs', 'newton-cholesky'],
            label='Solver',
            label2='Optimization algorithm',
            getter=lambda: self._config['solver'],
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
        
    def set_estimator(self):
        self._config['alpha'] = self.alpha.get_value()
        self._config['max_iter'] = self.max_iter.get_value()
        self._config['solver'] = self.solver.get_value()
        self.estimator = linear_model.PoissonRegressor(**self._config)