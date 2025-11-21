from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HToggle
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class ARD(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            alpha_1=1e-6,
            alpha_2=1e-6,
            lambda_1=1e-6,
            lambda_2=1e-6,
            max_iter=300,
            threshold_lambda=10000,
        )
        else: self._config = config
        self.estimator = linear_model.ARDRegression(**self._config)

        self.max_iter = HTransparentSpinBox(
            label='Maximum iterations',
            minimum=1, maximum=100000, singleStep=1000,
            getter=lambda: self._config['max_iter'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.alpha_1 = HTransparentDoubleSpinBox(
            label='Alpha 1',
            label2='Shape parameter for the Gamma distribution prior over the alpha parameter',
            minimum=0, maximum=1, singleStep=1e-6, decimals=7,
            getter=lambda: self._config['alpha_1'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.alpha_2 = HTransparentDoubleSpinBox(
            label='Alpha 2',
            label2='Inverse scale parameter (rate parameter) for the Gamma distribution prior over the alpha parameter',
            minimum=0, maximum=1, singleStep=1e-6, decimals=7,
            getter=lambda: self._config['alpha_2'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.lambda_1 = HTransparentDoubleSpinBox(
            label='Lambda 1',
            label2='Shape parameter for the Gamma distribution prior over the lambda parameter',
            minimum=0, maximum=1, singleStep=1e-6, decimals=7,
            getter=lambda: self._config['lambda_1'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.lambda_2 = HTransparentDoubleSpinBox(
            label='Lambda 2',
            label2='Inverse scale parameter (rate parameter) for the Gamma distribution prior over the lambda parameter',
            minimum=0, maximum=1, singleStep=1e-6, decimals=7,
            getter=lambda: self._config['lambda_2'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.threshold_lambda = HTransparentSpinBox(
            label='Threshold lambda',
            label2='Threshold for removing (pruning) weights with high precision from the computation',
            minimum=5000, maximum=100000, singleStep=10000,
            getter=lambda: self._config['threshold_lambda'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['max_iter'] = self.max_iter.get_value()
        self._config['alpha_1'] = self.alpha_1.get_value()
        self._config['alpha_2'] = self.alpha_2.get_value()
        self._config['lambda_1'] = self.lambda_1.get_value()
        self._config['lambda_2'] = self.lambda_2.get_value()
        self._config['threshold_lambda'] = self.threshold_lambda.get_value()
        self.estimator = linear_model.ARDRegression(**self._config)