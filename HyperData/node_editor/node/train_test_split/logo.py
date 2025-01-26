from sklearn import model_selection
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.base import SplitterBase

DEBUG = False

class LeaveOneGroupOut(SplitterBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        self.set_splitter()
    
    def set_splitter(self):
        self.splitter = model_selection.LeaveOneGroupOut()