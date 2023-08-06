# stochastic gradient tree boost
# Whitebeam | Kieran Molloy | Lancaster University 2020

"""
This class implements Stochastic Gradient TreeBoost (SGTB) in:
- https://statweb.stanford.edu/~jhf/ftp/stobst.pdf
scikit-learn and R call this method GBM.
"""


from whitebeam.base import FriedmanTreeClassifier
import numpy as np
from scipy.special import expit
import time
import logging
from joblib import Parallel, delayed, cpu_count

PRECISION = 1e-5

class StochasticGradientBoostedClassifier():

    def __init__(self,
                subsample=0.7,
                max_depth=3,
                learning_rate=0.1,
                n_estimators=100,
                reg_lambda=0.1,
                n_jobs=-1,
                random_state=0,
                distribution = "bernoulli"):
        self.base_estimator = FriedmanTreeClassifier
        self.n_jobs = n_jobs
        if self.n_jobs < 0:
            self.n_jobs = cpu_count()
        self.base_params = {"subsample": subsample,
                            "max_depth": max_depth,
                            "random_state": random_state,
                            "n_jobs": self.n_jobs}
        self.distribution = distribution
        self.nu = learning_rate
        self.n_estimators = n_estimators
        self.reg_lambda = reg_lambda
        self.intercept = 0.0
        self.estimators = []
        self.feature_importances_ = None
        self.n_features_ = 0

    def fit(self, X, y):

        def initialize(y):
            if self.distribution == "gaussian":
                return np.mean(y)
            elif self.distribution == "bernoulli":
                p = np.clip(np.mean(y), PRECISION, 1-PRECISION)
                return np.log(p / (1.0 - p))
            else:
                return np.mean(y)

        def gradient(y, y_hat):
            if self.distribution == "gaussian":
                return y - y_hat
            elif self.distribution == "bernoulli":
                return y - expit(y_hat)
            else:
                return y - y_hat

        def estimate_gamma(y, y_hat):
            if self.distribution == "gaussian": 
                return np.mean(y-y_hat)
            elif self.distribution == "bernoulli":
                p = expit(y_hat)
                num = np.sum(y-p)
                denom = np.sum(p * (1-p)) + self.reg_lambda
                return num / denom
            else:
                return np.mean(y-y_hat)

        # initialise empty lists of estimators
        self.estimators = []

        # get unique values in the target column
        classes_k, y_encoded = np.unique(y, return_inverse=True)
        self.classes_ = classes_k
        self.n_classes_ = classes_k.shape[0]

        # define x and y, as well as random state
        X = X.astype(np.float)
        y = y.astype(np.float)
        if "random_state" not in self.base_params:
            self.base_params["random_state"] = 0
 
        # shape of X, n rows, m columns
        n, m = X.shape 
        self.intercept = initialize(y)
        self.n_features_ = m
        self.feature_importances_ = np.zeros(m)

        whitebeam_tmp = self.base_estimator()
        whitebeam_tmp.init_summary(X)
        xdim, summary, summaryn = whitebeam_tmp.get_summary()
        y_hat = np.zeros(n) + self.intercept
        with Parallel(n_jobs=self.n_jobs, prefer="threads") as parallel:
            for i in range(self.n_estimators):
                self.base_params["random_state"] += 1
                z = gradient(y, y_hat)
     
                estimator = self.base_estimator(**self.base_params)
                estimator.set_summary(xdim, summary, summaryn)

                estimator.fit(X, z, init_summary=False, parallel=parallel)

                do_oob = estimator.is_stochastic()
                oob_mask = estimator.get_oob_mask()
                t = estimator.predict(X, "index")
                leaves = estimator.dump()

                for j, leaf in enumerate(leaves):
                    leaf_mask = (t==j)
                    mask_j = np.logical_and(leaf_mask, ~oob_mask)
                    gamma_j = estimate_gamma(y[mask_j], y_hat[mask_j])
                    leaf["_y"] = leaf["y"]
                    leaf["y"] = gamma_j * self.nu
                    y_hat[leaf_mask] += leaf["y"]

                estimator.load(leaves)
                estimator.update_feature_importances()
                self.estimators.append(estimator)

        self.update_feature_importances()

        # Done fit()

    def predict(self, X, output_type="response", test_state = False):

        n, m = X.shape
        y_hat = np.full(n, self.intercept) 

        for estimator in self.estimators:
            y_hat += estimator.predict(X) 

        print(y_hat)

        if self.distribution == "bernoulli":
            # logistic sigmoid for ndarrays
            y_hat = expit(y_hat)

            # y_mat is the 
            y_mat = np.zeros((y_hat.shape[0], 2)) 
            y_mat[:,0] = 1.0 - y_hat
            y_mat[:,1] = y_hat

            # print(y_mat)
            return np.argmax(y_mat, axis=1)
        else:
            return y_hat

    def predict_proba(self, X):
        proba =  self.predict(X)

        proba = proba[:, :self.n_classes_]

        # normalising procedure
        normalizer = proba.sum(axis=1)[:, np.newaxis]
        normalizer[normalizer == 0.0] = 1.0
        proba /= normalizer

        # return the class probabilities of the input samples
        return proba


    def staged_predict(self, X):
        return self.staged_predict_proba(X)

    def staged_predict_proba(self, X):

        n, m = X.shape
        y_hat = np.full(n, self.intercept) 

        for stage, estimator in enumerate(self.estimators):
            y_hat += estimator.predict(X)

            if self.distribution == "bernoulli":

                # TODO: this is where multiclass can probably be implemented
                y_mat = np.zeros((y_hat.shape[0], 2)) 

                # logistic sigmoid for ndarrys
                y_mat[:,1] = expit(y_hat)

                # setup ymax expectation for class 0 or 1.
                y_mat[:,0] = 1.0 - y_mat[:,1]

                # yield the highest value for each row
                yield np.argmax(y_mat, axis=1)
            else:
                # yield y estimations
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

    def dump(self, columns=[]): 
        estimators = [estimator.dump(columns)
                        for estimator in self.estimators]
        return {"intercept": self.intercept, 
                "estimators": estimators}
    
    




