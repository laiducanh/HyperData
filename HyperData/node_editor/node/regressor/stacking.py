from node_editor.node.regressor.base import RegressorBase
from sklearn import ensemble
from ui.base_widgets.button import HToggle, HTransparentComboBox

class Stacking(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            passthrough=False
        )
        else: self._config = config

        self.passthrough = HToggle(
            label='Pass through',
            label2='Whether the output estimator is trained on the predictions',
            getter=lambda: self._config['passthrough'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['passthrough'] = self.passthrough.get_value()
