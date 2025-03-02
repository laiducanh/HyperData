from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.node.data.data import *
from node_editor.node.data_cleaning.data_cleaning import *
from node_editor.node.data_encoder.data_encoder import *
from node_editor.node.classifier.classifier import Classifier
from node_editor.node.classifier.meta_classifier import MetaClassifier, BaggingClassifier, VotingClassifier
from node_editor.node.regressor.regressor import Regressor
from node_editor.node.clustering.clustering import Clustering
from node_editor.node.decomposition.decomposition import Decomposition
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from node_editor.node.figure import *
from node_editor.node.predictor import Predictor
from node_editor.node.misc.misc import *
from node_editor.node.deep_learning.deep_learning import *

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4

class Node(NodeGraphicsNode):
    def __init__(self, title="Undefined Node",parent=None):
        if title == 'Undefined Node':
            super().__init__(title=title, inputs=[SINGLE_IN, MULTI_IN], outputs=[SINGLE_OUT, MULTI_OUT, SINGLE_OUT, SINGLE_OUT])
            self.content = NodeContentWidget(self,parent)
        elif title == 'Figure 2D':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = Figure2D(self,parent)
        elif title == 'Figure 3D':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = Figure3D(self,parent)
        elif title == 'Multi-Figure':
            super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
            self.content = MultiFigure(self,parent)
        elif title == 'Data Reader':
            super().__init__(title=title, inputs=[], outputs=[MULTI_OUT])
            self.content = DataReader(self,parent)
        elif title == 'Data Holder':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataHolder(self,parent)
        elif title == "Data Transpose":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataTranspose(self, parent)
        elif title == 'Data Concator':
            super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
            self.content = DataConcator(self,parent)
        elif title == 'Data Combiner':
            super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
            self.content = DataCombiner(self,parent)
        elif title == 'Data Merge':
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataMerge(self,parent)
        elif title == 'Data Compare':
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataCompare(self,parent)
        elif title == "Data Correlator":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataCorrelator(self,parent)
        elif title == "Data Locator":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataLocator(self,parent)
        elif title == "Data Filter":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataFilter(self,parent)
        elif title == "Data Sorter":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataSorter(self,parent)
        elif title == "Data Inserter":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataInserter(self,parent)
        elif title == "Data Normalizer":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataNormalizer(self,parent)
        elif title == "Data Scaler":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataScaler(self,parent)
        elif title == "Data Pivot":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataPivot(self,parent)
        elif title == "Data Unpivot":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataUnpivot(self,parent)
        elif title == "Data Stack":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataStack(self,parent)
        elif title == "Data Unstack":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataUnstack(self,parent)
        elif title == "Pairwise Measurer":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = PairwiseMeasurer(self,parent)
        elif title == 'Nan Eliminator':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = NAEliminator(self,parent)
        elif title == 'Nan Imputer':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = NAImputer(self,parent)
        elif title == "Drop Duplicate":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DropDuplicate(self,parent)
        elif title == "Label Encoder":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = LabelEncoder(self,parent)
        elif title == "Label Binarizer":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = LabelBinarizer(self,parent)
        elif title == "Ordinal Encoder":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = OrdinalEncoder(self,parent)
        elif title == "One-Hot Encoder":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = OneHotEncoder(self,parent)
        elif title == "Train/Test Splitter":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = TrainTestSplitter(self,parent)
        elif title == "Feature Expander":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = FeatureExpander(self,parent)
        elif title == "Classifier":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT, MULTI_OUT])
            self.content = Classifier(self,parent)
        elif title == "Bagging-Classifier":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = BaggingClassifier(self,parent)
        elif title == "Voting-Classifier":
            super().__init__(title=title, inputs=[MULTI_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = VotingClassifier(self,parent)
        elif title == "Meta-Classifier":
            super().__init__(title=title, inputs=[SINGLE_IN, MULTI_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = MetaClassifier(self,parent)
        elif title == "Regressor":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = Regressor(self,parent)
        elif title == "Clustering":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = Clustering(self,parent)
        elif title == "Decomposition":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = Decomposition(self,parent)
        elif title == "Feature Selector":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = FeatureSelector(self,parent)
        elif title == "Predictor":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = Predictor(self,parent)
        elif title == "Input Layer":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = InputLayer(self,parent)
        elif title == "Dense Layer":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DenseLayer(self,parent)
        elif title == "DL Model":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DLModel(self,parent)
        elif title == "Executor":
            super().__init__(title=title, inputs=[], outputs=[])
            self.content = Executor(self,parent)
        elif title == "Looper":
            super().__init__(title=title, inputs=[], outputs=[])
            self.content = Looper(self,parent)
        elif title == 'User Define Card':
            super().__init__(title=title, inputs=[], outputs=[])
            self.content = UserDefine(self,parent)
        
        self.menu = self.content.menu
        self.set_Content(self.content)

    

    