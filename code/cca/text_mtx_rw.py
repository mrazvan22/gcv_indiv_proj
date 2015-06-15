# -*- coding: utf-8 -*-

import numpy as np

def read_mtx_info(filename, sep=',', sprdsht_fmt=True, convert_to_float=True):
    in_file = open(filename, 'rt')
    attr_names = in_file.readline().strip().split(sep)
    if sprdsht_fmt:
        attr_names = attr_names[1:]
    data = []
    instance_names = []
    cur_line = in_file.readline()
    while cur_line != '':
        cur_line = cur_line.strip()
        cur_entries = cur_line.split(sep)
        if cur_line.endswith(sep) and (cur_entries[-1] == ''):
            cur_entries = cur_entries[0:-1]
        instance_names.append(cur_entries[0])
        if convert_to_float:
            data.append([float(entry) if entry else np.nan for entry in cur_entries[1:]])
        else:
            data.append(cur_entries[1:])
        cur_line = in_file.readline()
    colsizes = np.array([len(col) for col in data])
    max_colsize = np.max(colsizes)
    if np.any(colsizes != max_colsize):
        print "warning: irregular column lengths, padding ends with Nones"
        for row in data:
            row.extend([None] * (max_colsize - len(row)))
    data = np.array(data)
    in_file.close()
    return (data, attr_names, instance_names)
    
def write_mtx_info(filename, data, attr_names, instance_names):
    if (len(instance_names) != data.shape[0]):
        raise ValueError("number of instances must match number of matrix rows")
    if (len(attr_names) != data.shape[1]):
        raise ValueError("number of attributes must match number of matrix columns")
    out_file = open(filename, 'wt')
    out_file.write('ID,' + ','.join(attr_names) + '\n')
    for i in range(len(instance_names)):
#        out_file.write(instance_names[i] + ',' + ','.join(map(str, data[i,:])) + '\n')
        elt = instance_names[i]
        if elt.lower() == 'nan':
            elt = ''
        out_file.write(elt + ',' + ','.join(map(repr, data[i,:])) + '\n')
    out_file.close()