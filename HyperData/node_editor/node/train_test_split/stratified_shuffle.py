from sklearn import model_selection
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class StratifiedShuffleSplit(SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):
        self.clear_layout()

        if not config: self._config = dict(
            n_splits=10,
            test_size=0.2
        )
        else: self._config = config
        self.splitter = model_selection.StratifiedShuffleSplit(**self._config)

        self.splits = SpinBox(min=2, max=1000, step=1, text="number of splits")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.test_size = DoubleSpinBox(min=0, max=1, step=0.01, text="test size")
        self.test_size.button.valueChanged.connect(self.set_splitter)
        self.test_size.button.setValue(self._config["test_size"])
        self.vlayout.addWidget(self.test_size)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["test_size"] = self.test_size.button.value()
        self.splitter = model_selection.StratifiedShuffleSplit(**self._config)