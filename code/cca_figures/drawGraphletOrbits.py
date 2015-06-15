#! /usr/bin/env python

#"""
#    Given a set of orbit clusters and an output directory
#    Creates the output directory
#    Draws the orbits that the orbits represent
#
#    Run as:
#        ./testDrawing.py <cluster_file>
#
#    Implemented by:
#        Omer Nebil Yaveroglu
#        17.07.2012 - 17:02
#"""

import sys
import os
import shutil
import networkx as nx
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import numpy as np

import copy

GRAPHLET_SIZE = 5

graphlet_from_orbit = [1]

def pos_idx_to_pos(pos_idx, scale=1):
    return np.array(pos_idx) * scale

def draw_graphlet_orbits(orbitList, orbit2color=None, dark_background=True,
                         vertical_layout=False, figure=None, ax=None,
                         fontsize=20):
    orbitSet = set(orbitList)

    print "---------->>>", orbitSet, "\n\n"

    G = nx.Graph()
    colored_nodes = []
    rest = []
    posDictList = []

    included_widths = []
    included_heights = []

    if dark_background:
        foreground_color = 'w'
        background_color = 'k'
    else:
        foreground_color = 'k'
        background_color = 'w'

    #graphletCols = [ x for x in orbit2color]
    graphletCols = {}
    graphletCols = copy.deepcopy(orbit2color)

    #print "-----graphletCols before", graphletCols
    #graphletCols[1] = []
    #print "-----graphletCols after", graphletCols
    #print "orbit2color after", orbit2color


    # G0
    intersect = set([0]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [0, -1]
        edge_list = [(0, -1)]
        positions = [(2, 2), (2, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
#        posDictList.append(nx.spring_layout(tempG, scale = 1))
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[0]

    # G1
    intersect = set([1]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [1, 2, -2]
        edge_list = [(1, 2), (2, -2)]
        positions = [(2, 3), (2, 2), (2, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[1]

    intersect = set([2]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [3, -3, -4]
        edge_list = [(3, -3), (-3, -4), (-4, 3)]
        positions = [(x * 1.5, y * 1.5) for (x,y) in [(2, 2), (1, 1), (3, 1)]]
        #positions = [(2, 2), (1, 1), (3, 1)]]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[2]

    intersect = set([3]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [4, 5, -5, -6]
        edge_list = [(4, 5), (5, -5), (-5, -6)]
        positions = [(2, 3), (2, 2), (2, 1), (2, 0)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[3]

    intersect = set([4]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [6, 7, -7, -8]
        edge_list = [(6, 7), (7, -7), (7, -8)]
        positions = [(2, 3), (2, 2), (1, 1), (3, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[4]

    intersect = set([5]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [8, -9, -10, -11]
        edge_list = [(8, -9), (-9, -10), (-10, -11), (-11, 8)]
        positions = [(1, 2), (2, 2), (2, 1), (1, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[5]

    intersect = set([6]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [9, 10, 11, -12]
        edge_list = [(9, 11), (11, 10), (11, -12), (10, -12)]
        positions = [(2, 1), (3, 3), (2, 2), (1, 3)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        #print "-------graphletCols:",graphletCols

        for node in node_list:
          orbit2color[node]=graphletCols[6]

    intersect = set([7]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [12, 13, -13, -14]
        edge_list = [(12, 13), (13, -13), (-13, -14), (-14, 12), (13, -14)]
        positions = [(1, 2), (2, 3), (3, 2), (2, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[7]

    intersect = set([8]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [14, -15, -16, -17]
        edge_list = [(14, -15), (14, -16), (14, -17), (-15, -16), (-16, -17), (-17, -15)]
        positions = [(2, 3), (2, 2), (1, 1), (3, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[8]

    # Draw the orbits 15, 16, 17 if in the draw list
    intersect = set([9]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [15, 16, 17, 73, 74]
        edge_list = [(15, 16), (16, 17), (17, 73), (73, 74)]
        positions = [(2, 4), (2, 3), (2, 2), (2, 1), (2, 0)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[9]

    # Draw the orbits 18, 19, 20, 21 if in the draw list
    intersect = set([10]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [18, 19, 20, 21, 75]
        edge_list = [(18, 20), (20, 21), (19, 21), (21, 75)]
        positions = [(2, 4), (1, 1), (2, 3), (2, 2), (3, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[10]

    # Draw the orbits 22, 23 if in the draw list
    intersect = set([11]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [22, 23, 76, 77, 78]
        edge_list = [(23, 22), (23, 76), (23, 77), (23, 78)]
        positions = [(2, 3), (2, 2), (1, 2), (3, 2), (2, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[11]

    # Draw the orbits 24, 25, 26 if in the draw list
    intersect = set([12]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [24, 25, 26, 79, 80]
        edge_list = [(24, 26), (25, 26), (26, 79), (79, 80), (25,79)]
        #positions = [(1, 1), (2, 3), (1, 2), (3, 2), (3, 1)]
        positions = [(x,y*1.3) for (x,y) in [(1, 1), (2, 3), (1, 2), (3, 2), (3, 1)]]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[12]

    # Draw the orbits 27, 28, 29, 30 if in the draw list
    intersect = set([13]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [27, 28, 29, 30, 81]
        edge_list = [(27, 28), (28, 30), (30, 29), (30, 81), (29,81)]
        positions = [(2, 0), (2, 1), (1, 3), (2, 2), (3, 3)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[13]

    # Draw the orbits 31, 32, 33 if in the draw list
    intersect = set([14]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [31, 32, 33, 82, 83]
        edge_list = [(31, 33), (33, 32), (33, 82), (33, 83), (32,83)]
        #positions = [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)]
        positions = [(x,y*1.3) for (x,y) in [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)]]

        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[14]

    # Draw the orbits 34 if in the draw list
    intersect = set([15]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [34, 84, 85, 86, 87]
        edge_list = [(34, 84), (84, 85), (85, 86), (86, 87), (87,34)]
        positions = [(2, 3), (3, 2), (2.5, 1), (1.5, 1), (1, 2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        print "posDictList:", posDictList

        colored_nodes.extend(list(node_list))
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[15]

    # Draw the orbits 35, 36, 37, 38 if in the draw list
    intersect = set([16]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [35, 36, 37, 38, 88]
        edge_list = [(35, 38), (38, 37), (38, 88), (36, 37), (36,88)]
        positions = [(2, 0), (2, 3), (1, 2), (2, 1), (3, 2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(list(node_list))
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[16]

    # Draw the orbits 39, 40, 41, 42 if in the draw list
    intersect = set([17]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [39, 40, 41, 42, 89]
        edge_list = [(39, 42), (42, 40), (42, 41), (42, 89), (40,41), (41, 89)]
        positions = [(2, 0), (1, 2), (2, 3), (2, 1), (3, 2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[17]

    # Draw the orbits 43, 44 if in the draw list
    intersect = set([18]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [43, 44, 90, 91, 92]
        edge_list = [(43, 44), (43, 90), (44, 90), (44, 91), (44,92), (91, 92)]
        positions = [(1, 3), (2, 2), (3, 3), (1, 1), (3, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[18]

    # Draw the orbits 45, 46, 47, 48 if in the draw list
    intersect = set([19]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [45, 46, 47, 48, 93]
        edge_list = [(45, 47), (47, 48), (46, 48), (93, 46), (93,48), (93, 47)]
        positions = [(2, 0), (2, 3), (2, 1), (3, 2), (1, 2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[19]

    # Draw the orbits 49,50 if in the draw list
    intersect = set([20]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [49, 50, 94, 95, 96]
        edge_list = [(49, 50), (49, 94), (50, 95), (94, 95), (50,96), (96, 94)]
        positions = [(1, 2), (2, 1), (2, 3), (2, 2), (3, 2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[20]

    # Draw the orbits 51, 52, 53 if in the draw list
    intersect = set([21]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [51, 52, 53, 97, 98]
        edge_list = [(51, 53), (52, 53), (51, 97), (53, 98), (97,98), (52, 98)]
        positions = [(1, 1), (2, 3), (1, 2), (3, 1), (3, 2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[21]

    # Draw the orbits 54, 55 if in the draw list
    intersect = set([22]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [54, 55, 99, 100, 101]
        edge_list = [(54, 55), (54, 99), (55, 99), (55, 100), (100,99), (55, 101), (101, 99)]
        positions = [(2, 0), (1, 2), (3, 2), (2, 1), (2, 3)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[22]

    # Draw the orbits 56, 57 and 58 if in the draw list
    intersect = set([23]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [56, 57, 58, 102, 103]
        edge_list = [(56, 58), (58, 57), (58, 102), (58, 103), (57,102), (57, 103), (102, 103)]
        positions = [(1, 0), (2, 2 - 0.2), (1, 1 + 0.2), (2, 3), (3, 1 + 0.2)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[23]

    # Draw the orbits 59, 60, and, 61 if in the draw list
    intersect = set([24]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [59, 60, 61, 104, 105]
        edge_list = [(59, 60), (60, 61), (59, 61), (61, 104), (60,104), (61, 105), (105, 104)]
        positions = [(1, 0), (2, 1), (1, 2), (2, 3), (1, 4)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[24]

    # Draw the orbits 62, 63, 64 if in the draw list
    intersect = set([25]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [62, 63, 64, 106, 107]
        edge_list = [(62, 63), (63, 64), (63, 106), (64, 106), (64,107), (107, 106), (62, 107)]
        positions = [(3, 2), (2, 3), (2, 2), (1, 2), (2, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[25]

    # Draw the orbits 65, 66, 67 if in the draw list
    intersect = set([26]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [65, 66, 67, 108, 109]
        edge_list = [(65, 67), (65, 108), (67, 108), (67, 66), (66,108), (67, 109), (66, 109), (108, 109)]
        positions = [(2, 3), (2, 0), (1, 2), (3, 2), (2, 1)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[26]

    # Draw the orbits 68, 69 if in the draw list
    intersect = set([27]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [68, 69, 110, 111, 112]
        edge_list = [(68, 69), (68, 110), (68, 111), (69, 110), (69,111), (69, 112), (110, 112), (111, 112)]
        positions = [(1, 1), (2, 2), (3, 1), (1, 3), (3, 3)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[27]

    # Draw the orbits 70, 71 if in the draw list
    intersect = set([28]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [70, 71, 113, 114, 115]
        edge_list = [(70, 71), (70, 113), (70, 114), (115, 71), (115,113), (115, 114), (71, 113), (113, 114), (114, 71)]
        positions = [(2, 0), (3, 2), (1, 2), (2, 1), (2, 3)]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[28]

    # Draw the orbits 72 if in the draw list
    intersect = set([29]).intersection(orbitSet)
    if len(intersect) <> 0:
        node_list = [72, 116, 117, 118, 119]
        edge_list = [(72, 116), (72, 117), (72, 118), (72, 119), (116,117), (116, 118), (116, 119), (117, 118), (117, 119), (118, 119)]
        #positions = [(2, 3), (3, 2), (2.5, 1), (1.5, 1), (1, 2)]
        positions = [(x*1.3,y) for (x,y) in [(2, 3), (3, 2), (2.5, 1), (1.5, 1), (1, 2)]]
        G.add_nodes_from(node_list)
        G.add_edges_from(edge_list)

        tempG = nx.Graph()
        tempG.add_nodes_from(node_list)
        tempG.add_edges_from(edge_list)
        posDictList.append(dict(zip(node_list, map(pos_idx_to_pos, positions))))

        colored_nodes.extend(node_list)
        rest.extend(list(set(node_list) - intersect))

        (xcoords, ycoords) = zip(*positions)
        included_widths.append(np.max(xcoords) - np.min(xcoords) + 1)
        included_heights.append(np.max(ycoords) - np.min(ycoords) + 1)

        for node in node_list:
          orbit2color[node]=graphletCols[29]


    print "-------posDictList:, ",posDictList

    print "included_widths", included_widths
    print "included_heights", included_heights


    spacing_amount = 4
    pos = {}
    next_graphlet_posn = 0
    if vertical_layout:
        shift_coord_idx = 1
    else:
        shift_coord_idx = 0
    for (posit, width) in zip(posDictList, included_widths):
        for orbit in posit:
            posit[orbit][shift_coord_idx] += next_graphlet_posn
            pos[orbit] = posit[orbit]
#        next_graphlet_posn += spacing_amount

        print "incl_width", width
        next_graphlet_posn += (width + 2)

    if ((figure is None) != (ax is None)):
        raise ValueError('figure or axis given without the other')
    if figure is not None:
        fig = pylab.figure(figure.number)
    else:
        figsize = (len(posDictList) * GRAPHLET_SIZE, GRAPHLET_SIZE)
        figsize = (np.sum(included_widths) + 2*(len(included_widths) - 1),
                   np.max(included_heights))
        if vertical_layout:
            figsize = (figsize[1], figsize[0])
        fig = pylab.figure(figsize=figsize)
        ax = plt.axes([0,0,1,1])

#    print pos

    print "------------>orbit2color:", orbit2color


    if orbit2color is not None:
        #for elem in orbit2color.keys():
        #  orbit2color[elem] = [orbit2color[elem][0] for x in orbit2color[elem]]

        print "------------>orbit2color:", orbit2color

        #if not set(colored_nodes).issubset(set(orbit2color.keys())):
        #    raise ValueError('orbit2color keys do not match set of colored nodes')

        #print "\nnode_color:",node_color

        node_color = [orbit2color[nd] for nd in colored_nodes]
        #node_color = foreground_color

    else:
        node_color = 'r'
    node_size = fontsize * 75

    print "pos:", pos
    print "G:,",G
    print "colored_nodes:", colored_nodes
    print "node_color", node_color
    print "rest:", rest

    draw_nodes_colored = nx.draw_networkx_nodes(G, pos, nodelist = colored_nodes,
        node_size = node_size, node_color=node_color, hold=True)
    #draw_nodes_colored.set_edgecolor(foreground_color)
    draw_nodes_colored.set_edgecolor(node_color)
#    labels = dict((n, n) if n in colored_nodes else (n, '') for n in G.nodes())
    labels= dict()
    nx.draw_networkx_labels(G, pos, labels=labels, font_size = fontsize,
        font_color = background_color, hold=True)

    # if you want to set the node colours to white, commment the next line and swap the lines in the draw_nodes call .. also swap the lines in the if statement
    #node_color = [orbit2color[nd] for nd in colored_nodes]

    draw_nodes = nx.draw_networkx_nodes(G, pos, nodelist = rest,
        node_size = node_size, node_color = node_color, hold=True)
        #node_size = node_size, node_color = foreground_color, hold=True)

    print "edgecolor:",node_color

    #draw_nodes.set_edgecolor(foreground_color)
    #draw_nodes.set_edgecolor(orbit2color[colored_nodes[0]])
    draw_nodes.set_edgecolor(node_color)

    print "node_color", node_color[0]

    #nx.draw_networkx_edges(G, pos, width = 10, edge_color = node_color[0][:-1],
    nx.draw_networkx_edges(G, pos, width = 10, edge_color = foreground_color,
        hold=True)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_axis_bgcolor(background_color)

    pylab.gcf().set_facecolor(background_color)
    return fig
#    fig.savefig(outputName, facecolor=fig.get_facecolor(), edgecolor='none')


if __name__ == '__main__':
    clusterFile = sys.argv[1]

    # Create the output directory
    outputDir = clusterFile.rsplit('.', 1)[0] + '/'
    if os.path.isdir(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)

    fRead = open(clusterFile, 'r')
    lineCount = 1
    for line in fRead:
        orbitList = [int(val) for val in line.strip().split(' ')]

        outputName = outputDir + 'cluster' + str(lineCount) + '.png'
        outputName = outputDir + 'cluster' + str(lineCount) + '.pdf'
        fig = draw_graphlet_orbits(orbitList, fontsize=28)
        fig.savefig(outputName, facecolor=fig.get_facecolor(), edgecolor='none')

        lineCount += 1

    fRead.close()
