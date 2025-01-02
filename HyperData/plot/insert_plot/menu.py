from PySide6.QtCore import Signal
from ui.base_widgets.menu import Menu, Action


class Menu_type_2D (Menu):
    sig = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        from plot.insert_plot.utilis import (icon_line, icon_bar, icon_scatter, icon_pie, 
                                            icon_statistics,icon_surface, icon_none, icon_function)

        line = Menu("Line", self)
        line.setIcon(icon_line)
        for i in ['2d line', '2d step','2d stem']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        
        line.addSeparator()
        for i in ['fill between', '2d area', '2d stacked area', '2d 100% stacked area']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        
        bar = Menu('Column', self)
        bar.setIcon(icon_bar)
        for i in ['2d column', '2d clustered column', '2d stacked column', '2d 100% stacked column']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)
        bar.addSeparator()
        for i in ['dot','clustered dot','stacked dot','dumbbell']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)
        bar.addSeparator()
        for i in ['marimekko', 'treemap']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)

        scatter = Menu('Scatter', self)
        scatter.setIcon(icon_scatter)
        for i in ['2d scatter']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)
       
        scatter.addSeparator()
        for i in ['2d bubble']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)

        pie = Menu('Pie', self)
        pie.setIcon(icon_pie)
        for i in ['pie','coxcomb']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)
        pie.addSeparator()
        for i in ['doughnut','multilevel doughnut','semicircle doughnut']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)

        stats = Menu('Statistics', self)
        stats.setIcon(icon_statistics)
        for i in ['histogram','stacked histogram','hist2d']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)
        stats.addSeparator()
        for i in ['boxplot', 'violinplot','eventplot']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)

        surface = Menu('Surface', self)
        surface.setIcon(icon_surface)
        for i in ['heatmap']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)

        func = Menu('Function', self)
        func.setIcon(icon_function)
        action = Action(text='2D function', parent=self)
        action.triggered.connect(lambda: self.sig.emit('2d function'))
        func.addAction(action)

        none = Action(icon=icon_none,text='Delete', parent=self)
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
    sig = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        from plot.insert_plot.utilis import (icon_line, icon_bar, icon_scatter, icon_pie, 
                                            icon_statistics,icon_surface, icon_none, icon_function)

        line = Menu("Line", self)
        line.setIcon(icon_line)
        for i in ['3d line', '3d step','3d stem']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            line.addAction(action)
        
        bar = Menu('Column', self)
        bar.setIcon(icon_bar)
        for i in ['3d column']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            bar.addAction(action)

        scatter = Menu('Scatter', self)
        scatter.setIcon(icon_scatter)
        for i in ['3d scatter']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)
       
        scatter.addSeparator()
        for i in ['3d bubble']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            scatter.addAction(action)

        pie = Menu('Pie', self)
        pie.setIcon(icon_pie)
        for i in ['pie','doughnut']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            pie.addAction(action)

        stats = Menu('Statistics', self)
        stats.setIcon(icon_statistics)
        for i in ['histogram','stacked histogram']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)
        stats.addSeparator()
        for i in ['boxplot', 'violinplot']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            stats.addAction(action)

        surface = Menu('Surface', self)
        surface.setIcon(icon_surface)
        for i in ['3d surface','triangular 3d surface']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)
        surface.addSeparator()
        for i in ['heatmap']:
            action = Action(text=i.title(), parent=self)
            action.triggered.connect(lambda _, type=i: self.sig.emit(type.lower()))
            surface.addAction(action)

        func = Menu('Function', self)
        func.setIcon(icon_function)
        action = Action(text='2D function', parent=self)
        action.triggered.connect(lambda: self.sig.emit('2d function'))
        func.addAction(action)

        none = Action(icon=icon_none,text='Delete', parent=self)
        none.triggered.connect(lambda: self.sig.emit('delete'))


        self.addMenu(line)
        self.addMenu(bar)
        self.addMenu(scatter)
        self.addMenu(pie)
        self.addMenu(stats)
        self.addMenu(surface)
        #self.addMenu(func)
        self.addAction(none)