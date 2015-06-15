# -*- coding: utf-8 -*-
"""
Adds CSV columns that are the result of arithmetic operations on other columns.
"""

import os
import sys

import numpy as np

import text_mtx_rw

def _find_unique_index(elt, arr):
    idxs = np.flatnonzero(elt == np.array(arr))
    if len(idxs) != 1:
        raise ValueError('found {0} indexes (instead of 1) for {1} in {2}'.format(
            len(idxs), elt, arr))
    return idxs[0]

def _augment_with_combinations(data, attrs, insts, factorset1, factorset2, 
        fxn=lambda x,y: x*y, fxn_symb='x'):
    fctr1_idxs = [_find_unique_index(fctr, attrs) for fctr in factorset1]
    fctr2_idxs = [_find_unique_index(fctr, attrs) for fctr in factorset2]
    
    n_rows = data.shape[0]
    for idx1 in fctr1_idxs:
        for idx2 in fctr2_idxs:
            newvals = fxn(data[:, idx1], data[:, idx2])
            data = np.hstack((data, newvals.reshape(n_rows, 1)))
            attrs.append(attrs[idx1] + fxn_symb + attrs[idx2])
    return (data, attrs, insts)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: augment_with_products in_file out_file"
        
    in_filepath = sys.argv[1]
    out_filepath = sys.argv[2]
    
    if os.path.exists(out_filepath):
        sys.stderr.write("ERROR: {0} already exists".format(out_filepath))
        sys.exit(1)
        
    (data, attrs, insts) = text_mtx_rw.read_mtx_info(in_filepath)
    (data, attrs, insts) = _augment_with_combinations(data, attrs, insts,
        ['BCA'], ['RGDPL'], lambda x,y: x/y, fxn_symb='per')
    (data, attrs, insts) = _augment_with_combinations(data, attrs, insts, 
        ['KC', 'KG', 'KI'], ['RGDPL'], lambda x,y: x*y, fxn_symb='x')
    (data, attrs, insts) = _augment_with_combinations(data, attrs, insts, 
        ['KCxRGDPL', 'KGxRGDPL', 'KIxRGDPL', 'RGDPCH', 'RGDPL', 'RGDPL2'], 
        ['POP'], lambda x,y: x*y, fxn_symb='x')
        
#    (data, attrs, insts) = text_mtx_rw.read_mtx_info(in_filepath)
#    (data, attrs, insts) = _augment_with_combinations(data, attrs, insts,
#        ['ATBOILIMP', 'ATBOILEXP'], ['ATBOILTOT'], lambda x,y: x/y, fxn_symb='per')
#    (data, attrs, insts) = _augment_with_combinations(data, attrs, insts,
#        ['ATBOILIMP'], ['ATBOILEXP'], lambda x,y: x/y, fxn_symb='per')
        
    text_mtx_rw.write_mtx_info(out_filepath, data, attrs, insts)