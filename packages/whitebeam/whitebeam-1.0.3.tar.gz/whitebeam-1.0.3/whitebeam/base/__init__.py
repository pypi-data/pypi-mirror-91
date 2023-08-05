## just a casual empty init file :D

"""
The :mod:`whitebeam.base` module includes decision tree-based models for
classification and regression.
"""

from .alpha import AlphaTree
from .c45 import C45Tree
from .cart import DecisionTree
from .friedman import FriedmanTree
from .regr import RegTree
from .xgb import XGBTree

__all__ = ["AlphaTree",
           "C45Tree", "DecisionTree",
           "FriedmanTree", "RegTree", "XGBTree"]