from sklearn import model_selection
from ui.base_widgets.spinbox import HTransparentSpinBox, HTransparentDoubleSpinBox
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class GroupShuffleSplit (SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):
        
        self.clear_layout()

        if not config: self._config = dict(
            n_splits=5,
            test_size=0.2
        )
        else: self._config = config
        self.splitter = model_selection.GroupShuffleSplit(**self._config)

        self.splits = HTransparentSpinBox(minimum=2, maximum=1000, singleStep=1, label="number of splits")
        self.splits.button.setValue(self._config["n_splits"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
        self.test_size = HTransparentDoubleSpinBox(minimum=0, maximum=1, singleStep=0.01, label="test size")
        self.test_size.button.valueChanged.connect(self.set_splitter)
        self.test_size.button.setValue(self._config["test_size"])
        self.vlayout.addWidget(self.test_size)
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self._config["test_size"] = self.test_size.button.value()
        self.splitter = model_selection.GroupShuffleSplit(**self._config)