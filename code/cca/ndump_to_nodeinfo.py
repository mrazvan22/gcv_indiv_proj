# -*- coding: utf-8 -*-
"""
Reformats graphlet signature ndump2 files as CSV files.
"""

import logging
import re
import sys

logger = logging.getLogger(name="ndump_to_nodeinfo")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('usage: ndump_to_nodeinfo.py inFile outFile')

    (in_filename, out_filename) = sys.argv[1:3]

    logging.basicConfig(level=logging.DEBUG, filename=(out_filename + '.log'))

    logger.info("reading ndump2 file: {0}".format(in_filename))
    in_file = open(in_filename, 'rt')

    cur_line = in_file.readline()
    cur_entries = cur_line.split()
    n_orbits = len(cur_entries) - 1

    out_file = open(out_filename, 'wt')
    out_file.write('ID,' + ','.join(
        ['sig_{0}'.format(num+1) for num in range(n_orbits)]) + '\n')
    out_file.write(','.join(cur_entries) + '\n')

    cur_line = in_file.readline()
    while cur_line != '':
        out_file.write(re.sub('\s+', ',', cur_line) + '\n')
        cur_line = in_file.readline()

    in_file.close()
    out_file.close()
    logger.info("wrote csv: {0}".format(out_filename))
