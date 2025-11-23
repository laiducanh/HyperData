from node_editor.node.regressor.base import RegressorBase
from sklearn import ensemble
from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox

class Voting(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config

        
    def set_estimator(self):
        pass
