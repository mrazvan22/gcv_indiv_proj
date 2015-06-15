#! /usr/bin/env python
# usage: python convert_indicators_to_cvs_single <indicator_type> <input_file> <output_file>
#indicator type can be: "GO", "EC" (without quotation marks)
# converts the indicators to a .cvs file, on a network by network basis


import os
import sys
import csv
import networkx as nx
#from ..edgeList import readLeda


TYPE=sys.argv[1]
INPUT=sys.argv[2]
OUTPUT=sys.argv[3]


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


# resulting file is too big .. at least 111MB
if(TYPE == "GO"):
  go_dict = {}
  go_list = []
  with open(INPUT) as f:
    for line in f:
        words = line.split("\t")
        protein = words[0]
        go_term = words[1].split("\n")[0]
        go_list += [go_term]
        #print words[1]
        if(protein not in go_dict ):
          go_dict[protein] = [go_term]
        else:
          go_dict[protein] += [go_term]
        #print go_dict[protein]
        #print go_list

  #remove duplicated from list:
  go_list = list(set(go_list))

  with open(OUTPUT, 'wb') as out:
    #writer = csv.writer(out)
    #writer.writerows(['ID'] + go_list)
    out.write("ID")
    for go_term in go_list:
      out.write("," + go_term)
    out.write("\n")

    for protein in go_dict.keys():
      out.write(protein)
      for go_term in go_list:
        if(go_term in go_dict[protein]):
          out.write(",1")
        else:
          out.write(",0")
      out.write("\n")



if(TYPE == "EC"):
  net = readLeda(INPUT)
  with open(OUTPUT, 'wb') as out:
    out.write("ID,EC1,EC2,EC3,EC4,EC5,EC6\n")
    for node in net.nodes():
      out.write(node)
      ec_nr = int(node.split(".")[0].split(":")[1])
      for i in range(1,7):
        if(i == ec_nr):
          out.write(",1")
        else:
          out.write(",0")
      out.write("\n")

# 14 functional properties for yeast + additional logic for node labels
if(TYPE == "FUNCTIONAL"):
  protein_to_function_dict = {} # maps protein codes to function (string -> string)
  with open(INPUT) as f:
    for line in f:
        words = line.split("\t")
        protein = words[0]
        function = (" ".join(words[1:]))[:-1]
        protein_to_function_dict[protein] = function

  print "nr of functions=", set(protein_to_function_dict.values())

  aux_file = "indicators/yeast_ppi/ppi.dic"
  protein_to_id_dict = {} # maps protein codes to node numbers (string -> int)
  with open(aux_file) as g:
    for line in g:
        words = line.split("\t")
        ID = int(words[0][2:])
        protein = words[1][:-1]
        protein_to_id_dict[protein] = ID

  #print protein_to_function_dict
  #print protein_to_id_dict

  with open(OUTPUT, 'wb') as out:
    #writer = csv.writer(out)
    #writer.writerows(['ID'] + go_list)
    out.write("ID")
    functions = list(set(protein_to_function_dict.values()))
    functions = [f for f in functions if f != '']

    # having a comma in the names will mess up the CSV file, which contains comma separated terms
    assert ',' not in " ".join(functions)

    for func in functions:
      out.write("," + func)
    out.write("\n")

    print functions
    print len(protein_to_function_dict.keys())
    print len(protein_to_id_dict.keys())

    for protein in protein_to_function_dict.keys():
      if(protein in protein_to_id_dict.keys()):
        out.write(str(protein_to_id_dict[protein]))
        for func in functions:
          #print func + " --- " + protein + " --- " + protein_to_function_dict[protein]
          if(func in protein_to_function_dict[protein]):
            out.write(",1")
          else:
            out.write(",0")
        out.write("\n")

# same as before but with no extra logic for node labels
if(TYPE == "FUNCTIONAL_SIMPLE"):
  protein_to_function_dict = {} # maps protein codes to function (string -> string)
  print "Reading file: ", INPUT
  with open(INPUT) as f:
    for line in f:
        words = line.split("\t")
        protein = words[0]
        function = (" ".join(words[1:]))[:-1]
        protein_to_function_dict[protein] = function

  print "nr of functions=", set(protein_to_function_dict.values())

  with open(OUTPUT, 'wb') as out:
    #writer = csv.writer(out)
    #writer.writerows(['ID'] + go_list)
    out.write("ID")
    functions = list(set(protein_to_function_dict.values()))
    functions = [f for f in functions if f != '']

    # having a comma in the names will mess up the CSV file, which contains comma separated terms
    assert ',' not in " ".join(functions)

    for func in functions:
      out.write("," + func)
    out.write("\n")

    print functions
    print len(protein_to_function_dict.keys())

    for protein in protein_to_function_dict.keys():
      out.write(protein)
      for func in functions:
        #print func + " --- " + protein + " --- " + protein_to_function_dict[protein]
        if(func in protein_to_function_dict[protein]):
          out.write(",1")
        else:
          out.write(",0")
      out.write("\n")


if(TYPE== "METABOLIC_COMPOUND"):
  cpd_to_ecs = {} # maps each compounds to a list of ECs (the ECs will only store the first number)
  with open(INPUT) as f:
    for line in f:
      words = line.split(" ")
      cpd1 = words[0]
      cpd2 = words[1]

      assert "\n" not in cpd1 or "\n" not in cdp2

      ecs = words[2:]
      ecs = [int(ec[3]) for ec in ecs]

      if(cpd1 in cpd_to_ecs.keys()):
        cpd_to_ecs[cpd1] += ecs
      else:
        cpd_to_ecs[cpd1] = ecs

      if(cpd2 in cpd_to_ecs.keys()):
        cpd_to_ecs[cpd2] += ecs
      else:
        cpd_to_ecs[cpd2] = ecs

  # remove the duplicate ECs in the lists
  for key in cpd_to_ecs.keys():
    cpd_to_ecs[key] = list(set(cpd_to_ecs[key]))

  with open(OUTPUT, "w") as f:

    f.write("ID")
    for i in range(1,7):
      f.write(",EC"+str(i))
    f.write("\n")

    for key in cpd_to_ecs.keys():
      f.write(key)
      for i in range(1,7):
        if(i in cpd_to_ecs[key]):
          f.write(",1")
        else:
          f.write(",0")
      f.write("\n")


  print cpd_to_ecs.keys()[:10]
  print cpd_to_ecs.values()[:10]

