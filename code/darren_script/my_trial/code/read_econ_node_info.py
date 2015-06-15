# -*- coding: utf-8 -*-
"""
Reads economic attributes from per-country files.
"""

import collections
import os
import re

CountryAttribute = collections.namedtuple(
    'CountryAttribute', ['country_name', 'year', 'attr_name', 'values'])
def get_attrs_for_country_file(file_path, country_name):
    attrs = dict()
    in_file = open(file_path, 'rt')
    for line in in_file:
        fields = line.strip().split('\t')
        year = fields[0].partition(' ')[0]
        value = fields[1]
        attr_name = re.sub('\W', '_', fields[2].strip())
        attr_key = (year, attr_name)
        cur_attr_vals = attrs.get(attr_key, [])
        cur_attr_vals.append(value)
        attrs[attr_key] = cur_attr_vals
    in_file.close()
    return [CountryAttribute(country_name, key[0], key[1], attrs[key]) for key in attrs.keys()]

def read_all_attrs_from_dir(dir_path):
    all_attrs = []
    for fname in os.listdir(dir_path):
        print "reading: {0}".format(fname)
        fpath = os.path.join(dir_path, fname)
        if os.path.isfile(fpath):
            attrs = get_attrs_for_country_file(fpath, fname)
            all_attrs = all_attrs + attrs
    return all_attrs