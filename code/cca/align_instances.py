# -*- coding: utf-8 -*-
"""
Reorders and (where necessary) drops rows from two input tables so that 
column i of table 1 matches column i of table 2. This is useful for analyses
using data consisting of matched pairs of vectors.
"""

import logging
import numpy as np
import os
import sys

from text_mtx_rw import read_mtx_info, write_mtx_info

logger = logging.getLogger('align_instances')

def align_instances(data1, insts1, data2, insts2):
    sidxs1 = np.argsort(insts1)
    sidxs2 = np.argsort(insts2)
    keep1 = []
    keep2 = []
    rm1 = []
    rm2 = []
    pos1 = 0
    pos2 = 0
    while (pos1 < len(sidxs1)) and (pos2 < len(sidxs2)):
        cur_idx1 = sidxs1[pos1]
        cur_idx2 = sidxs2[pos2]
        elt1 = insts1[cur_idx1]
        elt2 = insts2[cur_idx2]
        if elt1 == elt2:
            keep1.append(cur_idx1)
            keep2.append(cur_idx2)
            pos1 = pos1 + 1
            pos2 = pos2 + 1
        elif elt1 < elt2:
            rm1.append(cur_idx1)
            pos1 = pos1 + 1
        elif elt1 > elt2:
            rm2.append(cur_idx2)
            pos2 = pos2 + 1
        else:
            raise ValueError('incomparable (nan?) sort indexes')
    rm1 = rm1 + list(sidxs1[pos1:])
    rm2 = rm2 + list(sidxs2[pos2:])    
    
    rm_elts1 = [insts1[i] for i in rm1]
    rm_elts2 = [insts2[i] for i in rm2]
    keep_elts1 = [insts1[i] for i in keep1]
    keep_elts2 = [insts2[i] for i in keep2]
    assert len(np.intersect1d(rm_elts1, rm_elts2)) == 0
    assert len(np.intersect1d(rm_elts1, keep_elts2)) == 0
    assert len(np.intersect1d(keep_elts1, rm_elts2)) == 0
    assert len(np.intersect1d(rm_elts1, keep_elts1)) == 0
    assert len(np.intersect1d(keep_elts2, rm_elts2)) == 0
    
    logger.info("The following instances could not be matched and were removed:")
    if len(rm1) <= 10:
        logger.info("data1: " + str([insts1[i] for i in rm1]))
    else:
        logger.info("data1: <{0} instances>".format(len(rm1)))
    for i in rm1:
        logger.info(str(insts1[i]))
    if len(rm2) <= 10:
        logger.info("data2: " + str([insts2[i] for i in rm2]))
    else:
        logger.info("data2: <{0} instances>".format(len(rm2)))
    for i in rm2:
        logger.info(str(insts2[i]))
        
    if (len(keep1)) == 0 or (len(keep2) == 0):
        logger.debug("first instances, set 1: {0}".format(insts1[:10]))
        logger.debug("first instances, set 2: {0}".format(insts2[:10]))
        logger.error("ERROR: no instance names matched between sets")
        raise ValueError("no instance names matched between sets")      
    
#    print "data1 (full): {0}".format([insts1[i] for i in rm1])
#    print "data2 (full): {0}".format([insts2[i] for i in rm2])
    
    sys.stdout.flush()
    algn_data1 = data1[np.ix_(keep1, range(data1.shape[1]))]
    algn_data2 = data2[np.ix_(keep2, range(data2.shape[1]))]
    algn_insts1 = [insts1[i] for i in keep1]
    algn_insts2 = [insts2[i] for i in keep2]
    
    assert np.all(pair[0] == pair[1] for pair in zip(algn_insts1, algn_insts2))    
    
    return (algn_data1, algn_insts1, algn_data2, algn_insts2)
    
if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('usage: align_instances.py file_path_1 file_path_2 out_dir_path')
        sys.exit(1)
        
    logging.basicConfig(level=logging.DEBUG)
    
    file_path_1 = sys.argv[1]
    file_path_2 = sys.argv[2]
    out_dir_path = sys.argv[3]
    
    dname1 = os.path.basename(file_path_1).rpartition('.')
    dname1 = dname1[0] if dname1[0] else dname1[2]
    dname2 = os.path.basename(file_path_2).rpartition('.')
    dname2 = dname2[0] if dname2[0] else dname2[2]
    
    (data1, attrs1, inst1) = read_mtx_info(file_path_1)
    (data2, attrs2, inst2) = read_mtx_info(file_path_2)
    
    if len(data1.shape) != 2:
        logger.warning("data1 is not 2D")
    if len(data2.shape) != 2:
        logger.warning("data2 is not 2D")
    
    (data1, inst1, data2, inst2) = align_instances(data1, inst1, data2, inst2)
    
    write_mtx_info(out_dir_path + os.sep + 
        dname1 + '_matched-to_' + dname2 + '.csv', data1, attrs1, inst1)
    write_mtx_info(out_dir_path + os.sep + 
        dname2 + '_matched-to_' + dname1 + '.csv', data2, attrs2, inst2)