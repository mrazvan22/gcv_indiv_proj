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
	
folder = sys.argv[1].rstrip('/')

fileList = os.listdir(folder)
for file in fileList:
	if file.endswith('.gw'):
		gwFile = folder + '/' + file
		outputPath = file.rsplit('.', 1)[0] + '.txt'
	
		network = readLeda(gwFile)
	
		fWrite = open(outputPath, 'w')
		for edge in network.edges():
			fWrite.write('{0}\t{1}\n'.format(edge[0], edge[1]))
		fWrite.close()