import sys
sys.path.append('/vol/bio-nets/packages/networkx-1.8.1')
import networkx as nx
import os



if(len(sys.argv) != 3):
  print "Error parsing parameters. Usage: filter_litarature_nets <input_net_file> <output_net_file>"
# hc = high confidence network, i.e. each pair of interacting proteins need to have at least 2 different publication sources

INPUT_NET=sys.argv[1]
OUTPUT_NET=sys.argv[2]

g = nx.Graph()

with open(INPUT_NET) as f:
    d = 0;
    for line in f:
        a,b = line.split()
        a = a.upper()
        b = b.upper()
        # remove self loops
        if a==b:
          continue
        g.add_nodes_from([a,b])
        g.add_edge(a,b)


#for e in g.edges():
#     print e[0], e[1]

with open(OUTPUT_NET, "w") as f:
  for e in g.edges():
    f.write(e[0] + " " + e[1] + "\n")

f.close()
print len(g.nodes()), len (g.edges())
core_name = "_".join(OUTPUT_NET.split("_")[:-1])
cmd = "../../list2leda " + OUTPUT_NET + " > " + core_name + ".gw"
print "Running: ", cmd
os.system(cmd)
