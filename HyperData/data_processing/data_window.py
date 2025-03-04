from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTableView, QApplication)
from PySide6.QtGui import QIcon, QGuiApplication, QBrush, QColor
from PySide6.QtCore import QModelIndex, Signal, Qt, QAbstractTableModel
import os, missingno, squarify
from time import gmtime, strftime, time
import pandas as pd
import numpy as np
from config.settings import list_name, GLOBAL_DEBUG, logger
from ui.base_widgets.button import (_DropDownPushButton, _PrimaryPushButton, ComboBox, Toggle, _ComboBox,
                                    _TransparentPushButton, _TransparentToolButton)
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.window import Dialog
from ui.utils import get_path, isDark
from plot.canvas import ExplorerCanvas
from data_processing.utlis import check_float, check_integer

DEBUG = False

class TableModel(QAbstractTableModel):
    def __init__(self, data: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._data = data.astype('object')
        self.arrays = self._data.to_numpy()
        self.numRows = 100
        self.numColumns = 100
        self.toggleDecor = False
   
    def data(self, index:QModelIndex, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
            return
        
        if index.row()>=self.numRows or index.row()<0 or index.column()>=self.numColumns or index.column()<0:
            return 
        
        value = self.arrays[index.row(), index.column()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return value
    
        if self.toggleDecor:
            value = str(value)
            if value.lower() in ['true','false']:
                background_color = QColor("#FFC4A4")
            elif value == 'nan':
                background_color = QColor("#FBA2D0")
            elif check_integer(value):
                background_color = QColor("#6C7EE1")
            elif check_float(value):
                background_color = QColor("#92B9E3")
            else:
                background_color = QColor("#C688EB")
            
            brightness = 0.2126*background_color.getRgb()[0]+ \
                         0.7152*background_color.getRgb()[1]+ \
                         0.0722*background_color.getRgb()[2]
            if brightness >= 128: text_color = QColor("black")
            else: text_color = QColor("white")

            if role == Qt.ItemDataRole.ForegroundRole:
                return QBrush(text_color)
            elif role == Qt.ItemDataRole.BackgroundRole:
                #return QGuiApplication.palette().base()
                return QBrush(background_color)
            
        return 

    def toggleDecoration(self, toggle=False):
        self.toggleDecor = toggle
        self.layoutChanged.emit()
      
    def canFetchMore(self, index:QModelIndex):

        if self.numRows<self._data.shape[0] or self.numColumns<self._data.shape[1]:
            return True
        return False
    
    def fetchMore(self, index:QModelIndex):

        maxFetch=20     #maximum number of rows/columns to grab at a time.
        
        remainderRows=self._data.shape[0]-self.numRows
        
        if maxFetch < remainderRows:
            self.beginInsertRows(QModelIndex(), self.numRows, self.numRows+maxFetch-1)
            self.numRows += maxFetch
            self.endInsertRows()
        else:
            self.beginResetModel()
            self.numRows = self._data.shape[0]
            self.endResetModel()

        remainderColumns=self._data.shape[1]-self.numColumns
        
        if maxFetch < remainderColumns:
            self.beginInsertColumns(QModelIndex(), self.numColumns, self.numColumns+maxFetch-1)
            self.numColumns += maxFetch
            self.endInsertColumns()
        else:
            self.beginResetModel()
            self.numColumns = self._data.shape[1]
            self.endResetModel()
        

    def rowCount(self, parent):
        if self.numRows < self._data.shape[0]:
            return self.numRows
        return self._data.shape[0]
        

    def columnCount(self, parent):
        if self.numColumns < self._data.shape[1]:
            return self.numColumns
        return self._data.shape[1]
    
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                pass
                #for i in range(self._data.shape[1]):
                return str(list_name[section]).capitalize()+"\n"+str(self._data.columns[section])
                #return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                #print(type(self._data.index[section]),self._data.index[section])
                if isinstance(self._data.index[section], int):
                    return str(self._data.index[section]+1)
                
                return str(self._data.index[section])
    
    def getArray(self) -> np.ndarray:
        return self.arrays
           
class TableView (QWidget):
    def __init__(self, data: pd.DataFrame, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Data")
        self.model = TableModel(data, self.parent())
        
        self.clipboard = QApplication.clipboard()
        self.selected_values = list()

        self.initUI(data)
    
    def initUI (self, data:pd.DataFrame):

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.view.setStyleSheet("QWidget {background:white}")

        self.hlayout = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout)
        self.decorate = Toggle(text="Decoration")
        self.decorate.button.setChecked(False)
        self.decorate.button.checkedChanged.connect(lambda c: self.model.toggleDecoration(c))
        
        self.hlayout.addWidget(self.decorate)
        self.hlayout.addStretch()
        self.time_update = BodyLabel()
        self.hlayout.addWidget(self.time_update)
        
        self.view = QTableView(self.parent())
        self.update_data(data)
        self.vlayout.addWidget(self.view)
        #view.setVerticalScrollBar(widget)
        
        layout1 = QHBoxLayout()
        self.vlayout.addLayout(layout1)
        text = BodyLabel('Data types:')
        text.setFixedWidth(100)
        layout1.addWidget(text)
        self.data_type = BodyLabel()
        layout1.addWidget(self.data_type)
        self.copy_btn = _PrimaryPushButton()
        #self.copy_btn.setIcon(Icon(os.path.join('copy.png')))
        self.copy_btn.setText('Copy to clipboard')
        #self.copy_btn.setToolTip('Copy to clipboard')
        self.copy_btn.setToolTipDuration(2000)
        self.copy_btn.clicked.connect(self.copy_func)
        layout1.addWidget(self.copy_btn)

        layout4 = QHBoxLayout()
        #layout4.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vlayout.addLayout(layout4)
        text = BodyLabel('Data points:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.data_point = BodyLabel()
        layout4.addWidget(self.data_point)
        text = BodyLabel('Missing:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.missing = BodyLabel()
        layout4.addWidget(self.missing)
        text = BodyLabel('Distinct:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.distinct = BodyLabel()
        layout4.addWidget(self.distinct)
        text = BodyLabel('Unique:')
        text.setFixedWidth(100)
        layout4.addWidget(text)
        self.unique = BodyLabel()
        layout4.addWidget(self.unique)

    def on_selection (self):

        self.data = self.model.getArray()

        # selected cell values
        selectedIndexes=self.view.selectionModel().selectedIndexes()
        
        selectedAll = False
        # check if all cells are selected
        if len(selectedIndexes) == self.data.size: 
            selectedAll = True
        
        _datapoints = 0
        _missing = 0
        self.selected_values = np.array([])
        
        if selectedAll:
            _datapoints = self.data.size
            self.selected_values = self.data.copy()
        elif selectedIndexes:
            _datapoints = len(selectedIndexes)
            for i in selectedIndexes:
                self.selected_values = np.append(self.selected_values, i.data())
        
        self.selected_values = self.selected_values.astype(str)
        _values, _count = np.unique(self.selected_values, return_counts=True)
        _unique_values = _values[_count == 1]

        string = list()
        for value in self.selected_values:
            if value.lower() in ['true','false']:
                string.append('boolean')
            elif value == 'nan':
                string.append('nan')
            elif check_integer(value):
                string.append('int')
            elif check_float(value):
                string.append("float")
            else:
                string.append("string")

        _missing = string.count("nan")
        data_type = ", ".join(list(set(string)))
        
        self.data_type.setText(data_type)
        self.unique.setText(str(len(_unique_values)))
        self.distinct.setText(str(np.unique(self.selected_values).shape[0]))
        self.data_point.setText(str(_datapoints))
        self.missing.setText(str(_missing))
       
    def copy_func (self):
        string = [str(i) for i in self.selected_values]
        self.clipboard.setText(', '.join(string))
    
    def update_data (self, data: pd.DataFrame):
        self.model = TableModel(data, self.parent())
        self.view.setModel(self.model)
        self.view.selectionModel().selectionChanged.connect(self.on_selection)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.time_update.setText(f"Updated: {time}")
            
class ExploreView (QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.univar_plot = ["histogram","boxplot","density","kde"]
        self.bivar_plot = ["line","scatter","bar","area","hexbin"]
        self.multivar_plot = ["heatmap","correlation","covariance"]
        self.nan_plot = ["NaNs matrix","NaNs bar"]

        self.grouplist = []
        
        self.initUI()
        self.initMenu()
        self.update_data(data)
    
    def initUI(self):
        self.vlayout = QVBoxLayout(self)
        self.describe_layout = QHBoxLayout()
        self.describe_layout.setContentsMargins(0,0,0,0)
        self.vlayout.addLayout(self.describe_layout)
        self.groupby = Toggle(text="Group by")
        self.groupby.button.checkedChanged.connect(self.update_describe)
        self.groupby.button.checkedChanged.connect(lambda c: self.groupby2.setEnabled(c))
        self.describe_layout.addWidget(self.groupby)
        self.groupby2 = _TransparentPushButton(text="Choose group" if not self.grouplist else str(self.grouplist))
        self.groupby2.setEnabled(False)
        self.groupby2.pressed.connect(self.groupbyDialog)
        self.describe_layout.addWidget(self.groupby2)
        self.describe_layout.addStretch()
        self.view = QTableView(self.parent())
        self.vlayout.addWidget(self.view)
        self.plot_widget = QWidget()
        self.plot_selection = QHBoxLayout(self.plot_widget)
        self.plot_selection.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vlayout.addWidget(self.plot_widget)
        self.btn = _DropDownPushButton(self)
        self.btn.setFixedWidth(150)
        self.plot_selection.addWidget(self.btn)
        menu = self.initMenu()
        self.btn.setMenu(menu)
        self.btn.setText("NaNs matrix")
        self.varx = ComboBox(text="X")
        self.plot_selection.addWidget(self.varx)
        self.vary = ComboBox(text="Y")
        self.plot_selection.addWidget(self.vary)
        self.plot_btn = _PrimaryPushButton(self)
        self.plot_btn.setText("Apply")
        self.plot_btn.pressed.connect(self.update_plot)
        self.vlayout.addWidget(self.plot_btn)
        self.canvas = ExplorerCanvas()
        self.vlayout.addWidget(self.canvas)
    
    def initMenu(self):
        menu = Menu(parent=self)
        menu_univar = Menu("Univariate analysis", self)
        for i in self.univar_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.setText(s))
            action.triggered.connect(self.update_selection)
            menu_univar.addAction(action)
        menu.addMenu(menu_univar)
        menu_bivar = Menu("Bivariate analysis", self)
        for i in self.bivar_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.setText(s))
            action.triggered.connect(self.update_selection)
            menu_bivar.addAction(action)
        menu.addMenu(menu_bivar)
        menu_multivar = Menu("Multivariate analysis", self)
        for i in self.multivar_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.setText(s))
            action.triggered.connect(self.update_selection)
            menu_multivar.addAction(action)
        menu.addMenu(menu_multivar)
        menu_nan = Menu("Missing values", self)
        for i in self.nan_plot:
            action = Action(text=i, parent=self)
            action.triggered.connect(lambda _, s=i: self.btn.setText(s))
            action.triggered.connect(self.update_selection)
            menu_nan.addAction(action)
        menu.addMenu(menu_nan)
        return menu

    def groupbyDialog(self):
        class GroupWidget(QWidget):
            def __init__(self, parent:Dialog, cols:list=[], group:str=None):
                super().__init__(parent)

                idx = parent.main_layout.count()-1
                parent.main_layout.insertWidget(idx, self)

                self.hlayout = QHBoxLayout(self)
                self.hlayout.setContentsMargins(0,0,0,0)

                self.col = _ComboBox(parent=parent)
                self.col.addItems(cols)
                self.col.setCurrentText(group)
                self.hlayout.addWidget(self.col)

                delete = _TransparentToolButton(parent=parent)
                delete.setIcon("delete.png")
                delete.pressed.connect(self.onDelete)
                self.hlayout.addWidget(delete)

            def onDelete(self):
                self.parent().main_layout.removeWidget(self)
                self.deleteLater()
                QApplication.processEvents()
                self.parent().adjustSize()

        def add(group=None):
            GroupWidget(dialog, self.data.columns, group)

        dialog = Dialog("Group by", self.parent())

        add_btn = _TransparentPushButton(self)
        add_btn.setIcon("add.png")
        add_btn.pressed.connect(add)
        dialog.main_layout.addWidget(add_btn)

        for group in self.grouplist:
            add(group)

        if dialog.exec():
            self.grouplist = []
            for widget in dialog.findChildren(GroupWidget):
                widget : GroupWidget
                self.grouplist.append(widget.col.currentText())
            self.groupby2.setText(str(self.grouplist))
            self.update_describe()

    def update_selection(self):
        try:
            # save current text for later
            _varx = self.varx.button.currentText()
            _vary = self.vary.button.currentText()

            # update x and y variables for plot
            self.varx.button.clear()
            self.vary.button.clear()

            plottype = self.btn.text()

            self.varx.button.addItems(self.data.columns)
            self.vary.button.addItems(self.data.columns)

            # set previous text if possible
            self.varx.button.setCurrentText(_varx)
            self.vary.button.setCurrentText(_vary)
            
            # self.varx.button.currentTextChanged.connect(self.update_plot)
            # self.vary.button.currentTextChanged.connect(self.update_plot)

            if plottype in self.univar_plot:
                self.varx.setVisible(True)
                self.vary.setVisible(False)
            elif plottype in self.bivar_plot:
                self.varx.setVisible(True)
                self.vary.setVisible(True)
            elif plottype in self.multivar_plot + self.nan_plot:
                self.varx.setVisible(False)
                self.vary.setVisible(False)
            
            #self.update_plot()
        except Exception as e:
            logger.exception(e)

    def update_data (self, data:pd.DataFrame):
        self.data = data
        self.update_describe()
        self.update_selection()
        self.update_plot()
    
    def update_describe(self):
        if self.data.empty:
            describe = pd.DataFrame()
        elif self.groupby.button.isChecked() and self.grouplist != []:
            describe = self.data.groupby(self.grouplist).describe()
        else:
            describe = self.data.describe()
        
        self.model = TableModel(describe, self.parent())
        self.view.setModel(self.model)
    
    def update_plot(self):
        try:
            plottype = self.btn.text()
            
            varx = self.varx.button.currentText()
            vary = self.vary.button.currentText()
            
            if self.data.empty:
                self.canvas.fig.clear()
            else:
                self.canvas.fig.clear()
                ax = self.canvas.fig.add_subplot()
                
                if plottype == "NaNs matrix": missingno.matrix(df=self.data,fontsize=6,ax=ax)
                elif plottype == "NaNs bar": missingno.bar(df=self.data,fontsize=6,ax=ax)
                elif plottype == "histogram": self.data.hist(varx, ax=ax)
                elif plottype == "boxplot": self.data.boxplot(varx, ax=ax)
                elif plottype == "density": self.data[varx].plot.density(ax=ax)
                elif plottype == "kde": self.data[varx].plot.kde(ax=ax)
                elif plottype == "line": self.data.plot.line(varx, vary, ax=ax)
                elif plottype == "scatter": self.data.plot.scatter(varx, vary, ax=ax)
                elif plottype == "bar": self.data.plot.bar(varx, vary, ax=ax)
                elif plottype == "area": self.data.plot.area(varx, vary, ax=ax)
                elif plottype == "hexbin": self.data.plot.hexbin(varx, vary, ax=ax)
                elif plottype == "heatmap": ax.imshow(self.data.select_dtypes(include="number"), aspect="auto")
                elif plottype == "correlation": ax.imshow(self.data.corr(numeric_only=True), aspect="auto")
                elif plottype == "covariance": ax.imshow(self.data.cov(numeric_only=True), aspect="auto")
            
            #     xticks = []
            #     for ind, label in enumerate(ax.get_xticklabels()):
            #         # keep the maximum number of xticks = 10
            #         if ind % np.ceil(len(ax.get_xticklabels())/5):
            #             xticks.append("")
            #         else: xticks.append(label)
            #     ax.set_xticks(ax.get_xticks(), xticks)
                
            self.canvas.draw_idle() 
            
        except Exception as e:
            logger.exception(e)
        
class DataView (QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Data")
        layout = QHBoxLayout(self)
        self.setWindowIcon(QIcon(os.path.join(get_path(),"ui","icons","data-window.png")))
        screen = QGuiApplication.primaryScreen().geometry().getRect()
        #self.setMinimumSize(int(screen[2]*0.5), int(screen[3]*0.5))
        
        self.tableview = TableView(data, parent)
        layout.addWidget(self.tableview)

        self.explore = ExploreView(data, parent)
        layout.addWidget(self.explore)
    
    def update_data (self, data):
        self.tableview.update_data(data)
        self.explore.update_data(data)

class DataSelection (QWidget):
    sig = Signal(str)
    def __init__(self, data, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Data")
        layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon(os.path.join(get_path(),"ui","icons","data-window.png")))
        screen = QGuiApplication.primaryScreen().geometry().getRect()
        self.setMinimumSize(int(screen[2]*0.5), int(screen[3]*0.5))
        
        self.tableview = TableView(data, parent)
        layout.addWidget(self.tableview)
        self.tableview.copy_btn.setText('Insert to input field')
        self.tableview.copy_btn.pressed.connect(self.btn_pressed)

    def update_data (self, data):
        self.tableview.update_data(data)
    
    def btn_pressed (self):
        string = [str(i) for i in self.tableview.selected_values]
        self.sig.emit(", ".join(string))
