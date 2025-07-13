from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.statistics.dist_fitter.result_dialog import ResultDialog
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, TransparentPushButton
from ui.base_widgets.window import Dialog
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats._continuous_distns import (alpha, anglit, arcsine, argus, beta, betaprime, bradford,
                                            burr, burr12, cauchy, chi, chi2, cosine, crystalball,
                                            dgamma, dweibull, expon, exponnorm, exponweib, exponpow,
                                            f, fatiguelife, fisk, foldcauchy, foldnorm, genlogistic,
                                            gennorm, genpareto, genexpon, genextreme, gausshyper, gamma,
                                            genhalflogistic, genhyperbolic, geninvgauss, gibrat, gompertz,
                                            gumbel_r, gumbel_l, halfcauchy, halflogistic, halfnorm, 
                                            halfgennorm, hypsecant, invgamma, invgauss, invweibull, jf_skew_t,
                                            johnsonsb, johnsonsu, kappa4, kappa3, ksone, kstwo, laplace,
                                            laplace_asymmetric, levy, levy_l, loggamma, loglaplace, lognorm,
                                            loguniform, maxwell, moyal, nakagami, ncx2, ncf, nct, norm, 
                                            norminvgauss, pareto, pearson3, powerlaw, powerlognorm, powernorm, 
                                            rdist, rice, recipinvgauss, skewcauchy, skewnorm, studentized_range,
                                            t, trapezoid, triang, truncexpon, truncnorm, truncpareto, truncweibull_min,
                                            tukeylambda, uniform, weibull_min, weibull_max, wrapcauchy)

DEBUG = False

class DistFitter(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.output_sockets[0].setSocketLabel('Distribution')

        self._config = dict(
            dist = "Normal",
        )
        self.dist_list = ["Alpha","Anglit","Arcsine","Argus","Beta","Beta prime",
                          "Bradford","Burr (type III)","Burr (type XII)","Cauchy","Chi",
                          "Chi-square","Cosine","Crystalball","Double gamma","Double Weibull",
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
                          "Skewed Cauchy","Skew-normal","Studentized range","Student's t","Trapezoid",
                          "Triangular","Truncated exponential","Truncated normal","Truncated Pareto",
                          "Doubly truncated Weibull minimum","Tukey-Lambda","Uniform","Weibull minimum",
                          "Weibull maximum","Wrapped Cauchy"]

        self.label.hide()

        self.result_btn = TransparentPushButton()
        self.result_btn.setText("Result")
        self.result_btn.released.connect(self.result_dialog)
        self.vlayout.insertWidget(2,self.result_btn)        

    def config(self):
        self.dialog = Dialog(title="Configuration", parent=self.parent)

        test = HTransparentComboBox(
            items=self.dist_list, 
            label="Distribution",
            getter=lambda: self._config["dist"],
            layout=self.dialog.main_layout
        )

        if self.dialog.exec():
            self._config.update(
                dist = test.get_value(),
            )
            self.exec()
    
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            rng = np.random.default_rng()
            dist = stats.nbinom
            shapes = (5, 0.5)
            data = dist.rvs(*shapes, size=1000, random_state=rng)
            self.node.input_sockets[0].socket_data = data
            print('data in', self.node.input_sockets[0].socket_data)

        try:     
            self.data = self.node.input_sockets[0].socket_data.copy().to_numpy().ravel()
            dist = self._config["dist"]
            
            if dist == 'Alpha': dist = alpha
            elif dist == 'Anglit': dist = anglit
            elif dist == 'Arcsine': dist = arcsine
            elif dist == 'Argus': dist = argus
            elif dist == 'Beta': dist = beta
            elif dist == 'Beta prime': dist = betaprime
            elif dist == 'Bradford': dist = bradford
            elif dist == 'Burr (type III)': dist = burr
            elif dist == 'Burr (type XII)': dist = burr12
            elif dist == 'Cauchy': dist = cauchy
            elif dist == 'Chi': dist = chi
            elif dist == 'Chi-square': dist = chi2
            elif dist == 'Cosine': dist = cosine
            elif dist == 'Crystalball': dist = crystalball
            elif dist == 'Double gamma': dist = dgamma
            elif dist == 'Double Weibull': dist = dweibull
            elif dist == 'Exponential': dist = expon
            elif dist == 'Exponentially modified Normal': dist = exponnorm
            elif dist == 'Exponentiated Weibull': dist = exponweib
            elif dist == 'Exponential power': dist = exponpow
            elif dist == 'F': dist = f
            elif dist == 'Fatique-life (BirnBaum-Saunders)': dist = fatiguelife
            elif dist == 'Fisk': dist = fisk
            elif dist == 'Folded Cauchy': dist = foldcauchy
            elif dist == 'Folded Normal': dist = foldnorm
            elif dist == 'Generalized logistic': dist = genlogistic
            elif dist == 'Generalized Normal': dist = gennorm
            elif dist == 'Generalized Pareto': dist = genpareto
            elif dist == 'Generalized exponential': dist = genexpon
            elif dist == 'Generalized extreme value': dist = genextreme
            elif dist == 'Gauss hypergeometric': dist = gausshyper
            elif dist == 'Gamma': dist = gamma
            elif dist == 'Generalized half-logistic': dist = genhalflogistic
            elif dist == 'Generalized hyperbolic': dist = genhyperbolic
            elif dist == 'Generalized inverse Gaussian': dist = geninvgauss
            elif dist == 'Gibrat': dist = gibrat
            elif dist == 'Gompertz': dist = gompertz
            elif dist == 'Right-skewed Gumbel': dist = gumbel_r
            elif dist == 'Left-skewed Gumbel': dist = gumbel_l
            elif dist == 'Half-Cauchy': dist = halfcauchy
            elif dist == 'Half-logistic': dist = halflogistic
            elif dist == 'Half-normal': dist = halfnorm
            elif dist == 'Half of generalized normal': dist = halfgennorm
            elif dist == 'Hyperbolic secant': dist = hypsecant
            elif dist == 'Inverted Gamma': dist = invgamma
            elif dist == 'Inverse Gauss': dist = invgauss
            elif dist == 'Inverted Weibull': dist = invweibull
            elif dist == 'Jones and Faddy skew-t': dist = jf_skew_t
            elif dist == 'Johnson SB': dist = johnsonsb
            elif dist == 'Johnson SU': dist = johnsonsu
            elif dist == 'Kappa 4': dist = kappa4
            elif dist == 'Kappa 3': dist = kappa3
            elif dist == 'Kolmogorov-Smirnov one-sided': dist = ksone
            elif dist == 'Kolmogorov-Smirnov two-sided': dist = kstwo
            elif dist == 'Laplace': dist = laplace
            elif dist == 'Asymmetric Laplace': dist = laplace_asymmetric
            elif dist == 'Levy': dist = levy
            elif dist == 'Left-skewed Levy': dist = levy_l
            elif dist == 'Log Gamma': dist = loggamma
            elif dist == 'Log-Laplace': dist = loglaplace
            elif dist == 'Lognormal': dist = lognorm
            elif dist == 'Loguniform': dist = loguniform
            elif dist == 'Maxwell': dist = maxwell
            elif dist == 'Moyal': dist = moyal
            elif dist == 'Nakagami': dist = nakagami
            elif dist == 'Non-central chi-squared': dist = ncx2
            elif dist == 'Non-central F': dist = ncf
            elif dist == "Non-central Student's t": dist = nct
            elif dist == 'Normal': dist = norm
            elif dist == 'Normal inverse Gaussian': dist = norminvgauss
            elif dist == 'Pareto': dist = pareto
            elif dist == 'Pearson type III': dist = pearson3
            elif dist == 'Power-function': dist = powerlaw
            elif dist == 'Power log-normal': dist = powerlognorm
            elif dist == 'Power normal': dist = powernorm
            elif dist == 'R-distributed': dist = rdist
            elif dist == 'Rice': dist = rice
            elif dist == 'Reciprocal inverse Gaussian': dist = recipinvgauss
            elif dist == 'Skewed Cauchy': dist = skewcauchy
            elif dist == 'Skew-normal': dist = skewnorm
            elif dist == 'Studentized range': dist = studentized_range
            elif dist == "Student's t": dist = t
            elif dist == 'Trapezoid': dist = trapezoid
            elif dist == 'Triangular': dist = triang
            elif dist == 'Trunated exponential': dist = truncexpon
            elif dist == 'Truncated normal': dist = truncnorm
            elif dist == 'Truncated Pareto': dist = truncpareto
            elif dist == 'Doubly truncated Weibull minimum': dist = truncweibull_min
            elif dist == 'Tukey-Lambda': dist = tukeylambda
            elif dist == 'Uniform': dist = uniform
            elif dist == 'Weibull minimum': dist = weibull_min
            elif dist == 'Weibull maximum': dist = weibull_max
            elif dist == 'Wrapped Cauchy': dist = wrapcauchy

            params = dist.fit(self.data)
            self.dist = dist(*params)
          
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
        dialog = ResultDialog(self.data, self.dist, self._config["dist"])
        dialog.exec()
    
    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data