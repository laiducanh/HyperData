from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import preprocessing
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import Toggle, PrimaryComboBox, TransparentComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import TransparentSpinBox
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

DEBUG = False

class ExpanderBase(QWidget):
    """ 
    Base class for FeatureExpander 
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create and set a main vertical layout with no margins
        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        # Create a scrollable area and add it to the main layout
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        # Initialize configuration dict and null transfomer
        self._config = dict()

        # Set up configuration
        self.set_config(config=None)
        
    def clear_layout (self):
        # Remove all child widgets from the layout
        while self.vlayout.count():
            item = self.vlayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def set_config(self, config=None):
        # Overwrite in subclass
        # clear_layout is needed before setting up configuration
        self.clear_layout()

class PolynomialFeatures(ExpanderBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        # Default configuration if none provided
        if not config: 
            self._config = dict(
                degree=2,
                interaction_only=False,
                include_bias=True,
            )
        else: 
            self._config = config
  
        # UI Components
        self.degree = TransparentSpinBox(
            text="Degree", 
            text2="Maximal degree of the polynomial features",
            getter=lambda: self._config["degree"],
            setter=lambda v: self._config.update({"degree":v}),
            layout=self.vlayout
        )
        
        self.interaction_only = Toggle(
            text="Interaction features",
            text2="Only interaction features are produced",
            setter=lambda v: self._config.update({"interaction_only":v}),
            getter=lambda: self._config["interaction_only"],
            layout=self.vlayout
        )
        self.include_bias = Toggle(
            text="Bias",
            text2="Add a bias column",
            getter=lambda: self._config["include_bias"],
            setter=lambda v: self._config.update({"include_bias":v}),
            layout=self.vlayout
        )

class SplineTransfomer(ExpanderBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        # Default configuration if none provided
        if not config: 
            self._config = dict(
                n_knots = 5,
                degree = 3,
                knots = "uniform",
                extrapolation = "constant",
                include_bias = True,
            )
        else: 
            self._config = config
        
        # Ui Components 
        self.n_knots = TransparentSpinBox(
            min=2, 
            text="Knots", 
            text2="Number of knots of the plines",
            getter=lambda: self._config["n_knots"],
            setter=self.update_config,
            layout=self.vlayout
        )
        self.degree = TransparentSpinBox(
            text="Degree",
            text2="The polynomial degree of the spline basis",
            getter=lambda: self._config["degree"],
            setter=self.update_config,
            layout=self.vlayout
        )
        self.knots = TransparentComboBox(
            items=["uniform","quantile"], 
            text="Distribution",
            text2="How knot positions are distributed along the features",
            getter=lambda: self._config["knots"],
            setter=self.update_config,
            layout=self.vlayout
        )
        self.extrapolation = TransparentComboBox(
            items=["error","constant","linear","continue","periodic"],
            text="Extrapolation",
            text2="Type of method to extrapolate values",
            getter=lambda: self._config["extrapolation"],
            setter=self.update_config,
            layout=self.vlayout
        )
        self.include_bias = Toggle(
            text="Bias",
            text2="Add a bias column",
            getter=lambda: self._config["include_bias"],
            setter=self.update_config,
            layout=self.vlayout
        )
        
    def update_config(self):
        # Update config from UI elements
        self._config.update(
            n_knots = self.n_knots.button.value(),
            degree = self.degree.button.value(),
            knots = self.knots.button.currentText(),
            extrapolation = self.extrapolation.button.currentText(),
            include_bias = self.include_bias.button.isChecked(),
        )

class FeatureExpander (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            estimator="Polynomial expansion",
            config=dict(),
        )
        
        self.estimator_list = ["Polynomial expansion","Univariate B-spline"]
            
    def currentWidget(self) -> ExpanderBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Feature Expansion", self.parent)
        
        expander = PrimaryComboBox(
            items=self.estimator_list,
            text="Scaler",
            setter=lambda s: self.stackedlayout.setCurrentIndex(self.estimator_list.index(s)),
            getter=lambda: self._config["estimator"],
            layout=dialog.main_layout
        )
        expander.button.setMinimumWidth(250)

        dialog.main_layout.addWidget(SeparateHLine())
    
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(PolynomialFeatures())
        self.stackedlayout.addWidget(SplineTransfomer())
        self.stackedlayout.setCurrentIndex(self.estimator_list.index(expander.button.currentText()))
        self.currentWidget().set_config(self._config["config"])

        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                estimator = expander.button.currentText()
            )
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data.copy()
            X = data.to_numpy()

            if self._config["estimator"] == "Polynomial expansion":
                self.estimator = preprocessing.PolynomialFeatures(**self._config["config"])
            elif self._config["estimator"] == "Univariate B-spline":
                self.estimator = preprocessing.SplineTransformer(**self._config["config"])
            
            data_transformed = self.estimator.fit_transform(X, **self._config["config"])
            columns = [f"Expanded_feature {i+1}" for i in range(data_transformed.shape[1])]
            data = pd.DataFrame(data_transformed, columns=columns)
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.estimator} run successfully.")

            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
     
    def eval (self):
        self.resetNode()
        # reset socket data
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
