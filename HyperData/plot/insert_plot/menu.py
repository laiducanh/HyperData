from PyQt6.QtCore import pyqtSignal
from ui.base_widgets.menu import Menu, Action
from ui.utils import icon

class Menu_type_2D (Menu):
    sig = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        line = Menu("Line", self)
        line.setIcon("line.png")
        for i in ['2d line', '2d step','2d stem']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)

        line.addSeparator()
        for i in ['fill between', '2d area', '2d stacked area', '2d 100% stacked area']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        
        bar = Menu('Column', self)
        bar.setIcon("bar.png")
        for i in ['2d column', '2d clustered column', '2d stacked column', '2d 100% stacked column',
                  'marimekko', 'treemap']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)

        scatter = Menu('Scatter', self)
        scatter.setIcon("scatter.png")
        for i in ['2d scatter']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)
       
        scatter.addSeparator()
        for i in ['2d bubble']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)

        pie = Menu('Pie', self)
        pie.setIcon("pie.png")
        for i in ['pie','doughnut']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)

        stats = Menu('Statistics', self)
        stats.setIcon('statistics.png')
        for i in ['histogram','stacked histogram','hist2d']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)
        stats.addSeparator()
        for i in ['boxplot', 'violinplot','eventplot']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)

        surface = Menu('Surface', self)
        surface.setIcon('surface.png')
        for i in ['heatmap']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)

        func = Menu('Function', self)
        func.setIcon("function.png")
        action = Action(text='2D function', parent=self)
        action.triggered.connect(lambda: self.sig.emit('2d function'))
        func.addAction(action)

        none = Action(icon="delete.png",text='Delete', parent=self)
        none.triggered.connect(lambda: self.sig.emit('delete'))


        self.addMenu(line)
        self.addMenu(bar)
        self.addMenu(scatter)
        self.addMenu(pie)
        self.addMenu(stats)
        self.addMenu(surface)
        #self.addMenu(func)
        self.addAction(none)

class Menu_type_3D (Menu):
    sig = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        line = Menu("Line", self)
        line.setIcon("line.png")
        for i in ['3d line', '3d step','3d stem']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        
        bar = Menu('Column', self)
        bar.setIcon("bar.png")
        for i in ['3d column']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)

        scatter = Menu('Scatter', self)
        scatter.setIcon("scatter.png")
        for i in ['3d scatter']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)
       
        scatter.addSeparator()
        for i in ['3d bubble']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)

        pie = Menu('Pie', self)
        pie.setIcon("pie.png")
        for i in ['pie','doughnut']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)

        stats = Menu('Statistics', self)
        stats.setIcon('statistics.png')
        for i in ['histogram','stacked histogram']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)
        stats.addSeparator()
        for i in ['boxplot', 'violinplot']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)

        surface = Menu('Surface', self)
        surface.setIcon('surface.png')
        for i in ['3d surface','triangular 3d surface']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)
        surface.addSeparator()
        for i in ['heatmap']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)

        func = Menu('Function', self)
        func.setIcon("function.png")
        action = Action(text='2D function', parent=self)
        action.triggered.connect(lambda: self.sig.emit('2d function'))
        func.addAction(action)

        none = Action(icon="delete.png",text='Delete', parent=self)
        none.triggered.connect(lambda: self.sig.emit('delete'))


        self.addMenu(line)
        self.addMenu(bar)
        self.addMenu(scatter)
        self.addMenu(pie)
        self.addMenu(stats)
        self.addMenu(surface)
        #self.addMenu(func)
        self.addAction(none)