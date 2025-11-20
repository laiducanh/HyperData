from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HTransparentComboBox
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QApplication
from plot.canvas import Canvas

DEBUG = False

class Report(Dialog):
    def __init__(self, histories:list, parent=None):
        super().__init__(title="Model Performance",parent=parent)

        self.clipboard = QApplication.clipboard()
        self.histories = histories
        
        self.fold = HTransparentComboBox(
            items=[f'{str(i+1)}' for i in range(len(histories))],
            label='Fold',
            setter=self.update_plot,
            layout=self.main_layout,
        )

        curve = []
        for key in self.histories[0].history.keys():
            if 'val' in key:
                continue
            curve.append(key)
        self.curve = HTransparentComboBox(
            items=curve,
            label='Curve',
            setter=self.update_plot,
            layout=self.main_layout
        )

        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)
        self.update_plot()
    
    def update_plot(self):
        # clear plot
        self.canvas.figure.clear()

        # add axis
        self.ax = self.canvas.figure.add_subplot()

        if self.histories: 
            history = self.histories[int(self.fold.get_value())-1]

            # drawing
            curve = self.curve.get_value()
            self.ax.plot(history.history[f'{curve}'], label=f'training {curve}')
            self.ax.plot(history.history[f'val_{curve}'], label=f'validation {curve}')

            # show appropriate ticks
            self.ax.set(
            # ... and label them with the respective list entries
            title="Training progress",
            ylabel=curve,
            xlabel='Epoch')

            self.ax.legend()

        self.canvas.draw_idle()