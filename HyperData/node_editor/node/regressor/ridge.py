from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox

class RidgeRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            alpha=1.0,
            solver="auto",
            positive=False
        )
        else: self._config = config
        self.estimator = linear_model.Ridge(**self._config)

        self.alpha = HTransparentDoubleSpinBox(
            label='Regularization strength',
            label2='Constant that multiplies the L2 term',
            minimum=0, maximum=1000, singleStep=1,
            getter=lambda: self._config['alpha'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.solver = HTransparentComboBox(
            items=["auto","svd","cholesky","lsqr","sparse_cg","sag","saga","lbfgs"],
            label='Solver',
            getter=lambda: self._config['solver'],
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
        self._config['solver'] = self.solver.get_value()
        self._config['positive'] = self.positive.get_value()
        self.estimator = linear_model.Ridge(**self._config)