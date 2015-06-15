# -*- coding: utf-8 -*-

#import collections
import numpy as np
#import re
import os
import sys

from read_econ_node_info import CountryAttribute, read_all_attrs_from_dir

#class CountryMeasurement(object):
#    def __init__(self, country, year, meas_name):
#        self.country = country
#        self.year = year
#        self.meas_name = meas_name
#        self.meas_values = []
#        
#    def add_measurement(self, meas_value):
#        self.meas_values.add(meas_value)
#        
#    def __eq__(self, other):
#        return ( (isinstance(other, CountryMeasurement)) and
#            (self.country == other.country) and
#            (self.year == other.year) and 
#            (self.meas_name == other.meas_name) )
#            
#    def __hash__(self):
#        return (str(self.country) + str(self.year) + str(self.meas_name)).hash()

def group_attrs_by_year(all_attrs):
    attrs_by_year = dict()
    for attr in all_attrs:
        cur_year = attr.year
        yr_attr_list = attrs_by_year.get(cur_year, [])
        yr_attr_list.append(attr)
        attrs_by_year[cur_year] = yr_attr_list
    return attrs_by_year
    
def group_attrs_by_country(all_attrs):
    attrs_by_ctry = dict()
    for attr in all_attrs:
        cur_ctry = attr.country_name
        ctry_attr_list = attrs_by_ctry.get(cur_ctry, [])
        ctry_attr_list.append(attr)
        attrs_by_ctry[cur_ctry] = ctry_attr_list
    return attrs_by_ctry

if __name__ == '__main__':
    # in_dir_path should not contain any files other than node-attribute files
    if len(sys.argv) != 4:
        sys.exit('usage: econ_node_info_to_csv.py in_dir_path per_year_out_dir_path per_node_out_dir_path')
#    
    in_dir_path = sys.argv[1]
    per_year_out_dir_path = sys.argv[2]
    per_node_out_dir_path = sys.argv[3]
    
    print "reading node attributes from all files in {0}".format(in_dir_path)
    
    all_attrs = read_all_attrs_from_dir(in_dir_path)
    
#    all_attrs = []
#    for fname in os.listdir(in_dir_path):
#        print "reading: {0}".format(fname)
#        fpath = os.path.join(in_dir_path, fname)
#        if os.path.isfile(fpath):
#            attrs = get_attrs_for_country_file(fpath, fname)
#            all_attrs = all_attrs + attrs
    
    attrs_by_year = group_attrs_by_year(all_attrs)
#    attrs_by_year = dict()
#    for attr in all_attrs:
#        cur_year = attr.year
#        yr_attr_list = attrs_by_year.get(cur_year, [])
#        yr_attr_list.append(attr)
#        attrs_by_year[cur_year] = yr_attr_list
        
    for year in attrs_by_year.keys():
        print "writing: {0}".format(year)
        
        # write a country-vs-attribute CSV, with a placeholder string 
        # for missing values
        cur_attrs = attrs_by_year[year]
        all_attr_names = list(set([attr.attr_name for attr in cur_attrs]))
        all_attr_names.sort()
        cur_attrs.sort(key=(lambda x: x.attr_name))        
        cur_attrs.sort(key=(lambda x: x.country_name)) 
        incomplete_attrs = set()
        incomplete_countries = set()
        outfile_all = open(per_year_out_dir_path + os.sep + year + '_all.csv', 'wt')
        outfile_all.write('country,' + ','.join(all_attr_names))
        cur_country = None
        for attr in cur_attrs:
            if attr.country_name != cur_country:
                if cur_country:
                    n_rem_attrs = (len(all_attr_names) - cur_attr_idx)
                    outfile_all.write(',missing' * n_rem_attrs)
                    incomplete_attrs.update(all_attr_names[-n_rem_attrs:])
                    if n_rem_attrs > 0:
                        incomplete_countries.add(cur_country)
                outfile_all.write('\n' + attr.country_name)
                cur_attr_idx = 0
                cur_country = attr.country_name
            next_avail_attr_name = attr.attr_name
            while (all_attr_names[cur_attr_idx] != next_avail_attr_name):
                incomplete_attrs.add(all_attr_names[cur_attr_idx])
                incomplete_countries.add(cur_country)
                outfile_all.write(',missing')
                cur_attr_idx = cur_attr_idx + 1
            
            outfile_all.write(',' + str(np.median([float(val) for val in attr.values])))
            cur_attr_idx = cur_attr_idx + 1
        outfile_all.close()
        
        # write a country-vs-attribute CSV, eliminating countries
        # with missing attributes
        cur_attrs_complete = [attr for attr in cur_attrs if attr.country_name
            not in incomplete_countries]
        cur_country = None
        outfile_complete_ctry = open(per_year_out_dir_path + os.sep + year + 
            '_complete-countries.csv', 'wt')
        outfile_complete_ctry.write('country,' + ','.join(all_attr_names))
        for attr in cur_attrs_complete:
            if attr.country_name != cur_country:
                outfile_complete_ctry.write('\n' + attr.country_name)
                cur_country = attr.country_name
            outfile_complete_ctry.write(',' + 
                str(np.median([float(val) for val in attr.values])))
        outfile_complete_ctry.close()
        
        # write a country-vs-attribute CSV, eliminating attributes with 
        # missing values
        full_avail_attr_names = [attr_name for attr_name in all_attr_names 
            if attr_name not in incomplete_attrs]
        cur_attrs_complete = [attr for attr in cur_attrs if attr.attr_name
            not in incomplete_attrs]
        cur_country = None
        outfile_complete_attrs = open(per_year_out_dir_path + os.sep + year + 
            '_complete-attrs.csv', 'wt')
        outfile_complete_attrs.write('country,' + ','.join(full_avail_attr_names))
        for attr in cur_attrs_complete:
            if attr.country_name != cur_country:
                outfile_complete_attrs.write('\n' + attr.country_name)
                cur_country = attr.country_name
            outfile_complete_attrs.write(',' + 
                str(np.median([float(val) for val in attr.values])))
        outfile_complete_attrs.close()
    
    attrs_by_ctry = group_attrs_by_country(all_attrs)
#    attrs_by_ctry = dict()
#    for attr in all_attrs:
#        cur_ctry = attr.country_name
#        ctry_attr_list = attrs_by_ctry.get(cur_ctry, [])
#        ctry_attr_list.append(attr)
#        attrs_by_ctry[cur_ctry] = ctry_attr_list
        
    for ctry in attrs_by_ctry.keys():
        # write a year-vs-attribute CSV for the given country
        cur_attrs = attrs_by_ctry[ctry]
        cur_attrs.sort(key = lambda x: x.attr_name)
        cur_attrs.sort(key = lambda x: x.year)
        all_attr_names = list(set([attr.attr_name for attr in cur_attrs]))
        all_attr_names.sort()
        all_years = list(set([int(attr.year) for attr in cur_attrs]))
#        all_years.sort()
#        min_year = all_years[0]
        min_year = np.min(all_years)
#        max_year = np.max(all_years)
        print "writing: {0}".format(ctry)
        ctryfile_all = open(per_node_out_dir_path + os.sep + ctry + '.csv', 'wt')
        ctryfile_all.write('year,' + ','.join(all_attr_names))
        ctryfile_all.write('\n' + str(min_year))
        cur_year = min_year
        cur_attr_idx = 0
        for attr in cur_attrs:
            if int(attr.year) != cur_year:
                n_rem_attrs = (len(all_attr_names) - cur_attr_idx)
                ctryfile_all.write(',nan' * n_rem_attrs)
                ctryfile_all.write('\n' + attr.year)
                cur_attr_idx = 0
                cur_year = cur_year + 1
            next_avail_attr_name = attr.attr_name
            while (all_attr_names[cur_attr_idx] != next_avail_attr_name):
                ctryfile_all.write(',nan')
                cur_attr_idx = cur_attr_idx + 1
            ctryfile_all.write(',' + str(np.median([float(val) for val in attr.values])))
            cur_attr_idx = cur_attr_idx + 1
        n_rem_attrs = (len(all_attr_names) - cur_attr_idx)
        ctryfile_all.write(',nan' * n_rem_attrs + '\n')
        ctryfile_all.close()