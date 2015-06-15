# -*- coding: utf-8 -*-
"""
Reformats information from per-country economic-attribute data files into a 
single CSV with country_year instances.
"""

from collections import defaultdict
import numpy as np
import os
import sys

from read_econ_node_info import read_all_attrs_from_dir
import econ_node_info_to_csv

start_year = 1980;
end_year = 2010;

# if we required these, we would eliminate almost all the country-year pairs
#excluded_attributes = set(['Deposit_Rate', 'Discount_Rate', 'Government_Bonds',
#                           'Lending_Rate', 'Money_Market_Rate', 'Treasury_Bills', 'LE'])
# with these exclusions, we're left with only the most common attributes
#excluded_attributes.update(set(['BCA', 'GGR_NGDP', 'GGXWDG_NGDP', 'LE', 'LUR', 
#    'PCPIPCH']))
#excluded_attributes = set(['LE', 'BCA'])
excluded_attributes = set()

if __name__ == '__main__':
    # in_dir_path should not contain any files other than node-attribute files
    if len(sys.argv) != 3:
        print "usage: econ_node_info_to_year_aggregated_csv in_dir_path out_dir_path"
    
    in_dir_path = sys.argv[1]
    out_dir_path = sys.argv[2]
    
    print "reading node attributes from all files in {0}".format(in_dir_path)
    all_attrs = read_all_attrs_from_dir(in_dir_path)
    
    info_file_path = os.path.join(out_dir_path, 
        '{0}to{1}_complete-countries.info'.format(start_year, end_year))
    info_file = open(info_file_path, 'wt')
    
    info_file.write("including years from {0} to {1}, inclusive\n".format(
        start_year, end_year))
    info_file.write("excluding attributes: {0}\n".format(sorted(excluded_attributes)))
    
    all_attrs = [attr for attr in all_attrs if 
        (int(attr.year) >= start_year and int(attr.year) <= end_year)]

    all_attr_names = frozenset((attr.attr_name for attr in all_attrs 
        if attr.attr_name not in excluded_attributes))
    sorted_all_attr_names = sorted(all_attr_names)
    info_file.write("included attributes: {0}\n".format(sorted_all_attr_names))
    
    attr_missing_counts = defaultdict(int)
    ctry_incl_counts = defaultdict(int)
    ctry_skip_counts = defaultdict(int)
    
    out_path = os.path.join(out_dir_path, 
        '{0}to{1}_complete-countries.csv'.format(start_year, end_year))
    if os.path.exists(out_path):
        sys.stderr.write("ERROR: '{0}' already exists\n".format(out_path))
        sys.exit()
    outfile = open(out_path, 'wt')
    outfile.write('country_year,' + ','.join(sorted_all_attr_names))
    attrs_by_ctry = econ_node_info_to_csv.group_attrs_by_country(all_attrs)
    for ctry in sorted(attrs_by_ctry.keys()):
        ctry_attrs = econ_node_info_to_csv.group_attrs_by_year(attrs_by_ctry[ctry])
        for year in sorted(ctry_attrs.keys()):
            ctry_year_attrs = ctry_attrs[year]
            ctry_year_attr_names = frozenset((attr.attr_name for attr in ctry_year_attrs))
            missing_attr_names = all_attr_names - ctry_year_attr_names
            if missing_attr_names:
                for attr_name in missing_attr_names:
                    attr_missing_counts[attr_name] += 1
                ctry_skip_counts[ctry] += 1
            else:
                ctry_incl_counts[ctry] += 1
                ctry_year_attrs = [attr for attr in ctry_year_attrs 
                    if attr.attr_name not in excluded_attributes]
                ctry_year_attrs.sort(key=lambda x: x.attr_name)
                assert [attr.attr_name for attr in ctry_year_attrs] == sorted_all_attr_names
                attr_idx = -1
                outfile.write('\n' + ctry + '_' + year)
                for cur_attr in ctry_year_attrs:
                    attr_idx += 1
                    assert cur_attr.attr_name == sorted_all_attr_names[attr_idx]
                    assert cur_attr.country_name == ctry
                    outfile.write(',' + 
                        str(np.median([float(val) for val in cur_attr.values])))
            
    info_file.write("\nnumber of times each attribute was missing for a (country,year) pair:\n")
    for attr_name in sorted_all_attr_names:
        info_file.write("{0}:{1}\n".format(attr_name, attr_missing_counts[attr_name]))

    info_file.write("\ncountry coverage:\n")
    for ctry in sorted(attrs_by_ctry.keys()):
        info_file.write("{0}: skip count {1}, include count {2}\n".format(ctry, 
            ctry_skip_counts[ctry], ctry_incl_counts[ctry]))
    
    print "wrote '{0}' and associated info file".format(out_path)
