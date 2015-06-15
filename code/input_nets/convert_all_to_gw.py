#! /usr/bin/env python
# usage: python convert_to_gw <folder> <start_year> <end_year>
# converts all .undirected files from the specified folder to .gw years start_year to end_year


import os
import sys


NET_PATH_TRADE_ALL=sys.argv[1]
START_YEAR=int(sys.argv[2])
END_YEAR=int(sys.argv[3])


for net_nr in range(START_YEAR,END_YEAR):
  input_file = NET_PATH_TRADE_ALL + "/" + str(net_nr) + ".undirected"
  output_file = NET_PATH_TRADE_ALL + "/" + str(net_nr) + ".gw"
  command = "cut -f1,2 " + input_file + " | ../list2leda > " + output_file
  print "Running command: ", command
  os.system(command)


