#! /usr/bin/env python
# usage: python ppy_lifecycle_cca <part1/part2/all> <annotations_folder> <THREADS> <net_nr> <GEN_FOLDER>
# the only optional argument "full" is used for calculating the gw vectors as well

import os
import sys
import numpy as np


ANNOTATIONS_FOLDER = sys.argv[2]
GEN_FOLDER=sys.argv[5]
THREADS=sys.argv[3]
TYPE=sys.argv[1]
NET_NR = int(sys.argv[4])

HUMAN_NETS_FOLDER='input_nets/human_ppi_all/'

YEAST_NETS_FOLDER='input_nets/yeast_ppi_all/'

HUMAN_NETS = [
"human_HI_2012_preliminary.gw",
"human_i2d_full.gw",
"human_i2d_hc.gw",
"human_ppi_56k.gw",
"biogrid-ppi/biogrid_human_ppi_noUBC_full.gw",
"biogrid-ppi/biogrid_human_ppi_hc.gw"
]

HUMAN_INDICATORS = [
"human_ppi_annotation_biogrid_final.txt",
"human_ppi_annotation_id2_final.txt",
"human_ppi_annotation_id2_final.txt",
"human_ppi_annotation_biogrid_final.txt",
"human_ppi_annotation_biogrid_final.txt",
"human_ppi_annotation_biogrid_final.txt"
]

YEAST_NETS=[
"yeast_apms_collins.gw",
"yeast_biogrid_genetic.gw",
"yeast_lc.gw",
"yeast_y2h_union_yu_ito_uetz.gw",
"biogrid-ppi/biogrid_yeast_ppi_noYLL039C_full.gw",
"biogrid-ppi/biogrid_yeast_ppi_hc.gw"
]

YEAST_INDICATORS= [
"yeast_functions_boone_final.txt",
"yeast_functions_merin_final.txt"
]

# expand yeast experiments to 6x2
YEAST_NETS *= 2
YEAST_INDICATORS = [YEAST_INDICATORS[0]] * 6 + [YEAST_INDICATORS[1]] * 6

# expand to the full file paths
HUMAN_NETS = [ HUMAN_NETS_FOLDER + net for net in HUMAN_NETS]
YEAST_NETS = [ YEAST_NETS_FOLDER + net for net in YEAST_NETS]


HUMAN_INDICATORS = [ANNOTATIONS_FOLDER + f for f in HUMAN_INDICATORS]
YEAST_INDICATORS = [ANNOTATIONS_FOLDER + f for f in YEAST_INDICATORS]

# merge the nets and annotations
NETS = HUMAN_NETS + YEAST_NETS
INDICATORS = HUMAN_INDICATORS +YEAST_INDICATORS

print "NETS:",np.array(NETS),"\n\n"
print "INDICATORS:",np.array(INDICATORS),"\n\n"

GW_SOURCE= NETS[NET_NR]
INDICATOR_SOURCE= INDICATORS[NET_NR]
NET= GW_SOURCE.split("/")[-1].split(".")[0]

FOLDER = str(NET_NR) + "-" + NET
#if the network is a yeast network, then also append the name of the indicator used to the FOLDER
if(NET_NR > 5):
  FOLDER += "_" + INDICATOR_SOURCE.split("_")[4]

print "NET:",NET

assert (TYPE == "part1" or TYPE == "part2" or TYPE == "all")

cmd = "make NET=" + NET + " FOLDER=" + FOLDER + " GW_SOURCE=" + GW_SOURCE + " INDICATOR_SOURCE=" + INDICATOR_SOURCE + " THREADS=" +THREADS + " canon_lc_ppi_" + TYPE
print cmd
os.system(cmd)


