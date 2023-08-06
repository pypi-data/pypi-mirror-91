# fancy cython functions
# Whitebeam | Kieran Molloy | Lancaster University 2020

#cython: boundscheck=False
#cython: wrapround=False
#cython: cdivision=True

import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport isnan

# define default dtype
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

def reorder(X, y, z, i_start, i_end, j_split, split_value, missing):
    """Reorders the thing

    Args:
        X (2-d Numpy Array): X Values
        y (1-d Numpy Array): Y Values
        z (1-d Numpy Array): z Values
        i_start (integer): row index starting point
        i_end (integer): row index ending point
        j_split (integer): column index for splitting variable
        split_value (integer): split threshold value
        missing (boolean): Missing Values or not

    Returns:
        [integer]: head index
    """
    return _reorder(X, y, z, i_start, i_end, j_split, split_value, missing)

def create_avc(np.ndarray[DTYPE_t, ndim=2] X not None, 
        np.ndarray[DTYPE_t, ndim=1] y not None, 
        np.ndarray[DTYPE_t, ndim=1] z not None, 
        np.ndarray[DTYPE_t, ndim=2] xdim not None, 
        np.ndarray[DTYPE_t, ndim=2] summary not None, 
        np.ndarray[DTYPE_t, ndim=2] summaryn not None):
    """Calculate AVC Logic from component factors. And leave as component factors

    Returns:
        0: Build pass
    """        

    # canvas --> (create_avc) --> avc 
    # AVC: Attribute-Value Class group in RainForest
    _create_avc(X, y, z, xdim, summary, summaryn)
    return 0

def apply_tree(tree_ind, tree_val, X, y, output_type):
    """Apply trained tree to a dataset

    Args:
        tree_ind (2-d Numpy Array): base index
        tree_val (2-d Numpy Array): values
        X (2-d Numpy Array): X Values
        y (1-d Numpy Array): Y Values
        output_type (string): "index" returns indices

    Returns:
        1-d Numpy Array: Fitted Values
    """    
    if output_type == "index":
        return _apply_tree0(tree_ind, tree_val, X, y)
    else:
        return _apply_tree1(tree_ind, tree_val, X, y)

################################################################################
# cython functions

 
cdef size_t _reorder(
        np.ndarray[DTYPE_t, ndim=2] X, # X: 2-d numpy array (n x m)
        np.ndarray[DTYPE_t, ndim=1] y, # y: 1-d numpy array (n)
        np.ndarray[DTYPE_t, ndim=1] z, # z: 1-d numpy array (n)
        size_t i_start, # i_start: row index to start
        size_t i_end,  # i_end: row index to end
        size_t j_split,  # j_split: column index for the splitting variable
        double split_value,  # split_value: threshold
        size_t missing):


    cdef size_t j
    cdef size_t m = X.shape[1]
    cdef size_t i_head = i_start
    cdef size_t i_tail = i_end - 1
    cdef size_t do_swap = 0

    with nogil:
        while i_head <= i_tail:

            if i_tail == 0: 
                # if tail is 'zero', should break
                # otherwise, segmentation fault, 
                # as size_t has no sign. 0 - 1 => huge number
                break
            
            do_swap = 0 
            if isnan(X[i_head,j_split]):
                if missing == 1: # send the missing to the right node
                    do_swap = 1
            else:
                if X[i_head,j_split] >= split_value:
                    do_swap = 1

            if do_swap == 1:
                # swap X rows
                for j in range(m):
                    X[i_head,j], X[i_tail,j] = X[i_tail,j], X[i_head,j]
                # swap y, z values
                y[i_head], y[i_tail] = y[i_tail], y[i_head]
                z[i_head], z[i_tail] = z[i_tail], z[i_head]
                # decrease the tail index
                i_tail -= 1
            else:
                # increase the head index
                i_head += 1

    return i_head

# create the avc :D
cdef void _create_avc(
        np.ndarray[DTYPE_t, ndim=2] X, 
        np.ndarray[DTYPE_t, ndim=1] y, 
        np.ndarray[DTYPE_t, ndim=1] z, 
        np.ndarray[DTYPE_t, ndim=2] xdim, 
        np.ndarray[DTYPE_t, ndim=2] summary, 
        np.ndarray[DTYPE_t, ndim=2] summaryn):

    # indices
    cdef size_t i, j, k, k_raw, k_tld

    # matrix sizes
    cdef size_t n = X.shape[0]
    cdef size_t m = X.shape[1]

    # the current 'image'
    cdef size_t n_summary = <size_t> summary.shape[0]/2

    # 
    cdef size_t n_bin
    cdef size_t xdim0 = <size_t> xdim[0, 4]
    cdef double k_prox

    # iterators
    cdef double y_i, z_i

    # totals
    cdef double y_tot = 0.0
    cdef double z_tot = 0.0
    cdef double n_na, y_na, z_na

    # update E[y] & E[z]
    with nogil:

        # iterate over n dimensions
        for i in range(n):

            # get the indices
            y_i = y[i]
            z_i = z[i]

            # add to get the totals
            y_tot += y_i
            z_tot += z_i

            # iterate over m dimensions
            for j in range(m):

                #if xdim[j, 2] < 1e-12:
                #    continue

                # check isnan to prevent errors
                if isnan(X[i, j]):
                    # update summary
                    summaryn[j, 1] += 1
                    summaryn[j, 2] += y_i
                    summaryn[j, 3] += z_i
                else:

                    k_prox = (X[i, j] - xdim[j, 1])/xdim[j, 2]
                    if k_prox < 0:
                        k_prox = 0
                    elif k_prox > xdim[j, 3] - 1:
                        k_prox = xdim[j, 3] - 1
                    k = <size_t> (k_prox + (xdim[j, 4] - xdim0)*2)
                    summary[k, 3] += 1
                    summary[k, 4] += y_i
                    summary[k, 5] += z_i

        # accumulate stats
        for j in range(m):
            n_bin = <size_t> xdim[j, 3]
            
            for k_raw in range(1, n_bin): 
                k = <size_t> (k_raw + (xdim[j, 4] - xdim0)*2)
                summary[k, 3] += summary[k-1, 3] 
                summary[k, 4] += summary[k-1, 4] 
                summary[k, 5] += summary[k-1, 5] 
                # fill the right node at the same time
                summary[k, 6] = n - summary[k, 3] - summaryn[j, 1]
                summary[k, 7] = y_tot - summary[k, 4] - summaryn[j, 2]
                summary[k, 8] = z_tot - summary[k, 5] - summaryn[j, 3]

            # fill the right node
            k = <size_t> ((xdim[j, 4] - xdim0)*2)
            summary[k, 6] = n - summary[k, 3] - summaryn[j, 1]
            summary[k, 7] = y_tot - summary[k, 4] - summaryn[j, 2]
            summary[k, 8] = z_tot - summary[k, 5] - summaryn[j, 3]

        # missing values
        for j in range(m):

            n_bin = <size_t> xdim[j, 3]
            n_na = summaryn[j, 1]
            y_na = summaryn[j, 2]
            z_na = summaryn[j, 3]

            if n_na == 0:
                continue

            for k_raw in range(n_bin):
                k = <size_t> (k_raw + (xdim[j, 4] - xdim0)*2)
                k_tld = k + n_bin
                summary[k_tld, 3] = summary[k, 3]
                summary[k_tld, 4] = summary[k, 4]
                summary[k_tld, 5] = summary[k, 5]
                summary[k_tld, 6] = summary[k, 6]
                summary[k_tld, 7] = summary[k, 7]
                summary[k_tld, 8] = summary[k, 8]
                summary[k_tld, 9] = 1

                summary[k, 3] += n_na
                summary[k, 4] += y_na
                summary[k, 5] += z_na
                summary[k_tld, 6] += n_na
                summary[k_tld, 7] += y_na
                summary[k_tld, 8] += z_na

    # done _create_avc


## I am not entirely sure why, but this only works in this format
## but both are required, even though they are basically the same 
## function at this point

# output index
cdef np.ndarray[DTYPE_t, ndim=1] _apply_tree0(
                            np.ndarray[np.int_t, ndim=2] tree_ind, 
                            np.ndarray[DTYPE_t, ndim=2] tree_val, 
                            np.ndarray[DTYPE_t, ndim=2] X, 
                            np.ndarray[DTYPE_t, ndim=1] y):
    # Initialize node/row indicies
    cdef size_t i, t
    cdef size_t n_samples = X.shape[0]

    with nogil:
        for i in range(n_samples):
            t = 0
            while tree_ind[t,0] < 0:
                if isnan(X[i, tree_ind[t,1]]):
                    if tree_ind[t,2]==0:
                        t = tree_ind[t,3] 
                    else:
                        t = tree_ind[t,4] 
                else:
                    if X[i,tree_ind[t,1]] < tree_val[t,0]:
                        t = tree_ind[t,3]
                    else:
                        t = tree_ind[t,4]
            y[i] = tree_ind[t,5]
    return y

# output y values
cdef np.ndarray[DTYPE_t, ndim=1] _apply_tree1(
                            np.ndarray[np.int_t, ndim=2] tree_ind, 
                            np.ndarray[DTYPE_t, ndim=2] tree_val, 
                            np.ndarray[DTYPE_t, ndim=2] X, 
                            np.ndarray[DTYPE_t, ndim=1] y):
    # Initialize node/row indicies
    cdef size_t i, t
    cdef size_t n_samples = X.shape[0]

    with nogil:
        for i in range(n_samples):
            t = 0
            while tree_ind[t,0] < 0:
                if isnan(X[i, tree_ind[t,1]]):
                    if tree_ind[t,2]==0:
                        t = tree_ind[t,3] 
                    else:
                        t = tree_ind[t,4] 
                else:
                    if X[i,tree_ind[t,1]] < tree_val[t,0]:
                        t = tree_ind[t,3]
                    else:
                        t = tree_ind[t,4]
            y[i] = tree_val[t,1]
    return y