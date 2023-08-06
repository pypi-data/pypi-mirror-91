# c4.5 tree
# Whitebeam | Kieran Molloy | Lancaster University 2020

"""
This class implements C45 by inheriting the alpha tree (alpha=1).
"""

from whitebeam.base.ccp import CCPTreeClassifier
import numpy as np

class C45TreeClassifier(CCPTreeClassifier):

    def __init__(self, 
                max_depth=5, 
                min_samples_split=2,
                min_samples_leaf=1):

        CCPTreeClassifier.__init__(self, 
                        alpha=1.0,
                        max_depth=max_depth,
                        min_samples_split=min_samples_split,
                        min_samples_leaf=min_samples_leaf)


