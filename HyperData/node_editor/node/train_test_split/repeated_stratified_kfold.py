from sklearn import model_selection
from ui.base_widgets.spinbox import SpinBox
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class RepeatedStratifiedKFold(SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):
        self.clear_layout()

        if not config: self._config = dict(
            n_splits=5,
            n_repeats=10
        )
        else: self._config = config
        self.splitter = model_selection.RepeatedStratifiedKFold(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of folds")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.repeats = SpinBox(min=1, max=1000, step=1, text="number of repeats")
        self.repeats.button.valueChanged.connect(self.set_splitter)
        self.repeats.button.setValue(self._config["n_repeats"])
        self.vlayout.addWidget(self.repeats)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["n_repeats"] = self.repeats.button.value()
        self.splitter = model_selection.RepeatedStratifiedKFold(**self._config)