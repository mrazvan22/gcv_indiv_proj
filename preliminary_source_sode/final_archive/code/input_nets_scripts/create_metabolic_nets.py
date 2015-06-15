import sys
sys.path.append('/vol/bio-nets/packages/networkx-1.8.1')
import networkx as nx
import numpy as np



if(len(sys.argv) != 3):
  print "Error parsing parameters. Usage: create_metabolic_nets <input_net_file> <output_net_file> "
  exit()

INPUT_NET=sys.argv[1]
OUTPUT_NET=sys.argv[2]



g = nx.Graph()
edgeList = []

with open(INPUT_NET) as f:
    for line in f:
        words = line.split()
        newEdge = words[0:2] + [x for x in words if x[0:3] == 'ec:']
        edgeList += [newEdge]

print np.array(edgeList[0:6])

#for e in g.edges():
#     print e[0], e[1]

with open(OUTPUT_NET, "w") as f:
  for e in edgeList:
    f.write(e[0])
    for i in range(1,len(e)):
      f.write(" " + e[i])
    f.write("\n")

print len(edgeList)
