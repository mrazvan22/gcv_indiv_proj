#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from scipy.spatial.distance import *
#import scipy.cluster.hierarchy as sch
import numpy as np
#from scipy.cluster.hierarchy import linkage, dendrogram
import scipy.stats
import os

import sys
#from plot_pearsons_heatmap_hclust import *


def calc_all_sigs(NET_NAME):
    source = "%s/%s/models/%s/%s-%s-%d/%s.gw" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1, NET_NAME)

    sigs = "python eval_calc_other_sigs.py %s" % source

    os.system(sigs)

    gdv_dest = "%s/%s/models/%s/%s-%s-%d/%s_gdv" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1, NET_NAME)

    gdv = "./ncount %s %s" % (source, gdv_dest)

    os.system(gdv)
    # only keep the gdv.gr_freq and gdv.ndump2
    #print ("rm %s; rm %s.cl_*" % (gdv_dest, gdv_dest))
    os.system("rm %s; rm %s.cl_*" % (gdv_dest, gdv_dest))

    pears_gdv_source = "%s.ndump2" % gdv_dest
    pears_gdv_dest = "%s.pears" % gdv_dest
    pears_gdv_cmd = "./pears_coeff_gdv %s %s test_matrix 0" % ( pears_gdv_source, pears_gdv_dest)
    print "Running: %s" % pears_gdv_cmd
    os.system(pears_gdv_cmd)


    gcv_dest = "%s/%s/models/%s/%s-%s-%d/%s_gcv" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1, NET_NAME)
    gcv = "./e_gdv %s %s %d 0" % (source, gcv_dest, NR_THREADS)
    os.system(gcv)

    pears_gcv_source = "%s.ndump2" % gcv_dest
    pears_gcv_dest = "%s.pears" % gcv_dest
    pears_gcv_cmd = "./pears_coeff %s %s test_matrix 0" % ( pears_gcv_source, pears_gcv_dest)
    print "Running: %s" % pears_gcv_cmd
    os.system(pears_gcv_cmd)




if (len(sys.argv) != 4):
  print 'Erorr parsing parameters. Usage: python eval_all_rnd_netse_sigs.py <folder> <net_type> <nr_nets>'
  exit()


netType = int(sys.argv[2])

FOLDER = sys.argv[1]

NR_RAND_NETS = int(sys.argv[3])

assert(netType == 2)

NETWORKS = ["hsa_metabolic_network", "human_ppi", "trade_2010_thresholded"]

TYPES = ["er", "er_dd", "geo", "sf", "sticky"]

#NR_RAND_NETS = 1
#NR_RAND_NETS = 30
RAND_NET_TYPES = len(TYPES)
NR_THREADS = 2

i = 0
NET_NAME = "graph"
for randType1 in range(RAND_NET_TYPES):
  for randNetNr1 in range(1, NR_RAND_NETS+1):
    source = "%s/%s/models/%s/%s-%s-%d/%s.gw" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1, NET_NAME)
    print source

    # calculate sinatrues for the original network
    calc_all_sigs(NET_NAME)
    os.system("python eval_rewire.py %s" % source)


    # generates 10 networks for 10 different rewiring probabilities
    for rew in range(10):
      new_name = NET_NAME + "_rew_" + str(rew)
      calc_all_sigs(new_name)

    # generates 10 networks each having a different edge completeness
    for compl in range(1,11):
      new_name = NET_NAME + "_compl_" + str(compl)
      calc_all_sigs(new_name)

    sample_folder = "%s/%s/models/%s/%s-%s-%d" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1)
    sample_network = "%s_rew_4.gw" % NET_NAME
    sample_base_name = NET_NAME

    # generated sigantures for 10 networks where only x% of the nodes have been used for calculating them
    node_sampling_cmd = "python eval_calc_sigs_sampling.py %s %s %s" % (sample_folder, sample_network, sample_base_name)
    os.system(node_sampling_cmd)




