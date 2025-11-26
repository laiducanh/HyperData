from node_editor.node.regressor.base import RegressorBase
from sklearn import linear_model
from ui.base_widgets.button import HToggle

class LinearRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config):
        self.clear_layout()

        if not config: self._config = dict(
            positive = False
        )
        else: self._config = config
        self.estimator = linear_model.LinearRegression(**self._config)

        self.positive = HToggle(
            label="Positive coefficients",
            label2='Whether to force the coefficients to be positive',
            getter=lambda: self._config['positive'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['positive'] = self.positive.get_value()
        self.estimator = linear_model.LinearRegression(**self._config)
