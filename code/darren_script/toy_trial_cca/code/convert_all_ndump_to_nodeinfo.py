# -*- coding: utf-8 -*-
"""
Converts all ndump2 files in one directory into a set of CSVs (one per ndump2
file)
"""

import logging
import os
import subprocess
import sys

logger = logging.getLogger("convert_all_ndump_to_nodeinfo")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: convert_all_ndump_to_nodeinfo.py in_dir out_dir')
    
    logging.basicConfig(level=logging.DEBUG)    
    
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    
    print "current working directory: ", os.getcwd()
    
    if not os.path.isdir(in_dir):
        sys.stderr.write(
            "input directory {0} must be a directory\n".format(in_dir))
        sys.exit(1)
    
    if os.path.exists(out_dir):
        sys.stderr.write(
            "output directory {0} already exists\n".format(out_dir))
        sys.exit(1)
    
    for (dirpath, dirnames, filenames) in os.walk(in_dir):
        cur_out_dir = os.path.join(out_dir, os.path.relpath(dirpath, start=in_dir))
        if not os.path.exists(cur_out_dir):
            os.mkdir(cur_out_dir)
        for filename in filenames:
            fptn = filename.rpartition('.')
            file_ext = fptn[2]
            data_name = fptn[0] if fptn[0] else fptn[2]
            if file_ext == "ndump2":
                arg1 = (dirpath + os.sep + filename)
                arg2 = (cur_out_dir + os.sep + data_name + ".csv")
                subp_args = ["python", "ndump_to_nodeinfo.py", arg1, arg2]
                logger.info("running: " + " ".join(subp_args))
                subprocess.call(subp_args)
            else:
                logger.info("skipped {0} (no ndump2 extension)".format(
                    filename))