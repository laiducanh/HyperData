from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HPrimaryComboBox, HToggle
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from keras import losses
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

DEBUG = False

class AlgorithmBase(QWidget):
    def __init__(self, config, parent = None):
        super().__init__(parent)

        self._config = config
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.initUI()

    def initUI(self):
        pass
        
class BinaryCrossentropy(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

    def initUI(self):
        if not self._config:
            self._config = dict(
                from_logits=False,
                label_smoothing=0.0,
            )
        
        HToggle(
            label='From logits',
            label2='Whether to interpret y_pred as a tensor of logit values',
            getter=lambda: self._config['from_logits'],
            setter=lambda s: self._config.update({'from_logits':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Smoothing',
            label2='Control smoothing label',
            minimum=0, maximum=1, singleStep=0.1, decimals=2,
            getter=lambda: self._config['label_smoothing'],
            setter=lambda s: self._config.update({'label_smoothing':s}),
            layout=self.vlayout
        )

class BinaryFocalCrossentropy(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                apply_class_balancing=False,
                alpha=0.25,
                gamma=2.0,
                from_logits=False,
                label_smoothing=0.0,
            )

        HToggle(
            label='Class balancing',
            label2='Whether to apply weight balancing on the binary classes 0 and 1',
            getter=lambda: self._config['apply_class_balancing'],
            setter=lambda s: self._config.update({'apply_class_balancing':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Weight balancing factor',
            label2='The weight for class 1',
            minimum=0, maximum=1, singleStep=0.1, decimals=2,
            getter=lambda: self._config['alpha'],
            setter=lambda s: self._config.update({'alpha':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Focusing parameter',
            label2='Used to compute the focal factor',
            getter=lambda: self._config['gamma'],
            setter=lambda s: self._config.update({'gamma':s}),
            layout=self.vlayout
        )

        HToggle(
            label='From logits',
            label2='Whether to interpret y_pred as a tensor of logit values',
            getter=lambda: self._config['from_logits'],
            setter=lambda s: self._config.update({'from_logits':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Smoothing',
            label2='Control smoothing label',
            minimum=0, maximum=1, singleStep=0.1, decimals=2,
            getter=lambda: self._config['label_smoothing'],
            setter=lambda s: self._config.update({'label_smoothing':s}),
            layout=self.vlayout
        )

class CategoricalCrossentropy(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

    def initUI(self):
        if not self._config:
            self._config = dict(
                from_logits=False,
                label_smoothing=0.0,
            )
        
        HToggle(
            label='From logits',
            label2='Whether to interpret y_pred as a tensor of logit values',
            getter=lambda: self._config['from_logits'],
            setter=lambda s: self._config.update({'from_logits':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Smoothing',
            label2='Control smoothing label',
            minimum=0, maximum=1, singleStep=0.1, decimals=2,
            getter=lambda: self._config['label_smoothing'],
            setter=lambda s: self._config.update({'label_smoothing':s}),
            layout=self.vlayout
        )

class CategoricalHinge(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class CosineSimilarity(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
class Hinge(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
class Huber(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                delta=1.0
            )

        HTransparentDoubleSpinBox(
            label='Change point',
            label2='The point where Huber loss function changes from a quadratic to linear',
            getter=lambda: self._config['delta'],
            setter=lambda s: self._config.update({'delta':s}),
            layout=self.vlayout
        )

class KLDivergence(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class LogCosh(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class MeanAbsoluteError(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class MeanAbsolutePercentageError(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class MeanSquaredError(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class MeanSquaredLogarithmicError(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class Poisson(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

class SquaredHinge(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
class Loss(QWidget):
    def __init__(self, config:dict, parent=None):
        super().__init__(parent=parent)

        self._config = config
        self.func_list = ['Binary cross-entropy','Binary focal cross-entropy','Categorical cross-entropy',
                          'Categorical hinge','Cosine similarity','Hinge','Huber','Kullback-Leibler divergence',
                          'Logarithm of hyperbolic cosine','Mean of absolute error','Mean absolute percentage error',
                          'Mean squared error','Mean squared logarithmic error','Poisson','Squared Hinge']
        
        self.initUI()
    
    def currentWidget(self) -> AlgorithmBase:
        return self.stackedlayout.currentWidget()       

    def initUI(self):
        self.vlayout = QVBoxLayout(self)
        algorithm = HPrimaryComboBox(
            items=self.func_list,
            label="Function",
            getter=lambda: self._config['loss'],
            setter=lambda s:self.stackedlayout.setCurrentIndex(self.func_list.index(s)),
            layout=self.vlayout
        )
        algorithm.button.setMinimumWidth(400)
        self.vlayout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        self.vlayout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(BinaryCrossentropy(self._config['config']))
        self.stackedlayout.addWidget(BinaryFocalCrossentropy(self._config['config']))
        self.stackedlayout.addWidget(CategoricalCrossentropy(self._config['config']))
        self.stackedlayout.addWidget(CategoricalHinge(self._config['config']))
        self.stackedlayout.addWidget(CosineSimilarity(self._config['config']))
        self.stackedlayout.addWidget(Hinge(self._config['config']))
        self.stackedlayout.addWidget(Huber(self._config['config']))
        self.stackedlayout.addWidget(KLDivergence(self._config['config']))
        self.stackedlayout.addWidget(LogCosh(self._config['config']))
        self.stackedlayout.addWidget(MeanAbsoluteError(self._config['config']))
        self.stackedlayout.addWidget(MeanAbsolutePercentageError(self._config['config']))
        self.stackedlayout.addWidget(MeanSquaredError(self._config['config']))
        self.stackedlayout.addWidget(MeanSquaredLogarithmicError(self._config['config']))
        self.stackedlayout.addWidget(Poisson(self._config['config']))
        self.stackedlayout.addWidget(SquaredHinge(self._config['config']))
        self.stackedlayout.setCurrentIndex(self.func_list.index(self._config['loss']))

    def set_loss(self):
        algorithm = self.func_list[self.stackedlayout.currentIndex()]
        config = self.currentWidget()._config
        self._config.update(
            loss = algorithm,
            config = config
        )
        if algorithm == 'Binary cross-entropy':
            loss = losses.BinaryCrossentropy(**config)
        elif algorithm == 'Binary focal cross-entropy':
            loss = losses.BinaryFocalCrossentropy(**config)
        elif algorithm == 'Categorical cross-entropy':
            loss = losses.CategoricalCrossentropy(**config)
        elif algorithm == 'Categorical hinge':
            loss = losses.CategoricalHinge(**config)
        elif algorithm == 'Cosine similarity':
            loss = losses.CosineSimilarity(**config)
        elif algorithm == 'Hinge':
            loss = losses.Hinge(**config)
        elif algorithm == 'Huber':
            loss = losses.Huber(**config)
        elif algorithm == 'Kullback-Leibler divergence':
            loss = losses.KLDivergence(**config)
        elif algorithm == 'Logarithm of hyperbolic cosine':
            loss = losses.LogCosh(**config)
        elif algorithm == 'Mean of absolute error':
            loss = losses.MeanAbsoluteError(**config)
        elif algorithm == 'Mean absolute percentage error':
            loss = losses.MeanAbsolutePercentageError(**config)
        elif algorithm == 'Mean squared error':
            loss = losses.MeanSquaredError(**config)
        elif algorithm == 'Mean squared logarithmic error':
            loss = losses.MeanSquaredLogarithmicError(**config)
        elif algorithm == 'Poisson':
            loss = losses.Poisson(**config)
        elif algorithm == 'Squared Hinge':
            loss = losses.SquaredHinge(**config)
        
        return loss

    def serialize(self):
        return {"config": self._config,
                "loss": self._loss,
            }

    def deserialize(self, data, hashmap={}):
        self._config = data['config']
        self._loss = data['loss']

