from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HButton
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from plot.canvas import Canvas

class TestBase (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)   

        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        self._config = dict()
        self.set_config(config=None)
        
    def clear_layout (self):
        for i in reversed(range(self.vlayout.count())):
            item = self.vlayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, HButton):
                self.vlayout.removeWidget(widget)
                widget.deleteLater()
    
    def set_config(self, config=None):
        self.clear_layout()
    
    def update_config(self):
        pass

    def result_dialog(self, title, samples, result):
        pass

class ResultDialogBase(Dialog):
    def __init__(self, title:str, samples=None, result=None, parent=None):
        super().__init__(parent)

        self.samples = samples
        self._result = result
        self.title = title

        self.setWindowTitle(title)
        
        if result:
            self.initStats(result)
            self.main_layout.addWidget(SeparateHLine())
            self.initPlot(samples)
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
    
    def initStats(self, result):
        pass

    def initPlot(self, samples):
        self.canvas = Canvas()
        self.main_layout.addWidget(self.canvas)
        for _ax in self.canvas.figure.axes: _ax.remove()
        self.plot(samples)
    
    def plot(self, samples):
        # clear plot
        self.canvas.figure.clear()

        # add axis
        self.ax = self.canvas.figure.add_subplot()

        for idx, sample in enumerate(samples):
            self.ax.hist(
                sample,
                bins='auto',
                label=f'Sample {idx+1}',
                histtype='stepfilled', 
                alpha=0.2
            )

        self.ax.legend()
        self.ax.set_title(self.title)
        self.canvas.draw_idle()