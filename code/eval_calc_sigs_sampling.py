#!/usr/bin/env python

import sys
import os
import networkx as nx
import numpy as np
import random

# Read the network
def readLeda(gwFile):
	network = nx.Graph()

	fRead = open(gwFile, 'r')

	mode = 0
	nodeIndexes = {}
	nodeCount = 1
	for line in fRead:
		if (mode == 0 or mode == 1) and line.startswith('|'):
			nodeName = line.rstrip().strip('|').lstrip('{').rstrip('}')
			network.add_node(nodeName)
			nodeIndexes[nodeCount] = nodeName
			nodeCount += 1

			if mode == 0:
				mode = 1
		elif mode == 1 and not line.startswith('|'):
			mode = 2
		elif mode == 2 and line.strip().endswith('|'):
			splitted = line.strip().split(' ')
			network.add_edge(nodeIndexes[int(splitted[0])], nodeIndexes[int(splitted[1])])


	fRead.close()


	return network


def write_to_file(out_file, deg_dist, clust_coeff, diameter, spectral_dist):
  print "Writing to %s" % out_file
  with open(out_file, "w") as f:
    f.write("deg_dist:\n")
    for deg in deg_dist:
      f.write("%d " % deg)

    f.write("\nclust_coeff:\n%f\ndiameter:\n%d\n" % (clust_coeff, diameter))

    f.write("spectral_dist:\n")
    for eig in spectral_dist:
      f.write("%.6f " % eig)

def write_partial_ndump(out_file, lines, target_nodes):
  with open(out_file, "w") as f:
    for line in lines[:target_nodes]:
      f.write(line)


def write_graph_to_file(out_file, subgraph):
  with open(out_file, "w") as f:
    for edge in subgraph.edges():
      f.write('{0}\t{1}\n'.format(edge[0], edge[1]))



if(len(sys.argv) != 4):
  print "Usage: python eval_calc_sigs_sampling.py <folder> <input_net.gw> <base_name_for_outputs> "

FOLDER = sys.argv[1]
INPUT_NET = sys.argv[2]
BASE_NAME = sys.argv[3]

# make sure you use the 40% rewired network
assert ("_rew_4" in INPUT_NET)

graph = readLeda(FOLDER + "/" + INPUT_NET)
NR_NODES = len(graph.nodes())
NR_EDGES = len(graph.edges())

clust_coeffs_all = nx.clustering(graph).values()
random.shuffle(clust_coeffs_all)

TARGET_LEN = 60
all_degrees  = graph.degree().values() # dictionary node:degree
random.shuffle(all_degrees)

for sample_nr in range(1,11):
  target_nodes = (NR_NODES * sample_nr) / 10

  degrees = [x for x in all_degrees]
  degrees = degrees[:target_nodes]

  #print degrees.items()[:10]
  #values = sorted(set(degrees))
  #print "values:", values[:10]
  deg_dist = [degrees.count(x) for x in range(1,TARGET_LEN+1)]
  #print deg_dist


  #if(len(deg_dist) > TARGET_LEN):
  #  deg_dist = deg_dist[:TARGET_LEN]
  #else:
  #  deg_dist = deg_dist + ([0] * (TARGET_LEN - len(deg_dist)))

  assert(len(deg_dist) == TARGET_LEN)

  clust_coeff = float(sum(clust_coeffs_all[:target_nodes]))/target_nodes

  eccentricities = nx.eccentricity(graph).values()
  diameter = max(eccentricities[:target_nodes])

  laplacian = nx.adjacency_matrix(graph)

  (xdim, ydim) = laplacian.shape

  assert(xdim == ydim)

  laplacian = laplacian.tolist()

  for i in range(xdim):
    laplacian[i][i] = -sum(laplacian[i])

  print "laplacian[0]", laplacian[0]

  laplacian = np.array(laplacian)[0:target_nodes,0:target_nodes]

  (eigs, vectors)  = np.linalg.eig(laplacian)
  eigs.sort()
  spectral_dist = [abs(x) for x in eigs]
  if(len(spectral_dist) > TARGET_LEN):
    spectral_dist = spectral_dist[:TARGET_LEN]
  else:
    spectral_dist += [0] * (TARGET_LEN - len(spectral_dist))

  assert(len(spectral_dist) == TARGET_LEN)

  print "spectral:", spectral_dist

  out_file = FOLDER + "/" + BASE_NAME + "_sampl_" + str(sample_nr) + ".sigs"
  write_to_file(out_file, deg_dist, clust_coeff, diameter, spectral_dist)

# now compute the node_sampled gcv and gdv ndumps and pears matrices

gdv_ndump_file = FOLDER + "/" + INPUT_NET.split(".")[0] + "_gdv.ndump2"
gcv_ndump_file = FOLDER + "/" + INPUT_NET.split(".")[0] + "_gcv.ndump2"

gdv_lines = []
gcv_lines = []

with open(gdv_ndump_file) as f:
  gdv_lines = f.readlines()
with open(gcv_ndump_file) as f:
  gcv_lines = f.readlines()

random.shuffle(gdv_lines)
random.shuffle(gcv_lines)

nodes = graph.nodes()
random.shuffle(nodes)

for sample_nr in range(1,11):
  target_nodes = (NR_NODES * sample_nr) / 10
  # generate cut ndump files
  gdv_out_file = FOLDER + "/" + BASE_NAME + "_sampl_" + str(sample_nr) + "_gdv.ndump"
  write_partial_ndump(gdv_out_file, gdv_lines, target_nodes)

  gcv_out_file = FOLDER + "/" + BASE_NAME + "_sampl_" + str(sample_nr) + "_gcv.ndump"
  write_partial_ndump(gcv_out_file, gcv_lines, target_nodes)

  # generate pearson's correlation matrices
  pears_gdv_dest = "%s.pears" % (gdv_out_file.split(".")[0])
  pears_gdv_cmd = "./pears_coeff_gdv %s %s test_matrix 0" % ( gdv_out_file, pears_gdv_dest)
  print "Running: %s" % pears_gdv_cmd
  os.system(pears_gdv_cmd)

  pears_gcv_dest = "%s.pears" % (gcv_out_file.split(".")[0])
  pears_gcv_cmd = "./pears_coeff %s %s test_matrix 0" % ( gcv_out_file, pears_gcv_dest)
  print "Running: %s" % pears_gcv_cmd
  os.system(pears_gcv_cmd)

  subgraph = graph.subgraph(nodes[:target_nodes])

  subgraph_out_base = FOLDER + "/" + BASE_NAME + "_sampl_" + str(sample_nr)
  write_graph_to_file(subgraph_out_base + ".txt", subgraph)


  os.system("./list2leda %s > %s" % (subgraph_out_base + ".txt",  subgraph_out_base + ".gw"))

  os.system("./ncount %s %s" % (subgraph_out_base + ".gw", subgraph_out_base))

  os.system("rm %s; rm %s.cl_*; rm %s.ndump2" % (subgraph_out_base, subgraph_out_base, subgraph_out_base))

  os.system("mv %s.gr_freq %s_gdv.gr_freq" % (subgraph_out_base, subgraph_out_base))
