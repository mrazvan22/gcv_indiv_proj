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


def write_output(out_file, new_edges):
  with open(out_file, "w") as f:
    for edge in new_edges:
      f.write('{0}\t{1}\n'.format(edge[0], edge[1]))

if(len(sys.argv) != 2):
  print "Usage: python eval_rewire.py <input_net.gw> "

INPUT_NET = sys.argv[1]
OUT_BASE = INPUT_NET.split(".")[0]

graph = readLeda(INPUT_NET)

NR_NODES_ORIG = len(graph.nodes())
all_nodes = graph.nodes()

print graph.edges()
out_txt = OUT_BASE + "_rew_" + str(0) + ".txt"
write_output(out_txt, graph.edges())

out_gw = OUT_BASE + "_rew_" + str(0) + ".gw"
os.system("./list2leda %s > %s" % (out_txt, out_gw) )


graph = readLeda(OUT_BASE + "_rew_0.gw")
NR_EDGES = len(graph.edges())
NR_NODES_REW = len(graph.nodes())

print "NR_NODES_ORIG:",NR_NODES_ORIG
print "NR_NODES_REW:",NR_NODES_REW


