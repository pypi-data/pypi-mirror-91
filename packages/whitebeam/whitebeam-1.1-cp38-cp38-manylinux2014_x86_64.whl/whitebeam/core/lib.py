# main library functions
# Whitebeam | Kieran Molloy | Lancaster University 2020


"""
This module defines the Whitebeam class and its basic templates.
The Whitebeam class implments splitting data and constructing decision rules.
User need to provide two additional functions to complete the Whitebeam class:
- find_split()
- is_leaf()
"""

from whitebeam.core._whitebeam import (
    reorder, 
    create_avc,
    apply_tree)
from whitebeam.utils.util import (
    reconstruct_tree,
    get_xdim,
    get_summaryn,
    get_summary,
    get_child_branch)
import numpy as np
import json
from joblib import parallel_backend, Parallel, delayed, cpu_count
from scipy.special import expit
import time
import logging

class Whitebeam:
    """Base class for decision trees.
    Warning: This class should not be used directly.
    Use derived classes instead.
    lol. copied this comment from sklearn docs
    """

    def __init__(self, 
                find_split,
                is_leaf, 
                n_hist_max = 512, 
                subsample = 1.0, # subsample rate for rows (samples)
                random_state = None,
                z_type = "M2",
                n_jobs = -1,
                is_classifier=True):
        """Initialise a tree

        Args:
            find_split (function): splitting function
            is_leaf (function): node checking function
            n_hist_max (int, optional): [description]. Defaults to 512.
            subsample (float, optional): Subsample Rate for Rows. Defaults to 1.0.
            z_type (str, optional): Objective Type. Defaults to "M2".
            n_jobs (int, optional): Num of Threads. Defaults to -1.
            is_classifier (bool, optional): Type of Tree. Defaults to True.
        """        

        self.find_split = find_split # user-defined
        self.is_leaf = is_leaf       # user-defined
        self.n_hist_max = n_hist_max
        self.subsample = np.clip(subsample, 0.0, 1.0)
        self.random_state = random_state
        self.z_type = z_type

        # TODO : change to function / proper attribute
        self.is_classifier = is_classifier

        self.leaves = []
        self.feature_importances_ = None
        self.n_features_ = 0
        self.tree_ind   = np.zeros((1,6), dtype=np.int)
        self.tree_val   = np.zeros((1,2), dtype=np.float)
        self.mask       = None
        self.xdim       = None
        self.summary    = None
        self.summaryn   = None
        self.n_jobs     = n_jobs
        if self.n_jobs < 0:
            self.n_jobs = cpu_count()

    def get_avc(self, X, y, z, i_start, i_end, parallel):
        """Calculate AVC matrix

        Args:
            X (array): Data Array
            y (array): Target Array
            z ([type]): [description]
            i_start ([type]): [description]
            i_end ([type]): [description]
            parallel ([type]): [description]

        Returns:
            [type]: [description]
        """
        n, m = X.shape
        y_i = y[i_start:i_end]
        z_i = z[i_start:i_end]
        self.summary[:,3:] = 0  # initialize canvas
        self.summaryn[:,1:] = 0 # initialize canvas for NA

        # TODO: smart guidance on "n_jobs"
        k = int(np.ceil(m/self.n_jobs))
        def p_create_avc(i):
            j_start = i*k
            if j_start > m-1:
                return 1
            j_end = min(m, (i+1)*k)
            jj_start = int(self.xdim[j_start,4]*2)
            jj_end = int(self.xdim[j_end-1,4]*2 + 
                        self.xdim[j_end-1,3]*2)
            X_ij = X[i_start:i_end,j_start:j_end]
            xdim_j = self.xdim[j_start:j_end,:]
            summary_j = self.summary[jj_start:jj_end,:]
            summaryn_j = self.summaryn[j_start:j_end,:]
            create_avc(X_ij, y_i, z_i, xdim_j, summary_j, summaryn_j)
            return 0

        #t0 = time.time()
        parallel(delayed(p_create_avc)(i) for i in range(self.n_jobs))
        #t1 = time.time() - t0
        #print(i_end-i_start, t1)

        return self.summary

    def split_branch(self, X, y, z, branch, parallel):
        """Splits the data (X, y) into two children based on 
           the selected splitting variable and value pair.
        """

        i_start = branch["i_start"]
        i_end = branch["i_end"]
   
        # Get AVC-GROUP
        avc = self.get_avc(X, y, z, i_start, i_end, parallel)
        if avc.shape[0] < 2:
            branch["is_leaf"] = True
            return [branch]

        # Find a split SS: selected split
        ss = self.find_split(avc)     
        if (not isinstance(ss, dict) or
            "selected" not in ss):
            branch["is_leaf"] = True
            return [branch]

        svar = ss["selected"][1]
        sval = ss["selected"][2]
        missing = ss["selected"][9]

        i_split = reorder(X, y, z, i_start, i_end, 
                            svar, sval, missing)

        if i_split==i_start or i_split==i_end:
            # NOTE: this condition may rarely happen
            #       We just ignore this case, and stop the tree growth
            branch["is_leaf"] = True
            return [branch]

        left_branch = get_child_branch(ss, branch, i_split, "@l")
        left_branch["is_leaf"] = self.is_leaf(left_branch, branch)

        right_branch = get_child_branch(ss, branch, i_split, "@r")
        right_branch["is_leaf"] = self.is_leaf(right_branch, branch) 

        return [left_branch, right_branch]

    def grow_tree(self, X, y, z, branches, parallel):
        """Grows a tree by recursively partitioning the data (X, y)."""
        branches_new = []
        leaves_new = []

        for branch in branches:
            for child in self.split_branch(X, y, z, branch, parallel):
                if child["is_leaf"]:
                    leaves_new.append(child)
                else:
                    branches_new.append(child)
        return branches_new, leaves_new

    def fit(self, X, y, init_summary=True, parallel=None): 
        """Fit a tree to the data (X, y)."""

        n, m = X.shape
        X = X.astype(np.float, order="C", copy=True)
        y = y.astype(np.float, order="C", copy=True)
        if self.z_type=="M2":
            z = np.square(y)
        elif self.z_type=="Hessian": # bernoulli hessian
            p = expit(y) 
            z = p * (1.0 - p)
        else:
            z = np.ones(n) 
 
        if self.subsample < 1.0:
            np.random.seed(self.random_state)
            self.mask = (np.random.rand(n) < self.subsample)
            X = X[self.mask,:]
            y = y[self.mask]
            z = z[self.mask]
            n, m = X.shape
        else:
            self.mask = np.full(n, True, dtype=np.bool)

        self.n_features_ = m

        branches = [{"_id": "ROOT",
                    "is_leaf": False,
                    "depth": 0,
                    "eqs": [],
                    "i_start": 0,
                    "i_end": n,
                    "y": np.mean(y),
                    "y_lst": [], 
                    "n_samples": n}]

        if init_summary:
            self.init_summary(X)

        self.leaves = []
        if self.xdim is None or self.summary is None or self.summaryn is None:
            logging.error("canvas is not initialized. no tree trained")
            return 1

        if parallel is None:
            with Parallel(n_jobs=self.n_jobs, prefer="threads") as parallel:
                while len(branches) > 0:
                    branches, leaves_new = self.grow_tree(X, y, z, 
                                                branches, parallel)
                    self.leaves += leaves_new
        else:
            # parallel-context is already given
            while len(branches) > 0:
                branches, leaves_new = self.grow_tree(X, y, z, 
                                            branches, parallel)
                self.leaves += leaves_new

        # integer index for leaves (from 0 to len(leaves))
        for i, leaf in enumerate(self.leaves): 
            leaf["index"] = i 
        self.update_feature_importances()
        self.tree_ind, self.tree_val = reconstruct_tree(self.leaves)
        return 0

    def predict(self, X, output_type="response"):
        """Predict y by applying the trained tree to X."""
        X = X.astype(np.float)
        n, m = X.shape
        y = np.zeros(n, dtype=np.float)
        out = apply_tree(self.tree_ind, self.tree_val, X, y, output_type)

        #print({"out" : out})

        # binary classifier only at the moment
        if self.is_classifier:
            return np.around(out)
        else:
            return out 

    def init_summary(self, X):
        self.xdim = get_xdim(X, self.n_hist_max)
        self.summary = get_summary(self.xdim)
        self.summaryn = get_summaryn(self.xdim)

    def set_summary(self, xdim, summary, summaryn):
        self.xdim = xdim
        self.summary = summary
        self.summaryn = summaryn
        self.summary[:,3:] = 0  # initialize canvas
        self.summaryn[:,1:] = 0 # initialize canvas for NA
 
    def get_summary(self):
        return self.xdim, self.summary, self.summaryn

    def is_stochastic(self):
        return self.subsample < 1.0

    def get_mask(self):
        return self.mask
    
    def get_oob_mask(self):
        """Returns a mask array for OOB samples"""
        return ~self.mask

    def get_ttab(self):
        """Returns tree tables (ttab). 
            ttab consists of tree_ind (np_array) and tree_val (np_array).
            tree_ind stores tree indices - integer array. 
            tree_val stores node values - float array.
        """
        return self.tree_ind, self.tree_val

    def dump(self, columns=[], compact=False):
        """Dumps the trained tree in the form of array of leaves"""
        def default(o):
            if isinstance(o, np.int64): return int(o)
            raise TypeError

        n_col = len(columns)
        for leaf in self.leaves:
            for eq in leaf["eqs"]:
                if eq["svar"] < n_col:
                    eq["name"] = columns[int(eq["svar"])]
        out = json.loads(json.dumps(self.leaves, default=default))
        if compact:
            suplst = ["i_start", "i_end", "depth",
                        "_id", "n_samples", "y_lst", 
                        "is_leaf", "prune_status"] # suppress
            out_cmpct = []
            for leaf in out:
                for key in suplst:
                    leaf.pop(key, None)
                out_cmpct.append(leaf) 
            return out_cmpct
        else:
            return out

    def load(self, leaves, columns=None):
        """Loads a new tree in the form of array of leaves"""
        self.leaves = leaves
        self.tree_ind, self.tree_val = reconstruct_tree(self.leaves)
        return None

    def get_sibling_id(self, leaf_id):
        """Returns a sibling ID for the given leaf_id.
           Siblings are the nodes that are at the same level 
            with the same parent node.
        """
        sibling_id = None
        if leaf_id[-1]=="L":
            sibling_id = leaf_id[:-1] + "R"
        elif leaf_id[-1]=="R":
            sibling_id = leaf_id[:-1] + "L"
        sibling_leaf = [leaf for leaf in self.leaves 
                        if leaf["_id"]==sibling_id]
        if len(sibling_leaf) == 0:
            sibling_id = None
        return sibling_id 

    def get_sibling_pairs(self):
        """Returns an array of sibling pairs. 
            For more info, see the get_sibling_id
        """
        id2index = {leaf["_id"]:i for i, leaf in enumerate(self.leaves)}
        leaf_ids = [k for k in id2index.keys()]
        sibling_pairs = []
        while len(leaf_ids) > 0:
            leaf_id = leaf_ids.pop()
            sibling_id = self.get_sibling_id(leaf_id) 
            if sibling_id is not None:
                if sibling_id in leaf_ids:
                    leaf_ids.remove(sibling_id)
                sibling_pairs.append((id2index[leaf_id], 
                                      id2index[sibling_id]))
            else:
                sibling_pairs.append((id2index[leaf_id], None))
        return sibling_pairs
   
    def get_feature_importances(self):
        return self.feature_importances_
 
    def update_feature_importances(self):
        """Returns a modified feature importance.
            This formula takes into account of node coverage and leaf value.
        """
        if self.n_features_ == 0:
            return None
        self.feature_importances_ = np.zeros(self.n_features_)
        cov = 0
        J = len(self.leaves)
        if J > 0:
            for j, leaf in enumerate(self.leaves):
                gamma_j = np.abs(leaf["y"])
                cov_j = leaf["n_samples"]
                cov += cov_j
                eff_j = cov_j*gamma_j
                for eq in leaf["eqs"]:
                    self.feature_importances_[eq["svar"]] += eff_j
            self.feature_importances_ /= J
            self.feature_importances_ /= cov
        return self.feature_importances_ 

