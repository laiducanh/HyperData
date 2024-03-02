from PyQt6.QtWidgets import QListWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QWidget, QLabel, QMainWindow
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
import os, qfluentwidgets
from ui.base_widgets.button import _PrimaryPushButton
from ui.base_widgets.text import StrongBodyLabel, TitleLabel, BodyLabel
from ui.base_widgets.separator import SeparateHLine

class Plottype_Button (_PrimaryPushButton):
    sig = pyqtSignal(str)
    def __init__(self,type,icon_size,tooltip):
        super().__init__()
        self.type = type
        self.setText((self.type).title())
        #self.setIconSize(QSize(icon_size,icon_size))
        self.setMaximumWidth(50)
        self.setToolTip(tooltip)
        self.setToolTipDuration(1000)
        #self.setFixedSize(QSize(icon_size,icon_size))
        self.installEventFilter(qfluentwidgets.ToolTipFilter(self, 0, qfluentwidgets.ToolTipPosition.BOTTOM))
        self.setMaximumWidth(200)
        self.clicked.connect(lambda: self.sig.emit(self.type))
        


class SideBar (qfluentwidgets.ListWidget):
    sig = pyqtSignal()
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.setFixedWidth(150)
        self.addItems(['Line Graphs','Column Graphs','Scatter Graphs','Pie Graphs','Statistics Graphs','Surface Graphs'])
        self.setCurrentRow(0)
    

class Line (QWidget):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(TitleLabel('Line Graphs'))
        text = BodyLabel("A line graph "
            "can show continuous data over time on an "
            "evenly scaled axis, so they're ideal for "
            "showing trends in data at equal intervals.")
        text.setWordWrap(True)
        
        layout2.addWidget(text)
        fig = QLabel()
        pixmap = QPixmap(os.path.join("UI","Plot","line.png"))
        #pixmap = pixmap.scaled(400,400)
        fig.setPixmap(pixmap)
        fig.setFixedWidth(100)
        layout1.addWidget(fig)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('2D Line'))
        layout_line2d = QHBoxLayout()
        layout_line2d.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layout_line2d)
        for i in ['2d line','2d step']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_line2d.addWidget(button)
        #layout_line2d.addStretch()
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('3D Line'))
        layout_line3d = QHBoxLayout()
        layout_line3d.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layout_line3d)
        for i in ['3d line','3d step']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_line3d.addWidget(button)
        #layout_line3d.addStretch()
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('2D Area'))
        layout_line2darea = QHBoxLayout()
        layout_line2darea.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for i in ['fill between','2d area','2d stacked area', "2d 100% stacked area"]:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_line2darea.addWidget(button)
        layout.addLayout(layout_line2darea)
        #layout_line2darea.addStretch()
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('3D Area'))
        layout_line3darea = QHBoxLayout()
        for i in ['3d area']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_line3darea.addWidget(button)
        layout.addLayout(layout_line3darea)
        layout_line3darea.addStretch()
        layout.addStretch()
        

class Bar (QWidget):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(TitleLabel('Column Graphs'))
        text = BodyLabel("Column graphs illustrate the comparisons among discrete data. "
        "The length of the columns is proportionally related to the categorial data.")
        text.setWordWrap(True)
        
        layout2.addWidget(text)
        fig = QLabel()
        pixmap = QPixmap(os.path.join("UI","Plot","bar.png"))
        #pixmap = pixmap.scaled(400,400)
        fig.setPixmap(pixmap)
        fig.setFixedWidth(100)
        layout1.addWidget(fig)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('2D Column'))
        layout_column2d_1 = QHBoxLayout()
        layout_column2d_1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layout_column2d_1)
        for i in ['2d column','2d clustered column','2d stacked column']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_column2d_1.addWidget(button)
        layout_column2d_2 = QHBoxLayout()
        layout_column2d_2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layout_column2d_2)
        for i in ['2d 100% stacked column','marimekko']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_column2d_2.addWidget(button)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('3D Column'))
        layout_column3d = QHBoxLayout()
        layout.addLayout(layout_column3d)
        for i in ['3d column']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_column3d.addWidget(button)
        layout_column3d.addStretch()
        #layout.addWidget(SeparateHLine())
        layout.addStretch()


class Scatter (QWidget):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(TitleLabel('Scatter Graphs'))
        text = BodyLabel("A Scatter graph uses dots to represent values for "
        "two different numeric variables. Scatter graphs are used to observe relationships between variables.")
        text.setWordWrap(True)
        
        layout2.addWidget(text)
        fig = QLabel()
        pixmap = QPixmap(os.path.join("UI","Plot","scatter.png"))
        #pixmap = pixmap.scaled(400,400)
        fig.setPixmap(pixmap)
        fig.setFixedWidth(100)
        layout1.addWidget(fig)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('Scatter'))
        layout_scatter3 = QHBoxLayout()
        layout.addLayout(layout_scatter3)
        for i in ['2d scatter','3d scatter']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_scatter3.addWidget(button)
        layout_scatter3.addStretch()
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('Bubble'))
        layout_bubble = QHBoxLayout()
        layout.addLayout(layout_bubble)
        for i in ['bubble']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_bubble.addWidget(button)
        layout_bubble.addStretch()
        layout.addStretch()

class Pie (QWidget):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(TitleLabel("Pie Graphs"))
        text = BodyLabel("A pie chart is a graphical representation technique that displays data in a "
                                           "circular-shaped graph. Pie charts are often used to represent sample data with data "
                                           "points belonging to a combination of few categories. Each of these "
                                           "categories is represented as a “slice of the pie.” ")
        text.setWordWrap(True)
        
        layout2.addWidget(text)
        fig = QLabel()
        pixmap = QPixmap(os.path.join("UI","Plot","pie.png"))
        #pixmap = pixmap.scaled(400,400)
        fig.setPixmap(pixmap)
        fig.setFixedWidth(100)
        layout1.addWidget(fig)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('2D Pie'))
        layout_2dpie = QHBoxLayout()
        layout.addLayout(layout_2dpie)
        for i in ['pie']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_2dpie.addWidget(button)
        layout_2dpie.addStretch()
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('Others'))
        layout_otherpie = QHBoxLayout()
        layout.addLayout(layout_otherpie)
        for i in ['doughnut','treemap']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_otherpie.addWidget(button)
        layout_otherpie.addStretch()
        layout.addStretch()


class Statistics (QWidget):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(TitleLabel("Statistics Graphs"))
        text = BodyLabel("All these graphs are used in various places to represent concisely a specific set of data "
                                           "in order to display the shape of data and identify outliers. They are useful in exploratory data analysis (EDA).")
        text.setWordWrap(True)
        
        layout2.addWidget(text)
        fig = QLabel()
        pixmap = QPixmap(os.path.join("UI","Plot","stats.png"))
        #pixmap = pixmap.scaled(400,400)
        fig.setPixmap(pixmap)
        fig.setFixedWidth(100)
        layout1.addWidget(fig)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('Histogram'))
        layout_hist = QHBoxLayout()
        for i in ['histogram','stacked histogram']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_hist.addWidget(button)
        layout_hist.addStretch()
        layout.addLayout(layout_hist)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('Box and Whisker'))
        layout_box = QHBoxLayout()
        layout.addLayout(layout_box)
        for i in ['boxplot','violinplot']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_box.addWidget(button)
        layout_box.addStretch()

        layout.addStretch()


class Surface (QWidget):
    sig = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)
        layout2.addWidget(TitleLabel("Surface Graphs"))
        text = BodyLabel("A surface graph plots sets of values in the form of a surface. It is "
                                           "useful when one needs to find the optimum combinations between two sets of data. "
                                           "Sometimes, three-dimensional data can be visualized as a contour instead of a 3D surface.")
        text.setWordWrap(True)
        
        layout2.addWidget(text)
        fig = QLabel()
        pixmap = QPixmap(os.path.join("UI","Plot","surface.png"))
        #pixmap = pixmap.scaled(400,400)
        fig.setPixmap(pixmap)
        fig.setFixedWidth(100)
        layout1.addWidget(fig)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('3D'))
        layout_surface = QHBoxLayout()
        layout.addLayout(layout_surface)
        layout_surface.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for i in ['3d surface','triangular 3d surface']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_surface.addWidget(button)
        layout.addWidget(SeparateHLine())
        layout.addWidget(StrongBodyLabel('Mesh'))
        layout_mesh = QHBoxLayout()
        layout_mesh.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(layout_mesh)
        for i in ['heatmap']:
            button = Plottype_Button(i,50,f"{i.title()}")
            button.sig.connect(lambda type: self.sig.emit(type))
            layout_mesh.addWidget(button)

        layout.addStretch()

class Plottype_Window (QMainWindow):
    sig = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setStyleSheet('QWidget { background:#BDC3C7;}')
        #self.setWindowOpacity(0.97)
        self.setFixedSize(QSize(700,500))
        self.setWindowIcon(QIcon(os.path.join("UI","app-icon.png")))
        self.setWindowTitle('Plot Types')

        layout = QHBoxLayout()

        self.central_widget = QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        
        listview = SideBar()
        layout.addWidget(listview)
        listview.currentTextChanged.connect(self.func)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        line = Line()
        line.sig.connect(lambda: self.close())
        line.sig.connect(lambda type: self.sig.emit(type))
        
        self.stackedlayout.addWidget(line)
        
        bar = Bar()
        bar.sig.connect(lambda: self.close())
        bar.sig.connect(lambda type: self.sig.emit(type))
        
        self.stackedlayout.addWidget(bar)
        
        scatter = Scatter()
        scatter.sig.connect(lambda: self.close())
        scatter.sig.connect(lambda type: self.sig.emit(type))
        
        self.stackedlayout.addWidget(scatter)

        pie = Pie()
        pie.sig.connect(lambda: self.close())
        pie.sig.connect(lambda type: self.sig.emit(type))
        
        self.stackedlayout.addWidget(pie)

        stats = Statistics()
        stats.sig.connect(lambda: self.close())
        stats.sig.connect(lambda type: self.sig.emit(type))
        
        self.stackedlayout.addWidget(stats)

        surface = Surface()
        surface.sig.connect(lambda: self.close())
        surface.sig.connect(lambda type: self.sig.emit(type))
        
        self.stackedlayout.addWidget(surface)

        self.stackedlayout.setCurrentIndex(0)

    

    def func(self, s): 
        if 'Line' in s:
            self.stackedlayout.setCurrentIndex(0)
        if 'Column' in s:
            self.stackedlayout.setCurrentIndex(1)
        if 'Scatter' in s:
            self.stackedlayout.setCurrentIndex(2)
        if 'Pie' in s:
            self.stackedlayout.setCurrentIndex(3)
        if 'Statistics' in s:
            self.stackedlayout.setCurrentIndex(4)
        if 'Surface' in s:
            self.stackedlayout.setCurrentIndex(5)

        if 'Field' in s:
            self.stackedlayout.setCurrentWidget(self.field_widget)
        if 'Stock' in s:
            self.stackedlayout.setCurrentWidget(self.stock_widget)
        if 'Map' in s:
            self.stackedlayout.setCurrentWidget(self.map_widget)