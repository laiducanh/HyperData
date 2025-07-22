from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from plot.canvas import Canvas
from ui.base_widgets.text import TitleLabel, BodyLabel
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.button import TransparentComboBox, TransparentPushButton, PrimaryComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.frame import Frame, ScrollArea
from node_editor.base.node_graphics_node import NodeGraphicsNode
from matplotlib import gridspec
from mpl_toolkits.mplot3d.axes3d import Axes3D
from plot.copy_objects import copy_Axes, copy_Drawings, copy_Figure

class SubFigure(Frame):
    sig = Signal()
    def __init__(self, subfig_idx=0, total_fig=None, 
                 rows=None, cols=None, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        # layout.setContentsMargins(0,0,0,0)
        self.subfig_idx = subfig_idx
        self.total_fig = total_fig
        self.rows = rows
        self.cols = cols

        hlayout1 = QHBoxLayout()
        layout.addLayout(hlayout1)

        hlayout1.addWidget(TitleLabel(f"Subfigure {subfig_idx+1}"))
        hlayout1.addStretch()
        self.fig = PrimaryComboBox()
        self.fig.setMinimumWidth(150)
        self.fig.currentTextChanged.connect(lambda: self.sig.emit())
        hlayout1.addWidget(self.fig)

        hlayout2 = QHBoxLayout()
        layout.addLayout(hlayout2)

        hlayout2.addWidget(BodyLabel("Row"))
        hlayout2.addStretch()
        self.row1 = TransparentComboBox()
        self.row1.setMinimumWidth(100)
        self.row1.currentTextChanged.connect(lambda: self.sig.emit())
        hlayout2.addWidget(self.row1)
        hlayout2.addWidget(BodyLabel("\u2192"))
        self.row2 = TransparentComboBox()
        self.row2.setMinimumWidth(100)
        self.row2.currentTextChanged.connect(lambda: self.sig.emit())
        hlayout2.addWidget(self.row2)

        hlayout3 = QHBoxLayout()
        layout.addLayout(hlayout3)

        hlayout3.addWidget(BodyLabel("Column"))
        hlayout3.addStretch()
        self.col1 = TransparentComboBox()
        self.col1.setMinimumWidth(100)
        self.col1.currentTextChanged.connect(lambda: self.sig.emit())
        hlayout3.addWidget(self.col1)
        hlayout3.addWidget(BodyLabel("\u2192"))
        self.col2 = TransparentComboBox()
        self.col2.setMinimumWidth(100)
        self.col2.currentTextChanged.connect(lambda: self.sig.emit())
        hlayout3.addWidget(self.col2)

        layout.addWidget(SeparateHLine())

        self.update_layout(self.total_fig, self.rows, self.cols)
    
    def update_layout(self, total_fig=None, rows=None, cols=None):
        fig = self.fig.currentText()
        row1 = self.row1.currentText()
        row2 = self.row2.currentText()
        col1 = self.col1.currentText()
        col2 = self.col2.currentText()
        self.fig.currentTextChanged.disconnect()
        self.row1.currentTextChanged.disconnect()
        self.row2.currentTextChanged.disconnect()
        self.col1.currentTextChanged.disconnect()
        self.col2.currentTextChanged.disconnect()

        self.fig.clear()
        self.row1.clear()
        self.row2.clear()
        self.col1.clear()
        self.col2.clear()
        self.total_fig = total_fig
        self.rows = rows
        self.cols = cols
        

        self.fig.addItems(["None"]+[f"Figure {i+1}" for i in range(total_fig)])
        self.row1.addItems([f"{i+1}" for i in range(rows)])
        self.row2.addItems([f"{i+1}" for i in range(rows)])
        self.col1.addItems([f"{i+1}" for i in range(cols)])
        self.col2.addItems([f"{i+1}" for i in range(cols)])

        self.fig.setCurrentText(fig)
        self.row1.setCurrentText(row1)
        self.row2.setCurrentText(row2)
        self.col1.setCurrentText(col1)
        self.col2.setCurrentText(col2)

        self.fig.currentTextChanged.connect(lambda: self.sig.emit())
        self.row1.currentTextChanged.connect(lambda: self.sig.emit())
        self.row2.currentTextChanged.connect(lambda: self.sig.emit())
        self.col1.currentTextChanged.connect(lambda: self.sig.emit())
        self.col2.currentTextChanged.connect(lambda: self.sig.emit())
    
class Layout(ScrollArea):
    def __init__(self, node: NodeGraphicsNode, canvas:Canvas, parent=None):
        super().__init__(parent=parent)

        # self.verticalScrollBar().setValue(1900)
        self.verticalScrollBar().rangeChanged.connect(lambda min, max: self.verticalScrollBar().setSliderPosition(max))
        self.canvas = canvas
        self.node = node
        self.total_figs = len(self.node.input_sockets[0].socket_data)
        self.current_idx = 0

        self.vlayout.addWidget(TitleLabel("Grid"))
        self.vlayout.addWidget(SeparateHLine())

        self.rows = HTransparentSpinBox(
            label="Rows", 
            minimum=1,
            setter=self.update_layout,
            layout=self.vlayout
        )

        self.cols = HTransparentSpinBox(
            label="Columns", 
            minimum=1,
            setter=self.update_layout,
            layout=self.vlayout
        )

        self.vlayout.addWidget(SeparateHLine())
        add_btn = TransparentPushButton()
        add_btn.setIcon("add.png")
        add_btn.pressed.connect(self.add_subfigure)
        self.vlayout.addWidget(add_btn)

        self.update_layout()
  
    def redraw_plot(self):
        for sub in self.findChildren(SubFigure):
            self.redraw_subplot(sub)
                    
    def redraw_subplot(self, sub:SubFigure):

        self.canvas.figure.clear()
        
        gs = gridspec.GridSpec(
            nrows=self.nrows,
            ncols=self.ncols,
        )

        row1, row2 = sub.row1.currentIndex(), sub.row2.currentIndex()
        col1, col2 = sub.col1.currentIndex(), sub.col2.currentIndex()
        fig_idx = sub.fig.currentIndex()
        proj3d = False

        if fig_idx > 0:
            canvas: Canvas = self.node.input_sockets[0].socket_data[fig_idx-1]
            proj3d = isinstance(canvas.axes, Axes3D)          
        
        if row2 >= row1 and col2 >= col1:
            if row1 == row2 and col1 == col2:
                subfig = self.canvas.figure.add_subfigure(gs[row1, col1])
            elif row1 == row2:
                subfig = self.canvas.figure.add_subfigure(gs[row1, col1:col2+1])
            elif col1 == col2:
                subfig = self.canvas.figure.add_subfigure(gs[row1:row2+1, col1])
            else:
                subfig = self.canvas.figure.add_subfigure(gs[row1:row2+1, col1:col2+1])   
            
            if fig_idx > 0:
                if not proj3d:
                    ax = subfig.add_subplot()
                    axy2 = ax.twinx()
                    axx2 = ax.twiny()
                    axpie = subfig.add_subplot()
                    axpolar = subfig.add_subplot(projection='polar')
                    axleg = subfig.add_subplot(gid='legend axes')
                     
                else:
                    ax = subfig.add_subplot(projection='3d', gid='legend axes')   

            copy_Figure(canvas.figure, subfig)

        self.canvas.draw_idle()

    def update_layout(self):
        self.nrows = self.rows.button.value()
        self.ncols = self.cols.button.value()
        self.total_figs = len(self.node.input_sockets[0].socket_data)

        for sub in self.findChildren(SubFigure):
            sub: SubFigure
            sub.update_layout(self.total_figs, self.nrows, self.ncols)

        self.redraw_plot()
    
    def add_subfigure(self):
        newfig = SubFigure(self.current_idx, self.total_figs, self.nrows, self.ncols, self)
        newfig.sig.connect(lambda: self.redraw_subplot(newfig))
        self.vlayout.insertWidget(self.vlayout.count()-1, newfig)
        self.current_idx += 1
        self.redraw_plot()
    
    def showEvent(self, event):
        self.update_layout()
        return super().showEvent(event)


