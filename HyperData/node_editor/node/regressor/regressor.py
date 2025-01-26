from node_editor.base.node_graphics_content import NodeContentWidget
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (DropDownPrimaryPushButton, _TransparentPushButton)
from ui.base_widgets.frame import SeparateHLine
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from node_editor.node.regressor.menu import AlgorithmMenu
from node_editor.node.regressor.report import scoring, Report
from node_editor.node.regressor.base import RegressorBase
from node_editor.node.regressor.linear import LinearRegression
from node_editor.node.regressor.ridge import RidgeRegression
from node_editor.node.regressor.lasso import Lasso
from node_editor.node.regressor.elasticnet import ElasticNet
from node_editor.node.regressor.least_angle import LeastAngleRegression
from node_editor.node.regressor.lars_lasso import LarsLasso
from node_editor.node.regressor.omp import OrthogonalMatchingPursuit
from node_editor.node.regressor.bayesian_ridge import BayesianRidgeRegression
from node_editor.node.regressor.ard import ARD
from node_editor.node.regressor.tweedie import TweedieRegression
from node_editor.node.regressor.poisson import PoissonRegression
from node_editor.node.regressor.gamma import GammaRegression
from node_editor.node.regressor.sgd import StochasticGradientDescent
from node_editor.node.regressor.passive_aggressive import PassiveAggressiveRegression
from node_editor.node.regressor.ransac import RANSAC
from node_editor.node.regressor.huber import HuberRegression
from node_editor.node.regressor.theilsen import TheilSenRegression
from node_editor.node.regressor.quantile import QuantileRegression
from node_editor.node.regressor.svr import SVR
from node_editor.node.regressor.nu_svr import NuSVR
from node_editor.node.regressor.linear_svr import LinearSVR
from node_editor.node.regressor.kneighbors import KNeighborsRegression
from node_editor.node.regressor.radius_neighbors import RadiusNeighborsRegression
from node_editor.node.regressor.gaussian_process import GaussianProcessRegression
from PySide6.QtWidgets import QStackedLayout
from sklearn import linear_model
import pandas as pd

DEBUG = False

class Regressor(NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)

        self.X, self.Y = list(), list()
        self.Y_test_score, self.Y_pred_score = list(), list()

        self.node.input_sockets[0].setSocketLabel("Train/Test")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "r2 score"

        self._config = dict(
            estimator = "Linear Regression",
            config = dict(),
        )

        self.estimator_list = ["Linear Regression","Ridge Regression","Lasso","ElasticNet",
                               "Least Angle Regression","LARS Lasso","Orthogonal Matching Pursuit",
                               "Bayesian Ridge Regression","Automatic Relevance Determination",
                               "Tweedie Regression","Poisson Regression","Gamma Regression",
                               "Stochastic Gradient Descent","Passive Aggressive Regression",
                               "Randon Sample Consensus","Huber Regression","Theil-Sen Regression",
                               "Quantile Regression","SVR","NuSVR","Linear SVR","K Neighbors Regression",
                               "Radius Neighbors Regression","Gaussian Process Regression"]

        self.estimator = linear_model.LinearRegression(**self._config["config"])

    def currentWidget(self) -> RegressorBase:
        return self.stackedlayout.currentWidget()

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        menu = AlgorithmMenu()
        menu.sig.connect(lambda string: algorithm.button.setText(string))
        menu.sig.connect(lambda string: self.stackedlayout.setCurrentIndex(self.estimator_list.index(string)))
        algorithm = DropDownPrimaryPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"])
        algorithm.button.setMenu(menu)
        dialog.main_layout.addWidget(algorithm)
        dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(LinearRegression())
        self.stackedlayout.addWidget(RidgeRegression())
        self.stackedlayout.addWidget(Lasso())
        self.stackedlayout.addWidget(ElasticNet())
        self.stackedlayout.addWidget(LeastAngleRegression())
        self.stackedlayout.addWidget(LarsLasso())
        self.stackedlayout.addWidget(OrthogonalMatchingPursuit())
        self.stackedlayout.addWidget(BayesianRidgeRegression())
        self.stackedlayout.addWidget(ARD())
        self.stackedlayout.addWidget(TweedieRegression())
        self.stackedlayout.addWidget(PoissonRegression())
        self.stackedlayout.addWidget(GammaRegression())
        self.stackedlayout.addWidget(StochasticGradientDescent())
        self.stackedlayout.addWidget(PassiveAggressiveRegression())
        self.stackedlayout.addWidget(RANSAC())
        self.stackedlayout.addWidget(HuberRegression())
        self.stackedlayout.addWidget(TheilSenRegression())
        self.stackedlayout.addWidget(QuantileRegression())
        self.stackedlayout.addWidget(SVR())
        self.stackedlayout.addWidget(NuSVR())
        self.stackedlayout.addWidget(LinearSVR())
        self.stackedlayout.addWidget(KNeighborsRegression())
        self.stackedlayout.addWidget(RadiusNeighborsRegression())
        self.stackedlayout.addWidget(GaussianProcessRegression())

        if dialog.exec():
            self.estimator = self.currentWidget().estimator
            self.exec()
        
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            X = df.iloc[:,:4]
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
            split = model_selection.ShuffleSplit(n_splits=2, test_size=0.2).split(X, Y)
            result = list()
            for fold, (train_idx, test_idx) in enumerate(split):
                result.append((train_idx, test_idx))
            self.node.input_sockets[0].socket_data = [result, X, Y]
            print('data in', self.node.input_sockets[0].socket_data)
        
        try:
            if DEBUG or isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter):
                # cv is an array of indexes corresponding to (train, test)
                cv = self.node.input_sockets[0].socket_data[0]
                self.X = self.node.input_sockets[0].socket_data[1]
                self.Y = self.node.input_sockets[0].socket_data[2]

                data = pd.concat([self.X, self.Y], axis=1)

                # convert self.X and self.Y into numpy arrays!
                self.X = self.X.to_numpy()
                self.Y = self.Y.to_numpy()
            
                for fold, (train_idx, test_idx) in enumerate(cv):
                    X_train, X_test = self.X[train_idx], self.X[test_idx]
                    Y_train, Y_test = self.Y[train_idx], self.Y[test_idx]

                    model = self.estimator
                    model.fit(X_train, Y_train)
                    
                    Y_pred = model.predict(X_test)
                    Y_pred_all = model.predict(self.X)

                    self.Y_test_score.append(Y_test)
                    self.Y_pred_score.append(Y_pred)

                    data[f"Fold{fold+1}_Prediction"] = Y_pred_all

                score = scoring(self.Y_test_score, self.Y_pred_score)
                self.score_btn.setText(f"Score: {score[self.score_function]:.2f}")
                # change progressbar's color   
                self.progress.changeColor('success')
                # write log
                if DEBUG or GLOBAL_DEBUG: print('data out', data)
                logger.info(f"{self.name} {self.node.id}: {self.estimator} run successfully.")
            else:
                data = pd.DataFrame()
                self.score_btn.setText(f"Score: --")
                # change progressbar's color   
                self.progress.changeColor('fail')
                # write log
                logger.warning(f"{self.name} {self.node.id}: not a valid splitter, return an empty Dataframe.")
        
        except Exception as e:
            data = pd.DataFrame()
            self.score_btn.setText(f"Score: --")
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)


        
        
        self.node.output_sockets[0].socket_data = self.estimator
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def score_dialog(self):
        dialog = Report(self.Y_test_score, self.Y_pred_score)
        score = scoring(self.Y_test_score, self.Y_pred_score)
        dialog.metricChange.connect(lambda s: self.score_btn.setText(f"Score {score[s]:.2f}"))
        if dialog.exec():
            self.score_function = dialog.score_function
    
    def eval(self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None
        # reset socket data
        self.node.input_sockets[0].socket_data = [[],pd.DataFrame(), pd.DataFrame()]
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data