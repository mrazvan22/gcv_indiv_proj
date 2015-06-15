# -*- coding: utf-8 -*-
"""
Combines per-year CSVs (of network data) into a single CSV with country_year
instances.
"""

import numpy as np
import os
import sys

import text_mtx_rw

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("usage: join_econ_network_years in_dir out_file\n")
        sys.exit(1)
    
    in_dirpath = sys.argv[1]
    out_filepath = sys.argv[2]
    
    combined_data = None
    combined_attr_names = []
    combined_inst_names = []
    
    for in_fname in os.listdir(in_dirpath):
        if in_fname.endswith('.csv'):
            fname_prefix = in_fname.rpartition('.')[0]
            print "reading: {0}".format(in_fname)
            (data, attr_names, instance_names) = text_mtx_rw.read_mtx_info(
                os.path.join(in_dirpath, in_fname))
            if combined_data is not None:
                combined_data = np.vstack((combined_data, data))
            else:
                combined_data = data
            if combined_attr_names:
                assert attr_names == combined_attr_names
            else:
                combined_attr_names = attr_names
            combined_inst_names.extend(('{0}_{1}'.format(name, fname_prefix)
                for name in instance_names))
            
    if os.path.exists(out_filepath):
        sys.stderr.write('ERROR: "{0}" already exists'.format(out_filepath))
    
    text_mtx_rw.write_mtx_info(out_filepath, combined_data, 
        combined_attr_names, combined_inst_names)
    print "wrote {0}".format(out_filepath)