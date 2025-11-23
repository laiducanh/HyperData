from node_editor.node.classifier.classifier import ClassifierBase
from sklearn import ensemble
from ui.base_widgets.button import HToggle, HTransparentComboBox

class Stacking(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            stack_method='auto',
            passthrough=False
        )
        else: self._config = config

        self.stack_method = HTransparentComboBox(
            items=['auto','predict_proba','decision_function','predict'],
            label='Method',
            label2='Method called for each base estimator',
            getter=lambda: self._config['stack_method'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.passthrough = HToggle(
            label='Pass through',
            label2='Whether the output estimator is trained on the predictions',
            getter=lambda: self._config['passthrough'],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config['stack_method'] = self.stack_method.get_value()
        self._config['passthrough'] = self.passthrough.get_value()
