from whitebeam.base import AlphaTree, C45Tree, DecisionTree, RegTree, XGBTree

from sklearn.metrics import roc_auc_score
import numpy as np
import pytest

from test.utils import createSomeData

def test_c45_auc():

    X_train, X_test, y_train, y_test = createSomeData()

    max_depth = 4
    model = C45Tree(max_depth=max_depth)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    auc = roc_auc_score(y_test, y_hat)
    
    assert auc > 0.5

def test_cart_auc():

    X_train, X_test, y_train, y_test = createSomeData()

    max_depth = 4
    model = DecisionTree(max_depth=max_depth)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    auc = roc_auc_score(y_test, y_hat)

    assert auc > 0.5
    
def test_alpha_auc():

    X_train, X_test, y_train, y_test = createSomeData()

    max_depth = 4
    model = AlphaTree(alpha=3.0, max_depth=max_depth)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    auc = roc_auc_score(y_test, y_hat)

    assert auc > 0.5

def test_regression_auc():

    X_train, X_test, y_train, y_test = createSomeData()

    max_depth = 4
    model = RegTree(max_depth=max_depth)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    auc = roc_auc_score(y_test, y_hat)

    assert auc > 0.5

def test_xgboost_auc():

    X_train, X_test, y_train, y_test = createSomeData()

    max_depth = 4
    model = XGBTree(max_depth=max_depth)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    auc = roc_auc_score(y_test, y_hat)

    assert auc > 0.5




    


