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

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4

class Node(NodeGraphicsNode):
    def __init__(self, title="Undefined Node",parent=None):
        match title:
            case 'Undefined Node':
                super().__init__(title=title, inputs=[SINGLE_IN, MULTI_IN], outputs=[SINGLE_OUT, MULTI_OUT, SINGLE_OUT, SINGLE_OUT])
                self.content = NodeContentWidget(self,parent)
            case 'Figure 2D':
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[])
                self.content = Figure2D(self,parent)
            case 'Figure 3D':
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[])
                self.content = Figure3D(self,parent)
            case 'Data Reader':
                super().__init__(title=title, inputs=[], outputs=[MULTI_OUT])
                self.content = DataReader(self,parent)
            case 'Data Holder':
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataHolder(self,parent)
            case "Data Transpose":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataTranspose(self, parent)
            case 'Data Concator':
                super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
                self.content = DataConcator(self,parent)
            case 'Data Combiner':
                super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
                self.content = DataCombiner(self,parent)
            case 'Data Merge':
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataMerge(self,parent)
            case 'Data Compare':
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataCompare(self,parent)
            case "Data Correlator":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataCorrelator(self,parent)
            case "Data Locator":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataLocator(self,parent)
            case "Data Filter":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataFilter(self,parent)
            case "Data Sorter":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataSorter(self,parent)
            case "Data Inserter":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataInserter(self,parent)
            case "Data Normalizer":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataNormalizer(self,parent)
            case "Data Scaler":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DataScaler(self,parent)
            case "Pairwise Measurer":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
                self.content = PairwiseMeasurer(self,parent)
            case 'Nan Eliminator':
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = NAEliminator(self,parent)
            case 'Nan Imputer':
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = NAImputer(self,parent)
            case "Drop Duplicate":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = DropDuplicate(self,parent)
            case "Label Encoder":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = LabelEncoder(self,parent)
            case "Label Binarizer":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = LabelBinarizer(self,parent)
            case "Ordinal Encoder":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = OrdinalEncoder(self,parent)
            case "One-Hot Encoder":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = OneHotEncoder(self,parent)
            case "Train/Test Splitter":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = TrainTestSplitter(self,parent)
            case "Feature Expander":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
                self.content = FeatureExpander(self,parent)
            case "Classifier":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT, MULTI_OUT])
                self.content = Classifier(self,parent)
            case "Bagging-Classifier":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = BaggingClassifier(self,parent)
            case "Voting-Classifier":
                super().__init__(title=title, inputs=[MULTI_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = VotingClassifier(self,parent)
            case "Meta-Classifier":
                super().__init__(title=title, inputs=[SINGLE_IN, MULTI_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = MetaClassifier(self,parent)
            case "Regressor":
                super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = Regressor(self,parent)
            case "Clustering":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = Clustering(self,parent)
            case "Decomposition":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
                self.content = Decomposition(self,parent)
            case "Predictor":
                super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
                self.content = Predictor(self,parent)
            case "Executor":
                super().__init__(title=title, inputs=[], outputs=[])
                self.content = Executor(self,parent)
            case "Looper":
                super().__init__(title=title, inputs=[], outputs=[])
                self.content = Looper(self,parent)
            case 'User Define Card':
                super().__init__(title=title, inputs=[], outputs=[])
                self.content = UserDefine(self,parent)
        
        self.menu = self.content.menu
        self.set_Content(self.content)

    

    