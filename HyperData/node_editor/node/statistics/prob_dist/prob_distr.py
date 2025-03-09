from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import PrimaryComboBox, _TransparentPushButton
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from PySide6.QtWidgets import QStackedLayout
from node_editor.node.statistics.prob_dist.base import DistBase
from node_editor.node.statistics.prob_dist.norm import Norm
from node_editor.node.statistics.prob_dist.alpha import Alpha
from node_editor.node.statistics.prob_dist.anglit import Anglit
from node_editor.node.statistics.prob_dist.arcsine import Arcsine
from node_editor.node.statistics.prob_dist.argus import Argus
from node_editor.node.statistics.prob_dist.beta import Beta
from node_editor.node.statistics.prob_dist.betaprime import BetaPrime
from node_editor.node.statistics.prob_dist.bradford import Bradford
from node_editor.node.statistics.prob_dist.burr import Burr
from node_editor.node.statistics.prob_dist.burr12 import Burr12
from node_editor.node.statistics.prob_dist.cauchy import Cauchy
from node_editor.node.statistics.prob_dist.chi import Chi
from node_editor.node.statistics.prob_dist.chi2 import Chi2
from node_editor.node.statistics.prob_dist.cosine import Cosine
from node_editor.node.statistics.prob_dist.crystalball import Crystalball
from node_editor.node.statistics.prob_dist.dgamma import DGamma
from node_editor.node.statistics.prob_dist.dweibull import DWeibull
from node_editor.node.statistics.prob_dist.expon import Expon
from node_editor.node.statistics.prob_dist.exponnorm import Exponnorm
from node_editor.node.statistics.prob_dist.exponweib import ExponWeib
from node_editor.node.statistics.prob_dist.exponpow import Exponpow
from node_editor.node.statistics.prob_dist.f import F
from node_editor.node.statistics.prob_dist.fatiquelife import FatiqueLife
from node_editor.node.statistics.prob_dist.fisk import Fisk
from node_editor.node.statistics.prob_dist.foldcauchy import FoldCauchy
from node_editor.node.statistics.prob_dist.foldnorm import Foldnorm
from node_editor.node.statistics.prob_dist.genlogistic import Genlogistic
from node_editor.node.statistics.prob_dist.gennorm import Gennorm
from node_editor.node.statistics.prob_dist.genpareto import Genpareto
from node_editor.node.statistics.prob_dist.genexpon import Genexpon
from node_editor.node.statistics.prob_dist.genextreme import Genextreme
from node_editor.node.statistics.prob_dist.gausshyper import Gausshyper
from node_editor.node.statistics.prob_dist.gamma import Gamma
from node_editor.node.statistics.prob_dist.genhalflogistic import Genhalflogistic
from node_editor.node.statistics.prob_dist.genhyperbolic import Genhyperbolic
from node_editor.node.statistics.prob_dist.geninvgauss import Geninvgauss
from node_editor.node.statistics.prob_dist.gibrat import Gibrat
from node_editor.node.statistics.prob_dist.gompertz import Gompertz
from node_editor.node.statistics.prob_dist.gumbel_r import Gumbelr
from node_editor.node.statistics.prob_dist.gumbel_l import Gumbell
from node_editor.node.statistics.prob_dist.halfcauchy import HalfCauchy
from node_editor.node.statistics.prob_dist.halflogistic import Halflogistic
from node_editor.node.statistics.prob_dist.halfnorm import Halfnorm
from node_editor.node.statistics.prob_dist.halfgennorm import Halfgennorm
from node_editor.node.statistics.prob_dist.hypsecant import Hypsecent
from node_editor.node.statistics.prob_dist.invgamma import Invgamma
from node_editor.node.statistics.prob_dist.invgauss import Invgauss
from node_editor.node.statistics.prob_dist.invweibull import Invweibull
from node_editor.node.statistics.prob_dist.jf_skew_t import Jfskewt
from node_editor.node.statistics.prob_dist.johnsonsb import JohnsonSB
from node_editor.node.statistics.prob_dist.johnsonsu import JohnsonSU
from node_editor.node.statistics.prob_dist.kappa4 import Kappa4
from node_editor.node.statistics.prob_dist.kappa3 import Kappa3
from node_editor.node.statistics.prob_dist.ksone import Ksone
from node_editor.node.statistics.prob_dist.kstwo import Kstwo
from node_editor.node.statistics.prob_dist.laplace import Laplace
from node_editor.node.statistics.prob_dist.asymmtric import Asmmetric
from node_editor.node.statistics.prob_dist.levy import Levy
from node_editor.node.statistics.prob_dist.levy_l import Levyl
from node_editor.node.statistics.prob_dist.loggamma import Loggamma
from node_editor.node.statistics.prob_dist.loglaplace import LogLaplace
from node_editor.node.statistics.prob_dist.lognorm import Lognorm
from node_editor.node.statistics.prob_dist.loguniform import Loguniform
from node_editor.node.statistics.prob_dist.maxwell import Maxwell
from node_editor.node.statistics.prob_dist.moyal import Moyal
from node_editor.node.statistics.prob_dist.nakagami import Nakagami
from node_editor.node.statistics.prob_dist.ncx2 import NCX2
from node_editor.node.statistics.prob_dist.ncf import NCF
from node_editor.node.statistics.prob_dist.nct import NCT
from node_editor.node.statistics.prob_dist.norminvgauss import NorminvGauss
from node_editor.node.statistics.prob_dist.pareto import Pareto
from node_editor.node.statistics.prob_dist.pearson3 import Pearson3
from node_editor.node.statistics.prob_dist.powerlaw import Powerlaw
from node_editor.node.statistics.prob_dist.powerlognorm import Powerlognorm
from node_editor.node.statistics.prob_dist.powernorm import Powernorm
from node_editor.node.statistics.prob_dist.rdist import Rdist
from node_editor.node.statistics.prob_dist.rice import Rice
from node_editor.node.statistics.prob_dist.recipinvgauss import Recipinvgauss
from node_editor.node.statistics.prob_dist.skewcauchy import SkewCauchy
from node_editor.node.statistics.prob_dist.skewnorm import Skewnorm
from node_editor.node.statistics.prob_dist.studentized_range import Studentized_range
from node_editor.node.statistics.prob_dist.t import T
from node_editor.node.statistics.prob_dist.trapezoid import Trapezoid
from node_editor.node.statistics.prob_dist.triang import Triang
from node_editor.node.statistics.prob_dist.truncexpon import Truncexpon
from node_editor.node.statistics.prob_dist.truncnorm import Truncnorm
from node_editor.node.statistics.prob_dist.truncpareto import Truncpareto
from node_editor.node.statistics.prob_dist.truncweibull_min import TruncWeibull
from node_editor.node.statistics.prob_dist.tukeylambda import Tukeylambda
from node_editor.node.statistics.prob_dist.uniform import Uniform
from node_editor.node.statistics.prob_dist.weibull_min import Weibullmin
from node_editor.node.statistics.prob_dist.weibull_max import Weibullmax
from node_editor.node.statistics.prob_dist.wrapcauchy import WrapCauchy

DEBUG = True

class ProbDist (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            dist = "Normal",
            config = None
        )
        self.dist_list = ["Alpha","Anglit","Arcsine","Argus","Beta","Beta prime",
                          "Bradford","Burr (type III)","Burr (type XII)","Cauchy","Chi",
                          "Chi-square","Cosine","Crystalball","Double gamme","Double Weibull",
                          "Exponential","Exponentially modified Normal","Exponentiated Weibull",
                          "Exponential power","F","Fatique-life (BirnBaum-Saunders)","Fisk",
                          "Folded Cauchy","Folded Normal","Generalized logistic","Generalized Normal",
                          "Generalized Pareto","Generalized exponential","Generalized extreme value",
                          "Gauss hypergeometric","Gamma","Generalized half-logistic",
                          "Generalized hyperbolic","Generalized inverse Gaussian","Gibrat",
                          "Gompertz","Right-skewed Gumbel","Left-skewed Gumbel","Half-Cauchy",
                          "Half-logistic","Half-normal","Half of generalized normal",
                          "Hyperbolic secant","Inverted Gamma","Inverse Gauss","Inverted Weibull",
                          "Jones and Faddy skew-t","Johnson SB","Johnson SU","Kappa 4","Kappa 3",
                          "Kolmogorov-Smirnov one-sided","Kolmogorov-Smirnov two-sided","Laplace",
                          "Asymmetric Laplace","Levy","Left-skewed Levy","Log Gamma","Log-Laplace",
                          "Lognormal","Loguniform","Maxwell","Moyal","Nakagami","Non-central chi-squared",
                          "Non-central F","Non-central Student's t","Normal","Normal inverse Gaussian",
                          "Pareto","Pearson type III","Power-function","Power log-normal",
                          "Power normal","R-distributed","Rice","Reciprocal inverse Gaussian",
                          "Skewed Cauchy","Skew-normal","Studentized range","Student's t","Trapezoidal",
                          "Triangular","Truncated exponential","Truncated normal","Truncated Pareto",
                          "Doubly truncated Weibull minimum","Tukey-Lambda","Uniform","Weibull minimum",
                          "Weibull maximum","Wrapped Cauchy"]

        self.label.hide()

        self.result_btn = _TransparentPushButton()
        self.result_btn.setText("Result")
        self.result_btn.released.connect(self.result_dialog)
        self.vlayout.insertWidget(2,self.result_btn)

        self.initDialog()
    
    def initDialog(self):
        self.dialog = Dialog(title="Configuration", parent=self.parent)

        self.test = PrimaryComboBox(items=self.dist_list, text="Distribution")
        self.test.button.setMinimumWidth(300)
        self.test.button.setCurrentText(self._config["dist"])
        self.test.button.currentTextChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(self.dist_list.index(s)))
        self.dialog.main_layout.addWidget(self.test)

        self.dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        self.dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(Alpha())
        self.stackedlayout.addWidget(Anglit())
        self.stackedlayout.addWidget(Arcsine())
        self.stackedlayout.addWidget(Argus())
        self.stackedlayout.addWidget(Beta())
        self.stackedlayout.addWidget(BetaPrime())
        self.stackedlayout.addWidget(Bradford())
        self.stackedlayout.addWidget(Burr())
        self.stackedlayout.addWidget(Burr12())
        self.stackedlayout.addWidget(Cauchy())
        self.stackedlayout.addWidget(Chi())
        self.stackedlayout.addWidget(Chi2())
        self.stackedlayout.addWidget(Cosine())
        self.stackedlayout.addWidget(Crystalball())
        self.stackedlayout.addWidget(DGamma())
        self.stackedlayout.addWidget(DWeibull())
        self.stackedlayout.addWidget(Expon())
        self.stackedlayout.addWidget(Exponnorm())
        self.stackedlayout.addWidget(ExponWeib())
        self.stackedlayout.addWidget(Exponpow())
        self.stackedlayout.addWidget(F())
        self.stackedlayout.addWidget(FatiqueLife())
        self.stackedlayout.addWidget(Fisk())
        self.stackedlayout.addWidget(FoldCauchy())
        self.stackedlayout.addWidget(Foldnorm())
        self.stackedlayout.addWidget(Genlogistic())
        self.stackedlayout.addWidget(Gennorm())
        self.stackedlayout.addWidget(Genpareto())
        self.stackedlayout.addWidget(Genexpon())
        self.stackedlayout.addWidget(Genextreme())
        self.stackedlayout.addWidget(Gausshyper())
        self.stackedlayout.addWidget(Gamma())
        self.stackedlayout.addWidget(Genhalflogistic())
        self.stackedlayout.addWidget(Genhyperbolic())
        self.stackedlayout.addWidget(Geninvgauss())
        self.stackedlayout.addWidget(Gibrat())
        self.stackedlayout.addWidget(Gompertz())
        self.stackedlayout.addWidget(Gumbelr())
        self.stackedlayout.addWidget(Gumbell())
        self.stackedlayout.addWidget(HalfCauchy())
        self.stackedlayout.addWidget(Halflogistic())
        self.stackedlayout.addWidget(Halfnorm())
        self.stackedlayout.addWidget(Halfgennorm())
        self.stackedlayout.addWidget(Hypsecent())
        self.stackedlayout.addWidget(Invgamma())
        self.stackedlayout.addWidget(Invgauss())
        self.stackedlayout.addWidget(Invweibull())
        self.stackedlayout.addWidget(Jfskewt())
        self.stackedlayout.addWidget(JohnsonSB())
        self.stackedlayout.addWidget(JohnsonSU())
        self.stackedlayout.addWidget(Kappa4())
        self.stackedlayout.addWidget(Kappa3())
        self.stackedlayout.addWidget(Ksone())
        self.stackedlayout.addWidget(Kstwo())
        self.stackedlayout.addWidget(Laplace())
        self.stackedlayout.addWidget(Asmmetric())
        self.stackedlayout.addWidget(Levy())
        self.stackedlayout.addWidget(Levyl())
        self.stackedlayout.addWidget(Loggamma())
        self.stackedlayout.addWidget(LogLaplace())
        self.stackedlayout.addWidget(Lognorm())
        self.stackedlayout.addWidget(Loguniform())
        self.stackedlayout.addWidget(Maxwell())
        self.stackedlayout.addWidget(Moyal())
        self.stackedlayout.addWidget(Nakagami())
        self.stackedlayout.addWidget(NCX2())
        self.stackedlayout.addWidget(NCF())
        self.stackedlayout.addWidget(NCT())
        self.stackedlayout.addWidget(Norm())
        self.stackedlayout.addWidget(NorminvGauss())
        self.stackedlayout.addWidget(Pareto())
        self.stackedlayout.addWidget(Pearson3())
        self.stackedlayout.addWidget(Powerlaw())
        self.stackedlayout.addWidget(Powerlognorm())
        self.stackedlayout.addWidget(Powernorm())
        self.stackedlayout.addWidget(Rdist())
        self.stackedlayout.addWidget(Rice())
        self.stackedlayout.addWidget(Recipinvgauss())
        self.stackedlayout.addWidget(SkewCauchy())
        self.stackedlayout.addWidget(Skewnorm())
        self.stackedlayout.addWidget(Studentized_range())
        self.stackedlayout.addWidget(T())
        self.stackedlayout.addWidget(Trapezoid())
        self.stackedlayout.addWidget(Triang())
        self.stackedlayout.addWidget(Truncexpon())
        self.stackedlayout.addWidget(Truncnorm())
        self.stackedlayout.addWidget(Truncpareto())
        self.stackedlayout.addWidget(TruncWeibull())
        self.stackedlayout.addWidget(Tukeylambda())
        self.stackedlayout.addWidget(Uniform())
        self.stackedlayout.addWidget(Weibullmin())
        self.stackedlayout.addWidget(Weibullmax())
        self.stackedlayout.addWidget(WrapCauchy())

        self.stackedlayout.setCurrentIndex(self.dist_list.index(self.test.button.currentText()))
    
    def currentWidget(self) -> DistBase:
        return self.stackedlayout.currentWidget()
    
    def config(self):
        if self.dialog.exec():
            self.currentWidget().update_config()
            self._config.update(
                dist = self.test.button.currentText(),
                config = self.currentWidget()._config
            )
            self.exec()
    
    def func(self):
        self.eval()

        try:     
            self.currentWidget().update_config()
            self.dist = self.currentWidget().dist
            rvs = self.dist.rvs() # check if distribution is valid
            
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")

        except Exception as e:
            self.result = None
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = self.dist
    
    def result_dialog(self):
        self.currentWidget().result_dialog()
    
    def eval(self):
        self.resetStatus()