from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HPrimaryComboBox, HToggle
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from keras import optimizers
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
        
class Adadelta(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                rho=0.95,
                epsilon=1e-07,
            )
        
        HTransparentDoubleSpinBox(
            label='Learning rate',
            label2='Adadelta tends to benefit from higher initial learning values',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Decay rate',
            minimum=0.0, singleStep=0.5, decimals=4,
            getter=lambda: self._config['rho'],
            setter=lambda s: self._config.update({'rho': s}),
            layout=self.vlayout
        )

class Adagrad(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                initial_accumulator_value=0.1,
                epsilon=1e-07,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            label2='Adagrad tends to benefit from higher initial learning values',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Initial accumulator',
            label2='Starting value for the accumulators (per-parameter momentum values)',
            minimum=0.0, singleStep=0.1, decimals=2,
            getter=lambda: self._config['initial_accumulator_value'],
            setter=lambda s: self._config.update({'initial_accumulator_value':s}),
            layout=self.vlayout
        )

class Adam(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)

    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                epsilon=1e-07,
                amsgrad=False,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Exponential decay rate 1',
            label2='The exponential decay rate for the 1st moment estimates',
            minimum=-100, maximum=100, decimals=4, singleStep=0.5,
            getter=lambda: self._config['beta_1'],
            setter=lambda s: self._config.update({'beta_1':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Exponential decay rate 2',
            label2='The exponential decay rate for the 2nd moment estimates',
            minimum=-100, maximum=100, decimals=4, singleStep=0.5,
            getter=lambda: self._config['beta_2'],
            setter=lambda s: self._config.update({'beta_2':s}),
            layout=self.vlayout
        )

        HToggle(
            label='Use AMSGrad',
            label2='Whether to apply AMSGrad variant of this algorithm',
            getter=lambda: self._config['amsgrad'],
            setter=lambda s: self._config.update({'amsgrad':s}),
            layout=self.vlayout
        )

class Adamax(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                epsilon=1e-07,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Exponential decay rate 1',
            label2='The exponential decay rate for the 1st moment estimates',
            minimum=-100, maximum=100, decimals=4, singleStep=0.5,
            getter=lambda: self._config['beta_1'],
            setter=lambda s: self._config.update({'beta_1':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Exponential decay rate 2',
            label2='The exponential decay rate for the 2nd moment estimates',
            minimum=-100, maximum=100, decimals=4, singleStep=0.5,
            getter=lambda: self._config['beta_2'],
            setter=lambda s: self._config.update({'beta_2':s}),
            layout=self.vlayout
        )

class Ftrl(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                learning_rate_power=-0.5,
                initial_accumulator_value=0.1,
                l1_regularization_strength=0.0,
                l2_regularization_strength=0.0,
                l2_shrinkage_regularization_strength=0.0,
                beta=0.0,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Power',
            label2=' Controls how the learning rate decreases during training. Use zero for a fixed learning rate',
            minimum=-100, maximum=0.0, singleStep=0.5, decimals=2,
            getter=lambda: self._config['learning_rate_power'],
            setter=lambda s: self._config.update({'learning_rate_power':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Initial accumulator',
            label2='Starting value for the accumulators (per-parameter momentum values)',
            minimum=0.0, singleStep=0.1, decimals=2,
            getter=lambda: self._config['initial_accumulator_value'],
            setter=lambda s: self._config.update({'initial_accumulator_value':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='L1 regularization',
            minimum=0, maximum=100, singleStep=0.1, decimals=2,
            getter=lambda: self._config['l1_regularization_strength'],
            setter=lambda s: self._config.update({'l1_regularization_strength':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='L2 regularization',
            minimum=0, maximum=100, singleStep=0.1, decimals=2,
            getter=lambda: self._config['l2_regularization_strength'],
            setter=lambda s: self._config.update({'l2_regularization_strength':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='L2 shrinkage',
            minimum=0, maximum=100, singleStep=0.1, decimals=2,
            getter=lambda: self._config['l2_shrinkage_regularization_strength'],
            setter=lambda s: self._config.update({'l2_shrinkage_regularization_strength':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Beta',
            minimum=-100, singleStep=0.5, decimals=2,
            getter=lambda: self._config['beta'],
            setter=lambda s: self._config.update({'beta':s}),
            layout=self.vlayout
        )

class Nadam(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                epsilon=1e-07,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Exponential decay rate 1',
            label2='The exponential decay rate for the 1st moment estimates',
            minimum=-100, maximum=100, decimals=4, singleStep=0.5,
            getter=lambda: self._config['beta_1'],
            setter=lambda s: self._config.update({'beta_1':s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Exponential decay rate 2',
            label2='The exponential decay rate for the 2nd moment estimates',
            minimum=-100, maximum=100, decimals=4, singleStep=0.5,
            getter=lambda: self._config['beta_2'],
            setter=lambda s: self._config.update({'beta_2':s}),
            layout=self.vlayout
        )

class RMSprop(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.001,
                rho=0.9,
                momentum=0.0,
                epsilon=1e-07,
                centered=False,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Decay rate',
            label2='Discounting factor for the history/coming gradient',
            minimum=0.0, singleStep=0.5, decimals=4,
            getter=lambda: self._config['rho'],
            setter=lambda s: self._config.update({'rho': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Momentum',
            minimum=0, 
            getter=lambda: self._config['momentum'],
            setter=lambda s: self._config.update({'momentum':s}),
            layout=self.vlayout
        )

        HToggle(
            label='Centered',
            label2='Whether gradients are normalized by the estimated variance of the gradient',
            getter=lambda: self._config['centered'],
            setter=lambda s: self._config.update({'centered':s}),
            layout=self.vlayout
        )

class SGD(AlgorithmBase):
    def __init__(self, config, parent=None):
        super().__init__(config, parent)
    
    def initUI(self):
        if not self._config:
            self._config = dict(
                learning_rate=0.01,
                momentum=0.0,
                nesterov=False,
            )

        HTransparentDoubleSpinBox(
            label='Learning rate',
            minimum=0.0, singleStep=0.005, decimals=4,
            getter=lambda: self._config['learning_rate'],
            setter=lambda s: self._config.update({'learning_rate': s}),
            layout=self.vlayout
        )

        HTransparentDoubleSpinBox(
            label='Momentum',
            label2='Accelerate gradient descent in the relevant direction and dampens oscillations',
            minimum=0, 
            getter=lambda: self._config['momentum'],
            setter=lambda s: self._config.update({'momentum':s}),
            layout=self.vlayout
        )

        HToggle(
            label='Nesterov momentum',
            label2='Whether to apply Nesterov momentum',
            getter=lambda: self._config['nesterov'],
            setter=lambda s: self._config.update({'nesterov':s}),
            layout=self.vlayout
        )

class Optimizer(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.label.hide()
        self.node.output_sockets[0].setSocketLabel("Optimizer")
        
        self._config = dict(
            optimizer = "Adam",
            config = dict(),
        )
        
        self.optimizer_list = ["Adadelta", "Adagrad", "Adam", "Adamax",
                               "Ftrl", "Nadam", "RMSprop", "SGD"]
        
    
    def currentWidget(self) -> AlgorithmBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.main_layout.addWidget(TitleLabel('Optimizer'))
        dialog.main_layout.addWidget(SeparateHLine())
        algorithm = HPrimaryComboBox(
            items=self.optimizer_list,
            label="Algorithm",
            getter=lambda: self._config['optimizer'],
            setter=lambda s:self.stackedlayout.setCurrentIndex(self.optimizer_list.index(s)),
            layout=dialog.main_layout
        )
        dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(Adadelta(self._config['config']))
        self.stackedlayout.addWidget(Adagrad(self._config['config']))
        self.stackedlayout.addWidget(Adam(self._config['config']))
        self.stackedlayout.addWidget(Adamax(self._config['config']))
        self.stackedlayout.addWidget(Ftrl(self._config['config']))
        self.stackedlayout.addWidget(Nadam(self._config['config']))
        self.stackedlayout.addWidget(RMSprop(self._config['config']))
        self.stackedlayout.addWidget(SGD(self._config['config']))
        self.stackedlayout.setCurrentIndex(self.optimizer_list.index(self._config['optimizer']))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                optimizer = algorithm.get_value()
            )
            self.exec()

    def func(self):
        self.eval()
        try:
            algorithm = self._config['optimizer']
            config = self._config['config']
            if algorithm == 'Adadelta':
                optimizer = optimizers.Adadelta(**config)
            elif algorithm == 'Adafactor':
                optimizer = optimizers.Adafactor(**config)
            elif algorithm == 'Adagrad':
                optimizer = optimizers.Adagrad(**config)
            elif algorithm == 'Adam':
                optimizer = optimizers.Adam(**config)
            elif algorithm == 'AdamW':
                optimizer = optimizers.AdamW(**config)
            elif algorithm == 'Adamax':
                optimizer = optimizers.Adamax(**config)
            elif algorithm == 'Ftrl':
                optimizer = optimizers.Ftrl(**config)
            elif algorithm == 'Lion':
                optimizer = optimizers.Lion(**config)
            elif algorithm == 'Nadam':
                optimizer = optimizers.Nadam(**config)
            elif algorithm == 'RMSprop':
                optimizer = optimizers.RMSprop(**config)
            elif algorithm == 'SGD':
                optimizer = optimizers.SGD(**config)

            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: created {algorithm} optimizer successfully.")

        except Exception as e:
            optimizer = None
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return None.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = optimizer

    def serialize(self):
        return {"config": self._config['config'],
                "optimizer": self._config['optimizer'],
                "comment": self.comment.toPlainText(),
            }

    def deserialize(self, data, hashmap={}):
        super().deserialize(data)
        self._config['config'] = data['config']
        self._config['optimizer'] = data['optimizer']
        self.comment.setText(data['comment'])
