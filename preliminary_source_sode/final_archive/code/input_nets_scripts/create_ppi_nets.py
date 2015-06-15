import sys
sys.path.append('/vol/bio-nets/packages/networkx-1.8.1')
import networkx as nx


def is_high_confidence(a, b, edgeList):
  pubs = []
  for edge in edgeList:
    if ( (edge[0] == a and edge[1] == b) or (edge[1] == a and edge[0] == b)):
      pubs += [int(edge[2])]

  return len (set(pubs)) > 1


if(len(sys.argv) != 4):
  print "Error parsing parameters. Usage: create_ppi_nets <input_net_file> <output_net_file> <normal/hc>"
# hc = high confidence network, i.e. each pair of interacting proteins need to have at least 2 different publication sources

INPUT_NET=sys.argv[1]
OUTPUT_NET=sys.argv[2]
TYPE=sys.argv[3]



g = nx.Graph()
edgeList = []

with open(INPUT_NET) as f:
    for line in f:
        a,b,c = line.split()
        #a,b = line.split()
        #edgeList += [[a,b]]
        edgeList += [[a,b,c]]

#print edgeList

with open(INPUT_NET) as f:
    d = 0;
    for line in f:
        #a,b = line.split()
        a,b,c = line.split()
        a = a.upper()
        b = b.upper()
        # remove self loops
        if a==b:
          continue
        g.add_nodes_from([a,b])
        if(TYPE == "normal"):
          g.add_edge(a,b)
        elif(TYPE == "hc"):
          if(is_high_confidence(a, b, edgeList)):
            g.add_edge(a,b)
        if ((d % 1422) == 0):
          print str(d / 1422) + "%\n"
        d += 1

#for e in g.edges():
#     print e[0], e[1]

with open(OUTPUT_NET, "w") as f:
  for e in g.edges():
    f.write(e[0] + " " + e[1] + "\n")

print len(g.nodes()), len (g.edges())
