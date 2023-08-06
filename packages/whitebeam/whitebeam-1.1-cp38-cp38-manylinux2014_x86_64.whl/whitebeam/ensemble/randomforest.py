# random forests
# Whitebeam | Kieran Molloy | Lancaster University 2020

"""
This class implements RandomForests:
- https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf
"""


from whitebeam.base import DecisionTreeClassifier
import numpy as np

class RandomForestEnsemble():

    def __init__(self,
                base_estimator,
                base_params,
                n_estimators=100,
                is_classifier = True):
        self.base_estimator = base_estimator
        self.base_params = base_params.copy()
        self.n_estimators = n_estimators
        self.estimators = []

        self.is_classifier = is_classifier

    def fit(self, X, y):

        X = X.astype(np.float)
        y = y.astype(np.float)
 
        whitebeam_tmp = DecisionTreeClassifier()
        whitebeam_tmp.init_summary(X)
        xdim, summary, summaryn = whitebeam_tmp.get_summary()
        for i in range(self.n_estimators):
            estimator = self.base_estimator(**self.base_params)
            estimator.set_summary(xdim, summary, summaryn)
            estimator.fit(X, y, init_summary=False)
            self.estimators.append(estimator)

    def predict(self, X):
        n, m = X.shape
        y_hat = np.zeros(n) 
        k = len(self.estimators)
        for estimator in self.estimators:
            y_hat += estimator.predict(X) 
        y_hat /= k

        if self.is_classifier:
            return np.around(y_hat)
        else:
            return y_hat

    def dump(self, columns=[]): 
        return [estimator.dump(columns) 
                for estimator in self.estimators]
      





