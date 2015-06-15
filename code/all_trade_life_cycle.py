#! /usr/bin/env python
# usage: python all_trade_life_cycle {full}/optional <net_name> <input_nets_folder> <start_year> <end_year> <gen_folder> <norm_type>
# the only optional argument "full" is used for calculating the gw vectors as well

import os
import sys


GEN_FOLDER=sys.argv[7]
NET_NAME = sys.argv[2]
NET_PATH_TRADE_ALL=GEN_FOLDER + '/' + NET_NAME
THREADS=int(sys.argv[6])
INPUT_FOLDER=sys.argv[3]
START_YEAR=int(sys.argv[4])
END_YEAR=int(sys.argv[5])
NORM_TYPE=int(sys.argv[8])


initial_filehandling_cmd="cd " + GEN_FOLDER + " && mkdir " + NET_NAME + " && cd .. && cp " + INPUT_FOLDER +  "/*.gw " + NET_PATH_TRADE_ALL
os.system(initial_filehandling_cmd)


if((sys.argv[1]) == "part1"):
  for net_nr in range(START_YEAR,END_YEAR):
    basefile= NET_PATH_TRADE_ALL + "/" + str(net_nr)
    egdv = "./e_gdv " + basefile + ".gw " + basefile + " " + str(THREADS) + " " + str(NORM_TYPE)
    print "Running: %s" % egdv
    os.system(egdv)


if((sys.argv[1]) == "part2"):
  for net_nr in range(START_YEAR,END_YEAR):
    basefile= NET_PATH_TRADE_ALL + "/" + str(net_nr)

    avg = "./avg_gdv " + basefile + ".ndump2 > " + basefile + ".avg "
    os.system(avg)

    pears_file =      NET_PATH_TRADE_ALL +"/pearsons_"            + str(net_nr) + ".data "
    pears_file_norm = NET_PATH_TRADE_ALL +"/pearsons_normalized_" + str(net_nr) + ".data "
    pears = "./pears_coeff " + basefile + ".ndump2 " + pears_file + pears_file_norm + str(NORM_TYPE)
    os.system(pears)

    pears_hclust_file = NET_PATH_TRADE_ALL + "/pearsons_hclust_" + str(net_nr) + ".data "
    hclust = "python final_results/h_clust.py " + pears_file_norm + pears_hclust_file + " | gnuplot"
    os.system(hclust)

    norm_pears_heatmap_cmd = "python final_results/gen_normal_pears_heatmap.py " + pears_file + " | gnuplot"
    os.system(norm_pears_heatmap_cmd)

