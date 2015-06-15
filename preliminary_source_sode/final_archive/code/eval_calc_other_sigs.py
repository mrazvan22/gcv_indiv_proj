#!/usr/bin/env python

import sys
import os
import networkx as nx
import numpy as np

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

if(len(sys.argv) != 2):
  print "Usage: python eval_calc_other_sigs.py <input_net.gw> "

INPUT_NET = sys.argv[1]
OUTPUT_FILE = INPUT_NET.split(".")[0] + ".sigs"


graph = readLeda(INPUT_NET)

degrees  = graph.degree() # dictionary node:degree
#out_degrees = graph.out_degree()

print degrees.items()[:10]
#print out_degrees.items()[:10]

values = sorted(set(degrees.values()))

print "values:", values[:10]

deg_dist = [degrees.values().count(x) for x in range(1,31)]
print deg_dist

TARGET_LEN = 60

if(len(deg_dist) > TARGET_LEN):
  deg_dist = deg_dist[:TARGET_LEN]
else:
  deg_dist = deg_dist + ([0] * (TARGET_LEN - len(deg_dist)))

assert(len(deg_dist) == TARGET_LEN)

clust_coeff = nx.average_clustering(graph)

sg = nx.connected_component_subgraphs(graph)

lengths = [len(s) for s in sg]
max_index = lengths.index(max(lengths))

print "connected_comp",lengths
diameter = nx.diameter(sg[max_index])


laplacian = nx.adjacency_matrix(graph)

(xdim, ydim) = laplacian.shape

assert(xdim == ydim)

laplacian = laplacian.tolist()
#print laplacian[2,:]
#print laplacian[2,2]

for i in range(xdim):
  #print -sum(laplacian[i])
  laplacian[i][i] = -sum(laplacian[i])

print laplacian[0]

(eigs, vectors)  = np.linalg.eig(laplacian)
eigs.sort()
spectral_dist = [abs(x) for x in eigs][:TARGET_LEN]

print "spectral:", spectral_dist


print "Writing to %s" % OUTPUT_FILE
with open(OUTPUT_FILE, "w") as f:
  f.write("deg_dist:\n")
  for deg in deg_dist:
    f.write("%d " % deg)

  f.write("\nclust_coeff:\n%f\ndiameter:\n%d\n" % (clust_coeff, diameter))

  f.write("spectral_dist:\n")
  for eig in spectral_dist:
    f.write("%.6f " % eig)
