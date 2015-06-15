#!/usr/bin/env python

"""
	Sample the edges based on the total threshold

	Run as:
		./thresholdNetworks.py <folder_to_summarize> <rate>


	Implemented by:
		Omer Nebil Yaveroglu
		29.10.2012 - 15:02
"""


import os
import sys

folderName = sys.argv[1]

print sys.argv[2]
rate = float(sys.argv[2])

if not folderName.endswith('/'):
	folderName += '/'

files = [str(x) + ".undirected" for x in [1970, 1980, 1990, 2000, 2010]]

fileList = os.listdir(folderName)

for file in files:
	if file.endswith('.undirected'):
		path = folderName + file
		edges = []

		fRead = open(path, 'r')

		totalWeight = 0
		for line in fRead:
			splitted = line.strip().split('\t')
			edges.append((splitted[0] , splitted[1] , float(splitted[3])))
			totalWeight += float(splitted[3])

		fRead.close()

		# Choose the top edges until the sample rate is achieved
		sorted_edges = sorted(edges, key=lambda edges: edges[2], reverse = True)

		accepted_edges = []
		currentWeight = 0

		for edge in sorted_edges:
			currentWeight += edge[2]
			accepted_edges.append((edge[0], edge[1]))

			if (currentWeight / totalWeight) > (rate / 100):
				break

		# Write the chosen edges
		outputFile = folderName + file.split(".")[0] + "-" + str(int(rate)) + ".undirected"
		fWrite = open(outputFile , 'w')

		for edge in accepted_edges:
			fWrite.write(edge[0] + '\t' + edge[1] + '\n')

		fWrite.close()

		os.system('./list2leda.py ' + outputFile)


