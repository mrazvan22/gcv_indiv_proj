#!/usr/bin/env python

import sys
import os
import networkx as nx

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

if(len(sys.argv) != 3):
  print 'Error parsing parameters. Usage: python add_extra_node.py <input_net.gw> <out_net.txt>'
  exit()

net_gw_file = sys.argv[1]
outputPath = sys.argv[2]

if net_gw_file.endswith('.gw'):

  network = readLeda(net_gw_file)

  fWrite = open(outputPath, 'w')
  for edge in network.edges():
    fWrite.write('{0}\t{1}\n'.format(edge[0], edge[1]))

  #add the extra node ZZZ and connect it with all the other nodes
  for node in network.nodes():
		fWrite.write('ZZZ\t{0}\n'.format(node))

  fWrite.close()
