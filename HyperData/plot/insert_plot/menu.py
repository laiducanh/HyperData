from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon, QAction
import os
from ui.base_widgets.menu import Menu

class Menu_type (Menu):
    sig = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        line = Menu("Line", self)
        line.setIcon(QIcon(os.path.join("UI","Icons","line.png")))
        for i in ['2d line', '2d step']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)

        line.addSeparator()
        for i in ['3d line', '3d step']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)

        line.addSeparator()
        for i in ['fill between', '2d area', '2d stacked area', '2d 100% stacked area']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        line.addSeparator()
        for i in ['3d area']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        
        bar = Menu('Column', self)
        bar.setIcon(QIcon(os.path.join("UI","Icons","bar.png")))
        for i in ['2d column', '2d clustered column', '2d stacked column', '2d 100% stacked column',
                  'marimekko']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)
        bar.addSeparator()
        for i in ['3d column']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)

        scatter = Menu('Scatter', self)
        scatter.setIcon(QIcon(os.path.join("UI","Icons","scatter.png")))
        for i in ['2d scatter', '3d scatter']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)
       
        scatter.addSeparator()
        for i in ['bubble']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)

        pie = Menu('Pie', self)
        pie.setIcon(QIcon(os.path.join("UI","Icons","pie.png")))
        for i in ['pie','doughnut']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)
        pie.addSeparator()
        for i in ['treemap']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)

        stats = Menu('Statistics', self)
        stats.setIcon(QIcon(os.path.join("UI","Icons",'statistics.png')))
        for i in ['histogram','stacked histogram']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)
        stats.addSeparator()
        for i in ['boxplot', 'violinplot']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)

        surface = Menu('Surface', self)
        surface.setIcon(QIcon(os.path.join('UI',"Icons",'surface.png')))
        for i in ['3d surface','triangular 3d surface']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)
        surface.addSeparator()
        for i in ['heatmap']:
            action = QAction(i.title(), self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)

        func = Menu('Function', self)
        func.setIcon(QIcon(os.path.join("UI","Icons","function.png")))
        action = QAction('2D function', self)
        action.triggered.connect(lambda: self.sig.emit('2d function'))
        func.addAction(action)

        none = QAction(QIcon(os.path.join("UI","Icons","none.png")),'None', self)
        none.triggered.connect(lambda: self.sig.emit('none'))


        self.addMenu(line)
        self.addMenu(bar)
        self.addMenu(scatter)
        self.addMenu(pie)
        self.addMenu(stats)
        self.addMenu(surface)
        #self.addMenu(func)
        self.addAction(none)