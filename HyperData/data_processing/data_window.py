from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTableView, QApplication, QLabel, QAbstractItemView,
                             QCompleter, QPushButton, QMainWindow, QScrollBar)
from PySide6.QtGui import QIcon, QGuiApplication
from PySide6.QtCore import QModelIndex, QSize, Signal, Qt, QAbstractTableModel, QMetaType
import os, missingno, squarify
from time import gmtime, strftime
import pandas as pd
import numpy as np
from config.settings import list_name, GLOBAL_DEBUG, logger
from ui.base_widgets.button import _DropDownPushButton, _PrimaryPushButton, ComboBox
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.menu import Menu, Action
from ui.utils import get_path
from plot.canvas import ExplorerCanvas
import seaborn as sns

DEBUG = False

class TableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self.numRows=100    
        self.numColumns=100

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        index=QModelIndex
        """
        if not index.isValid():
            return
        
        if index.row()>=self.numRows or index.row()<0 or index.column()>=self.numColumns or index.column()<0:
            return 
        
        if role==Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        elif role==Qt.ItemDataRole.BackgroundRole:
            return QGuiApplication.palette().base()
            
        return 
    
    def canFetchMore(self, index):
        """
        index=QModelIndex
        """
        if self.numRows<self._data.shape[0] or self.numColumns<self._data.shape[1]:
            return True
        else:
            return False
    def fetchMore(self, index):
        """
        Index=QModelIndex
        """
        maxFetch=20     #maximum number of rows/columns to grab at a time.
        
        remainderRows=self._data.shape[0]-self.numRows
        
        
        if maxFetch < remainderRows:
            self.beginInsertRows(QModelIndex(), self.numRows, self.numRows+maxFetch-1)
            self.endInsertRows()
            self.numRows+=maxFetch
        else:
            self.beginResetModel()
            self.numRows = self._data.shape[0]
            self.endResetModel()

        remainderColumns=self._data.shape[1]-self.numColumns
        
        if maxFetch<remainderColumns:
            self.beginInsertColumns(QModelIndex(), self.numColumns, self.numColumns+maxFetch-1)
            self.endInsertColumns()
            self.numColumns+=maxFetch
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
            
class TableView (QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Data")
        self.data = data
        
        self.clipboard = QApplication.clipboard()
        self.selected_values = list()

        self.initUI()
    
    def initUI (self):

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #self.view.setStyleSheet("QWidget {background:white}")

        self.time_update = BodyLabel()
        
        self.view = QTableView(self.parent())
        self.update_data(self.data)
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

        self.vlayout.addWidget(self.time_update)


    def on_selection (self):

        # selected cell values
        _selectedRows = self.view.selectionModel().selectedRows()
        _selectedColumns = self.view.selectionModel().selectedColumns()
        _selectedIndexes=self.view.selectionModel().selectedIndexes()
        
        # filter the selectedRows and selectedColumns so they do not overlap
        selectedAll = False
        selectedRows = list()
        for i in _selectedRows:
            selectedRows.append(i.row())
        selectedColumns = list()
        for i in _selectedColumns:
            selectedColumns.append(i.column())
        selectedIndexes = list()
        for i in _selectedIndexes:
            try:
                if not i.row() in selectedRows and not i.column() in selectedColumns:
                    selectedIndexes.append(i)
            except:pass
        
        # check if all cells are selected
        if len(selectedRows) == self.data.shape[0] or len(selectedColumns) == self.data.shape[1]:
            selectedAll = True
        
        _datapoints = 0
        _missing = 0
        self.selected_values = list()
        
        for i in selectedRows:
            _datapoints += self.data.iloc[i].shape[0]
            _missing += self.data.iloc[i].isna().sum()
            if self.data.shape[0]*self.data.shape[1] < 1000*20000:
                for j in self.data.iloc[i]:
                    self.selected_values.append(j)
        for i in selectedColumns:
            _datapoints += self.data.iloc[:,i].shape[0]
            _missing += self.data.iloc[:,i].isna().sum()
            if self.data.shape[0]*self.data.shape[1] < 1000*20000:
                for j in self.data.iloc[:,i]:
                    self.selected_values.append(j)
        for i in selectedIndexes:
            _datapoints += 1
            try: _missing += 1 if pd.isna(float(i.data())) else 0
            except:pass
            if self.data.shape[0]*self.data.shape[1] < 1000*20000:
                self.selected_values.append(i.data())
        
        if selectedAll:
            _datapoints = self.data.shape[0]*self.data.shape[1]
            _missing = pd.isnull(self.data).sum().sum()
        
        _unique_values = list()
        for i in self.selected_values:
            if i not in _unique_values:
                _unique_values.append(i)
            else:
                _unique_values.remove(i)

        string = list()
        for value in self.selected_values:
            value = str(value)
            if value.isdigit():
                string.append('int')
            elif value.replace('.','',1).isdigit():
                string.append("float")
            elif value.lower() in ['true','false']:
                string.append('boolean')
            elif value == 'nan':
                string.append('nan')
            else:
                string.append("string")
                
        data_type = ", ".join(list(set(string)))
        
        self.data_type.setText(data_type)
        self.unique.setText(str(len(_unique_values)))
        self.distinct.setText(str(np.unique(self.selected_values).shape[0]))
        self.data_point.setText(str(_datapoints))
        self.missing.setText(str(_missing))
       
    
    def copy_func (self):
        string = [str(i) for i in self.selected_values]
        self.clipboard.setText(', '.join(string))
    
    def update_data (self, data):
        self.data = data
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
        
        self.initUI()
        self.initMenu()
        self.update_data(data)
    
    def initUI(self):
        self.vlayout = QVBoxLayout(self)
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

    def update_selection(self):
        try:
            # update x and y variables for plot
            self.varx.button.clear()
            self.vary.button.clear()

            plottype = self.btn.text()

            self.varx.button.addItems(self.data.columns)
            self.vary.button.addItems(self.data.columns)
            
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
        if data.empty:
            describe = pd.DataFrame()
        else:
            describe = data.describe()
        
        self.model = TableModel(describe, self.parent())
        self.view.setModel(self.model)

        self.update_selection()
        self.update_plot()
    
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
                
                match plottype:
                    case "NaNs matrix": missingno.matrix(df=self.data,fontsize=6,ax=ax)
                    case "NaNs bar": missingno.bar(df=self.data,fontsize=6,ax=ax)
                    case "histogram": self.data.hist(varx, ax=ax)
                    case "boxplot": self.data.boxplot(varx, ax=ax)
                    case "density": self.data[varx].plot.density(ax=ax)
                    case "kde": self.data[varx].plot.kde(ax=ax)
                    case "line": self.data.plot.line(varx, vary, ax=ax)
                    case "scatter": self.data.plot.scatter(varx, vary, ax=ax)
                    case "bar": self.data.plot.bar(varx, vary, ax=ax)
                    case "area": self.data.plot.area(varx, vary, ax=ax)
                    case "hexbin": self.data.plot.hexbin(varx, vary, ax=ax)
                    case "heatmap": ax.imshow(self.data.select_dtypes(include="number"), aspect="auto")
                    case "correlation": ax.imshow(self.data.corr(numeric_only=True), aspect="auto")
                    case "covariance": ax.imshow(self.data.cov(numeric_only=True), aspect="auto")
            
            #     xticks = []
            #     for ind, label in enumerate(ax.get_xticklabels()):
            #         # keep the maximum number of xticks = 10
            #         if ind % np.ceil(len(ax.get_xticklabels())/5):
            #             xticks.append("")
            #         else: xticks.append(label)
            #     ax.set_xticks(ax.get_xticks(), xticks)

            self.canvas.draw_idle() 
            
        except Exception as e:
            print(e)
            logger.exception(e)
        
class DataView (QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Data")
        layout = QHBoxLayout(self)
        self.setWindowIcon(QIcon(os.path.join(get_path(),"ui","icons","data-window.png")))
        screen = QGuiApplication.primaryScreen().geometry().getRect()
        self.setMinimumSize(int(screen[2]*0.5), int(screen[3]*0.5))
        
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
