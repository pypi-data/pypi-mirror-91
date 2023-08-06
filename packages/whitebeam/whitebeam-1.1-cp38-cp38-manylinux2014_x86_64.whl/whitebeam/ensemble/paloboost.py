"""
This class implements PaloBoost, an imprvoed Stochastic Gradient TreeBoost
 that is robust to overfitting and can provide robust performance.
"""

from whitebeam.base import XGBoostedRegressor

from collections import Counter

import numpy as np
from scipy.special import expit

import logging
from joblib import Parallel, delayed, cpu_count

PRECISION = 1e-5

class PaloBoostEnsemble():

    def __init__(self,
                distribution="gaussian",
                learning_rate=0.1,
                subsample=0.7,
                subsample_splts=1.0,
                max_depth=3,
                n_estimators=100,
                reg_lambda=1.0,
                do_prune=True,
                n_jobs=-1,
                random_state=0,
                min_samples_split=2,
                min_samples_leaf=1):
        self.base_estimator = XGBTree
        self.n_jobs = n_jobs
        if self.n_jobs < 0:
            self.n_jobs = cpu_count()
        self.base_params = {"subsample": subsample,
                            "max_depth": max_depth,
                            "distribution": distribution,
                            "reg_lambda": reg_lambda,
                            "random_state": random_state,
                            "subsample_splts": subsample_splts,
                            "min_samples_split": min_samples_split,
                            "min_samples_leaf": min_samples_leaf,
                            "n_jobs": n_jobs}
        self.distribution = distribution
        self.nu = learning_rate
        self.n_estimators = n_estimators
        self.reg_lambda = reg_lambda
        self.do_prune = do_prune

        self.intercept = 0.0
        self.estimators = []
        self.prune_stats = []
        self.lr_stats = []
        self.feature_importances_ = None
        self.n_features_ = 0

    def fit(self, X, y):

        def initialize(y):
            if self.distribution == "gaussian":
                return np.mean(y)
            elif self.distribution == "bernoulli":
                p = np.clip(np.mean(y), PRECISION, 1-PRECISION)
                return np.log(p/(1-p))
            else:
                return np.mean(y)

        def gradient(y, y_hat):
            if self.distribution == "gaussian":
                return y - y_hat
            elif self.distribution == "bernoulli":
                return y - expit(y_hat)
            else:
                return y - y_hat

        def get_nu(y, y_hat, oob_mask, gamma, nu):

            min_n_oob = 1
            if (np.sum(oob_mask) < min_n_oob or
                np.abs(gamma) < PRECISION):
                return 0.0

            y_oob = y[oob_mask]
            y_hat_oob = y_hat[oob_mask]
           
            nu_max = nu 
            nu_min = 0 # NOTE
            if self.distribution == "gaussian": 
                nu = np.mean(y_oob - y_hat_oob)/gamma
            elif self.distribution == "bernoulli":
                num = np.sum(y_oob) + 0.5
                denom = np.sum((1-y_oob)*np.exp(y_hat_oob)) + 1.0
                nu = np.log(num/denom)/gamma
            nu = np.clip(nu, nu_min, nu_max) 

            return nu

        self.estimators = []
        self.prune_stats = []
        self.lr_stats = []

        X = X.astype(np.float)
        y = y.astype(np.float)
        if "random_state" not in self.base_params:
            self.base_params["random_state"] = 0

        n, m = X.shape 
        self.n_features_ = m
        self.feature_importances_ = np.zeros(m)
        self.intercept = initialize(y)
        
        whitebeam_tmp = self.base_estimator()
        whitebeam_tmp.init_cnvs(X)
        xdim, cnvs, cnvsn = whitebeam_tmp.get_cnvs()
        y_hat = np.full(n, self.intercept)

        with Parallel(n_jobs=self.n_jobs, prefer="threads") as parallel:
            for i in range(self.n_estimators):

                self.base_params["random_state"] += 1
                z = gradient(y, y_hat)

                estimator = self.base_estimator(**self.base_params)
                estimator.set_cnvs(xdim, cnvs, cnvsn)
                estimator.fit(X, z, init_cnvs=False, parallel=parallel)

                oob_mask = estimator.get_oob_mask()
                do_oob = estimator.is_stochastic()

                # NOTE: prune
                if do_oob and self.do_prune:
                    n_leaves_bf_prune = len(estimator.dump())
                    estimator.prune(X, y, y_hat, self.nu)
                    n_leaves_af_prune = len(estimator.dump())
                    self.prune_stats.append([i, n_leaves_bf_prune,
                                            n_leaves_af_prune])

                t = estimator.predict(X, "index")
                leaves = estimator.dump()
                avg_nu = 0.0
                for j, leaf in enumerate(leaves):
                    mask_j = (t==j)
                    gamma_j = leaf["y"]

                    # NOTE: learning-rate adjustment
                    nu_j = self.nu
                    cov_j = np.sum(mask_j)
                    if do_oob:
                        oob_mask_j = np.logical_and(mask_j, oob_mask)
                        nu_j = get_nu(y, y_hat, oob_mask_j, gamma_j, nu_j)

                    leaf["y"] = gamma_j * nu_j
                    y_hat[mask_j] += (gamma_j * nu_j)
                    avg_nu += (nu_j * cov_j)

                avg_nu = avg_nu/n
                self.lr_stats.append([i, avg_nu])
                estimator.load(leaves)
                estimator.update_feature_importances()
                self.estimators.append(estimator)

        self.update_feature_importances()

        # Done fit()

    def predict(self, X):

        n, m = X.shape
        y_hat = np.full(n, self.intercept) 

        for estimator in self.estimators:
            y_hat += estimator.predict(X) 

        if self.distribution == "bernoulli":
            y_hat = expit(y_hat)
            y_mat = np.zeros((y_hat.shape[0], 2))
            y_mat[:,0] = 1.0 - y_hat
            y_mat[:,1] = y_hat
            return y_mat
        else:
            return y_hat

    def predict_proba(self, X):
        return self.predict(X)

    def staged_predict(self, X):
        return self.staged_predict_proba(X)

    def staged_predict_proba(self, X):
        n, m = X.shape
        y_hat = np.full(n, self.intercept) 
        for stage, estimator in enumerate(self.estimators):
            y_hat += estimator.predict(X)
            if self.distribution == "bernoulli":
                y_mat = np.zeros((y_hat.shape[0],2))
                y_mat[:,1] = expit(y_hat)
                y_mat[:,0] = 1.0 - y_mat[:,1]
                yield y_mat
            else:
                yield y_hat 

    def update_feature_importances(self):
        fi = np.zeros(self.n_features_)        
        for est in self.estimators:
            fi += est.get_feature_importances()
        self.feature_importances_ = fi
        return self.feature_importances_

    def get_staged_feature_importances(self):
        fi = np.zeros(self.n_features_)        
        for i, est in enumerate(self.estimators):
            fi += est.get_feature_importances()
            yield fi

    def dump(self): 
        estimators = [estimator.dump(compact=True)
                        for estimator in self.estimators]
        return {"distribution": self.distribution,
                "learning_rate": self.nu,
                "n_estimators": self.n_estimators,
                "intercept": self.intercept, 
                "estimators": estimators}
   
    def load(self, model):
        self.distribution = model["distribution"]
        self.nu = model["learning_rate"]
        self.n_estimators = model["n_estimators"]
        self.intercept = model["intercept"] 
        for estjson in model["estimators"]:
            est = self.base_estimator()
            est.load(estjson)
            self.estimators.append(est)
        return None
 
    def get_prune_stats(self):
        return self.prune_stats

    def get_lr_stats(self):
        return self.lr_stats 


