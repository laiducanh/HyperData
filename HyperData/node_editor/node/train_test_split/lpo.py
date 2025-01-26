from sklearn import model_selection
from ui.base_widgets.spinbox import SpinBox
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class LeavePOut(SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):
        self.clear_layout()

        if not config: self._config = dict(
            p=2
        )
        else: self._config = config
        self.splitter = model_selection.LeavePOut(**self._config)

        self.splits = SpinBox(min=1, max=1000, step=1, text="number of samples")
        self.splits.button.setValue(self._config["p"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
    
    def set_splitter(self):
        self._config["p"] = self.splits.button.value()
        self.splitter = model_selection.LeavePOut(**self._config)