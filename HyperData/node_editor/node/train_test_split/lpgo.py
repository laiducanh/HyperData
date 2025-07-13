from sklearn import model_selection
from ui.base_widgets.spinbox import HTransparentSpinBox
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class LeavePGroupOut(SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):
        self.clear_layout()

        if not config: self._config = dict(
            n_groups=2
        )
        else: self._config = config
        self.splitter = model_selection.LeavePGroupsOut(**self._config)

        self.splits = HTransparentSpinBox(minimum=1, maximum=1000, singleStep=1, label="number of groups")
        self.splits.button.setValue(self._config["n_groups"])
        self.splits.button.valueChanged.connect(self.set_splitter)
        self.vlayout.addWidget(self.splits)
    
    def set_splitter(self):
        self._config["n_groups"] = self.splits.button.value()
        self.splitter = model_selection.LeavePGroupsOut(**self._config)