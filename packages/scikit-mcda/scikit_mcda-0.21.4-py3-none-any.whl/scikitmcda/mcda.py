'''
#########################################################
# SCI-KIT-MCDA Library                                  #
# Author: Antonio Horta                                 #
# https://gitlab.com/cybercrafter/scikit-mcda           #
# Cybercrafter ® 2021                                   #
#########################################################
'''

import pandas as pd
import numpy as np
import copy
from tabulate import tabulate
from constants import *

class MCDA:
    """
    Class: MCDA: Multi-Criteria Decision Aid
    """
    def __init__(self):
        self.df_original = 0
        self.weights = []
        self.signals = []
        self.normalization_method = "RootSumSquared"
        self.df_normalized = 0
        self.df_weighted = 0
        self.df_pis = []
        self.df_nis = []
        self.df_closeness = 0
        self.df_decision = []

    def dataframe(self, alt_data, alt_labels=[], criteria_label=[]):

        # define state labels if not exists
        if criteria_label == []:
            for s in range(0, len(alt_data[0])):
                state_label.append("C" + str(s+1))

        # define alternative labels if not exists
        if alt_labels == []:
            for a in range(0, len(alt_data)):
                alt_labels.append("A" + str(a+1))

        df_data = pd.DataFrame(data=alt_data, columns=criteria_label)
        df_data.insert(loc=0,
                    column='alternatives',
                    value=alt_labels)
        dfo = df_data

        self.df_original = copy.copy(dfo)
        self.df_calc = copy.copy(dfo)
        self.decision = []

    def set_normalization_method(self, normalization_method="RootSumSquared"):
        if normalization_method in NORMALIZATION_METHODS:
            self.normalization_method = normalization_method 
        else:
            raise ValueError("Invalid parameter! Use a method defined in constants. e.g. normalization_D, zScore etc...")

    def set_weights_manually(self, weights):
        if self.__check_weights(weights) is True:
            self.weights = weights
        else:
            raise ValueError("Invalid weights! Each weight must be float between 0 and 1 and same number of criteria")

    def set_weights_by_ranking_A(self):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {1 / rj} / {∑[1 / rk], where k range is 1 to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[1 / rk]
            b = b + (1 / k)
        for j in r: # Wj = {1 / rj} / b
            W.append((1 / j) / b)
        
        self.weights = W

    def set_weights_by_ranking_B(self):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {n -rj + 1} / {∑[ n - rk + 1], where k range is 1 to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[ n - rk + 1]
            b = b + (n - k + 1)
        for j in r: # Wj = {n -rj + 1} / b
            W.append((n - j + 1) / b)
        
        self.weights = W

    def set_weights_by_ranking_C(self):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {1 / n} * {∑[ 1 / K ], where K range is j to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1)
        r = r[::-1].tolist()

        W = []
        b = 0
        a = 1 / n
        for k in r: # b = ∑[ 1 / K ]
            b = b + (1 / k)
            W.insert(0, a * b)
        
        self.weights = W

    def set_weights_by_ranking_B_POW(self, P=0):
        """
        The criteria must be ordered by importance c1 > c2 > c3 ... 
        Wj = {n -rj + 1}P / {∑[ n - rk + 1]P, where k range is 1 to n}
        """
        n = len(self.df_original.columns) - 1
        r = np.arange(1, n+1, 1).tolist()
        W = []
        b = 0
        for k in r: # b = ∑[ n - rk + 1]
            b = b + pow((n - k + 1),P)
        for j in r: # Wj = {n -rj + 1} / b
            W.append(pow((n - j + 1), P) / b)
        print(W)
        self.weights = W

    def set_weights_by_entropy(self, normalization_method_for_entropy=None):
        
        # Save current norm method
        current_norm_method = self.normalization_method
       
        if normalization_method_for_entropy == None:
            normalization_method_for_entropy = current_norm_method

        # appy new norm method for entropy and apply
        self.set_normalization_method(normalization_method_for_entropy)

        self.__normalize()
        x, y = self.df_normalized.iloc[:,1:].shape
        entropies = np.empty(y)

        for i, col in enumerate(self.df_normalized.iloc[:,1:].T):
            if np.any(col == 0):
                entropies[i] = 0
            else:
                entropies[i] = -np.sum(col * np.log(col))
        entropies = entropies / np.log(x)

        result = 1 - entropies
        
        # set entropy weights
        self.weights = (result/np.sum(result)).tolist()


        #back current nor method
        self.normalization_method = current_norm_method

    def set_signals(self, signals):
        if self.__check_signals(signals) is True:
            self.signals = signals
        else:
            raise ValueError("Invalid signals! It's must be a list of 1 or -1")

    def topsis(self):        
        self.__normalize()
        self.__weighting_from_normalized()
        self.__xis()
        self.__closeness()
        return "topsis"

    def wsm(self):        
        self.__normalize()
        self.__weighting_from_normalized()
        self.__wsm()
        return "wsm"

    def wpm(self):        
        self.__normalize()
        self.__weighting_from_normalized()
        self.__wpm()
        return "wsm"

    def waspas(self, lambda_=0.5):
        if self.__check_lambda(lambda_) is True:
            self.__normalize()
            self.__weighting_from_normalized()
            self.__waspas(lambda_)
            return "waspas"

    def __normalize(self):
        if self.normalization_method == RootSumSquared_:
            self.__norm_RootSumSquared()
        elif self.normalization_method == Sum_:
            self.__norm_Sum()
        elif self.normalization_method == MinMax_:
            self.__norm_MinMax()
        elif self.normalization_method == Max_:
            self.__norm_Max()
        elif self.normalization_method == ZScore_:
            self.__norm_ZScore()
        elif self.normalization_method == Logistic_:
            self.__norm_Logistic()

    def __norm_ZScore(self):
        normalized = (self.df_original.iloc[:, 1:] - self.df_original.iloc[:, 1:].mean(axis=0))/self.df_original.iloc[:, 1:].std(axis=0)
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __norm_Logistic(self):
        normalized = (1/ 1 - pd.DataFrame(np.exp(self.df_original.iloc[:, 1:])))
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __norm_Max(self):
        normalized = (self.df_original.iloc[:, 1:]/self.df_original.iloc[:, 1:].max(axis=0))
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __norm_minMax(self):
        normalized = (self.df_original.iloc[:, 1:]-self.df_original.iloc[:, 1:].min(axis=0))/(self.df_original.iloc[:, 1:].max(axis=0)-self.df_original.iloc[:, 1:].min(axis=0))
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __norm_Sum(self):
        normalized = self.df_original.iloc[:, 1:]/self.df_original.iloc[:, 1:].sum(axis=0)
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __norm_RootSumSquared(self):
        normalized = self.df_original.iloc[:, 1:]/np.sqrt(self.df_original.iloc[:, 1:].pow(2).sum(axis=0))
        self.df_normalized = pd.DataFrame(self.df_original.iloc[:, 0]).join(normalized)

    def __weighting_from_normalized(self):
        weighted = self.df_normalized.iloc[:, 1:] * self.weights
        self.df_weighted = pd.DataFrame(self.df_original.iloc[:,0]).join(weighted)
         
    def __xis(self):
        pis = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals).max(axis=0) * self.signals
        self.df_pis = pis
        nis = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals).min(axis=0) * self.signals
        self.df_nis = nis

    def __closeness(self):
        dp = np.sqrt(self.df_weighted.iloc[:, 1:].sub(self.df_pis).sum(axis=1).pow(2))
        dn = np.sqrt(self.df_weighted.iloc[:, 1:].sub(self.df_nis).sum(axis=1).pow(2))
        closeness = pd.DataFrame(dn.div(dp+dn), columns=["closeness"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(closeness).sort_values(by=["closeness"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __waspas(self, lambda_):
        w_df = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals)
        q_wsm = pd.DataFrame(w_df.sum(axis=1), columns=["WSM"]) * lambda_
        q_wpm = pd.DataFrame(w_df.prod(axis=1), columns=["WPM"]) * (1 - lambda_) 

        waspas = q_wsm.iloc[:,0] + q_wpm.iloc[:,0]
        label = "WASPAS (λ " + str(lambda_) + " )" 
        waspas_df = pd.DataFrame(waspas, columns=[label]) 

        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(waspas_df).sort_values(by=[label], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __wsm(self):
        wsm = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals)
        wsm = pd.DataFrame(wsm.sum(axis=1), columns=["WSM"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(wsm).sort_values(by=["WSM"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __wpm(self):
        wpm = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals)
        wpm = pd.DataFrame(wpm.prod(axis=1), columns=["WPM"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_concat_labels = pd.DataFrame(self.df_original.iloc[:,0]).join(wpm).sort_values(by=["WPM"], ascending=False, ignore_index=True)
        df_ranking = df_concat_labels.join(pd.DataFrame(i, columns=["rank"]))
        self.df_decision = df_ranking

    def __check_lambda(self, lambda_):
        result = False
        if type(lambda_) == float:
            if (lambda_ >= 0 and lambda_ <= 1):
                result = True
            else:
                raise ValueError("Lambda must be a value between 0 and 1!")                
        return result

    def __check_weights(self, weights):
        result = False
        if type(weights) == list:
            if len(self.df_original.columns.tolist()) - 1 == len(weights) \
               and all(isinstance(n, float) for n in weights) \
               and all((n >= 0 and n <= 1) for n in weights) \
               and round(sum(weights)) == 1:
                result = True
        return result

    def __check_signals(self, signals):
        result = False
        if type(signals) == list:
            if len(self.df_original.columns.tolist()) - 1 == len(signals) \
               and all(isinstance(n, int) for n in signals) \
               and all((n == 1 or n == -1) for n in signals):                
                result = True
        return result

    def pretty_original(self, tablefmt='psql'):
        return tabulate(self.df_original, headers='keys', tablefmt=tablefmt)

    def pretty_normalized(self, tablefmt='psql'):
        return tabulate(self.df_normalized, headers='keys', tablefmt=tablefmt)

    def pretty_weighted(self, tablefmt='psql'):
        return tabulate(self.df_weighted, headers='keys', tablefmt=tablefmt)

    def pretty_Xis(self, tablefmt='psql'):
        return tabulate(pd.DataFrame(self.df_pis, columns=['PIS']).join(pd.DataFrame(self.df_nis, columns=["NIS"])).T, headers='keys', tablefmt=tablefmt)
    
    def pretty_decision(self, tablefmt='psql'):
        return tabulate(self.df_decision, headers='keys', tablefmt=tablefmt)
        

