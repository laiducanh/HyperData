from sklearn import model_selection
from ui.base_widgets.spinbox import HTransparentSpinBox
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class GroupKFold(SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_splits=5
        )
        else: self._config = config
        self.splitter = model_selection.GroupKFold(**self._config)
    
        self.splits = HTransparentSpinBox(
            minimum=2, maximum=1000, singleStep=1, 
            label="Number of folds",
            getter=lambda: self._config['n_splits'],
            setter=self.set_splitter,
            layout=self.vlayout
        )
    
    def set_splitter(self):
        self._config["n_splits"] = self.splits.button.value()
        self.splitter = model_selection.GroupKFold(**self._config)