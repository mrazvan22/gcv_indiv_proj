# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 10:13:02 2012

@author: darren
"""

from __future__ import division

import collections
import re
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import sys

import drawGraphletOrbits

N_ORBITS = 73
POINTS_PER_INCH = 72

negate_corr_signs = bool(int(sys.argv[4]))

varnames_to_desc = {
    "CC" : 'Consumption GDP',
    "TCGDP" : 'GDP',
    "CI" : 'Investment GDP',
    "POPULATION" : 'Population Size',
    "LE" : '# Employed',
    "CG" : 'Gov\'t Consumption GDP',
    "PCPIPCH" : 'Inflation Index',
    "GGXWDG_NGDP" : 'Gov\'t Gross Debt (% GDP)',
    "XRAT" : 'Exchange Rate vs USA',
    "LUR" : 'Unemployment %',
    "GGR_NGDP" : 'Gov\'t Revenue (% GDP)',
    "BCA" : 'Current Account Balance'
    }

def _attr_name_fxn(attr_str):
#    return re.sub(r'[\s"\']+', '', attr_str)
    return re.sub(r'["\']+', '', attr_str)

def _orbit_name_fxn(graphlet_str):
    digit_seqs = [elt for elt in re.split('\D', graphlet_str) if elt]
    if len(digit_seqs) == 0:
        raise ValueError('no digit sequence found in graphlet name')
    if len(digit_seqs) > 1:
        raise ValueError('more than one digit sequence found in graphlet name')
    return int(digit_seqs[0])

AttrCor = collections.namedtuple('AttrCor', ['attribute', 'correlation'])
def read_attrs_file(attrs_path, attr_fxn):
    print "reading: {0}".format(attrs_path)
    in_file = open(attrs_path, 'rt')
    attr_cors = []
    line_num = 0
    for line in in_file:
        line_num += 1
#        elts = [elt for elt in re.split('\s|[;\,]', line.strip()) if elt]
        elts = [elt for elt in re.split('[;\,\ ]', line.strip()) if elt]
        print "elts:"
        print elts
        if len(elts) == 0:
            continue
        if len(elts) != 2:
            print ('ERROR: each line of the attributes file {0} should be ' +
                'of the form "attribute_name correlation"').format(
                attrs_path)
            sys.exit()
        try:
            attr = attr_fxn(elts[0])
        except ValueError as ve:
            print "ERROR: line {0}: {1}".format(line_num, ve)
        try:
            cor = float(elts[1])
        except ValueError:
            print ('ERROR: line {0}: column 2 (correlation column): "{1}" not '
                'interpretable as a floating-point value').format(
                line_num, elts[1])
            sys.exit()
        if abs(cor) > 1:
            print 'WARNING: line {0}: correlation outside the range [-1,1]'.format(
                line_num)
        if negate_corr_signs:
            cor = -cor
        attr_cors.append(AttrCor(attribute=attr, correlation=cor))
    print attr_cors
    return attr_cors

def make_colormap(dark_background):
    if dark_background:
        mid_val = (1, 1, 1)
#        mid_val = (0.75, 0.75, 0.75)
    else:
        mid_val = (0, 0, 0)
#        mid_val = (0.25, 0.25, 0.25)
    mid_val = (0, 0, 1)
    strong_pos = (0, 1, 0)
    strong_neg = (255/255, 165/255, 0)
    strong_neg = (255/255, 50/255, 0)
    strong_neg = (255/255, 0/255, 0)
    cmap = colors.LinearSegmentedColormap.from_list('posToNeg',
        [(1, 0, 0), (1, 1, 0), (0, 1, 0)])
    return cmap

def cor_to_color(cor, dark_background):
    min_contrast = 0
    cor = np.minimum(cor, 1)
    cor = np.maximum(cor, -1)
#    if dark_background:
#        color_amt = abs(cor) * (1-min_contrast) + min_contrast
#        fill_val = 0
#    else:
#        color_amt = 1
#        fill_val = 1-abs(cor)
#        fill_val = fill_val * (1-min_contrast)
#    if cor > 0:
#        color = (color_amt, fill_val, fill_val)
#    else:
#        color = (fill_val, fill_val, color_amt)
    pos_to_neg_cmap = make_colormap(dark_background)
    map_val = np.sign(cor) * (np.abs(cor) * (1 - min_contrast) + min_contrast)
    map_val = (map_val + 1)/2
#    color = pos_to_neg_cmap(((cor + 1)/2)*255)
    color = pos_to_neg_cmap(map_val)
#    color = (color[0]/255, color[1]/255, color[2]/255)
#    print "{0} -> {1}".format(cor, color)
    return color

def display_attr_cors(attr_cors, fig, ax, dark_background, fontsize,
                      attrs2txt=None, xpos=0, start_ypos=0):
#    ax = fig.add_subplot(111, visible=False)
    nxt_ypos = start_ypos
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = -np.inf
    if not negate_corr_signs:
        attr_cors = reversed(attr_cors)
    for attr_cor in attr_cors:
        attr_txt = attr_cor.attribute
        attr_txt = attrs2txt.get(attr_txt, attr_txt) if attrs2txt else attr_txt
        txt = fig.text(xpos, nxt_ypos, attr_txt, fontsize=fontsize,
            color = cor_to_color(attr_cor.correlation, dark_background),
            transform = ax.transData)
        fig.canvas.draw()
        tbox = txt.get_window_extent()
#        print tbox.y1-tbox.y0
        tbox = tbox.transformed(ax.transData.inverted())
        text_height = tbox.y1-tbox.y0
        x_min = np.min([x_min, tbox.x0, tbox.x1])
        x_max = np.max([x_max, tbox.x0, tbox.x1])
        y_min = np.min([y_min, tbox.y0, tbox.y1])
        y_max = np.max([y_max, tbox.y0, tbox.y1])
#        print text_height
        nxt_ypos += text_height
    return (x_min, x_max, y_min, y_max)

def vis_attrs_vs_graphlets(attrs_path, orbits_path, out_name, attrs2txt=None):
    dark_background = True
    fontsize=36

    if dark_background:
        bg_color = (0, 0, 0)
        fg_color = (1, 1, 1)
    else:
        bg_color = (1, 1, 1)
        fg_color = (0, 0, 0)

    n_top = 3
    attr_cors = read_attrs_file(attrs_path, _attr_name_fxn)
#    print attr_cors
    gphl_cors = read_attrs_file(orbits_path, _orbit_name_fxn)
#    print gphl_cors

    text_pad_inches = fontsize/POINTS_PER_INCH

    # figure out how big the attribute-text region is, which we can only know
    # for sure after it is rendered
    test_plot_size = 10
    testFig = plt.figure(figsize=(test_plot_size, test_plot_size))
    testAx = plt.subplot(gridspec.GridSpec(1, 1, left=0, right=1)[0])
    (x_min, x_max, y_min, y_max) = display_attr_cors(
        attr_cors, testFig, testAx, dark_background=dark_background,
        fontsize=fontsize, attrs2txt=attrs2txt)
    plt.title(str((x_min, x_max, y_min, y_max)))
    text_size_x = (x_max - x_min) * test_plot_size
    text_size_y = (y_max - y_min) * test_plot_size
    print "text_size (x, y) = " + str((text_size_x, text_size_y))
    plt.savefig('testFig.png')
    plt.close(testFig)

    figsize = (drawGraphletOrbits.GRAPHLET_SIZE * n_top,
               drawGraphletOrbits.GRAPHLET_SIZE * 2 )
    width_ratio = [text_size_x + 2*text_pad_inches, figsize[0]]
    figsize = (figsize[0] + text_size_x + 2*text_pad_inches, figsize[1])
    if text_size_y > figsize[1]:
        print ("WARNING: attribute text vertical size exceeds figure height" +
            "; expanding figure height")
        figsize = (figsize[0], text_size_y)
    fig = plt.figure(figsize=figsize)

#    width_ratio = [1,n_top]
#    axText = plt.subplot(1,2,1)
    gs = gridspec.GridSpec(1, 2, width_ratios=width_ratio, wspace=0,
        left=0, right=1)
    axText = plt.subplot(gs[0], frame_on=False)
    axText.set_xticks([])
    axText.set_yticks([])

#    xpos=1.0/(n_top+2)
    xpos = text_pad_inches/figsize[0]
    print figsize[1]
    print text_size_y
    start_ypos = (figsize[1] - text_size_y)/(figsize[1])
    display_attr_cors(attr_cors, fig, axText, dark_background=dark_background,
                      fontsize=fontsize, attrs2txt=attrs2txt,
                      xpos=xpos, start_ypos=start_ypos)
    plt.title("Attributes:", fontsize=fontsize, color=fg_color)

    orbit2color = dict([
        (gcor.attribute, cor_to_color(gcor.correlation, dark_background))
        for gcor in gphl_cors if gcor.attribute in range(0, N_ORBITS)])

    gphl_cors.sort(key=lambda x:x.correlation, reverse=True)
    hi_pos_cor_orbits = [attr_cor.attribute for attr_cor in gphl_cors[0:n_top]]
    hi_neg_cor_orbits = [attr_cor.attribute for attr_cor in gphl_cors[-n_top:]]
    gs = gridspec.GridSpec(2, 2, width_ratios=width_ratio, wspace=0, left=0, right=1)
#    axPos = plt.subplot(2,2,2)
    node_label_scale = (2/3)
    axPos = plt.subplot(gs[1], frame_on=False)
    drawGraphletOrbits.draw_graphlet_orbits(
        hi_pos_cor_orbits, orbit2color=orbit2color,
        dark_background=dark_background, vertical_layout=False,
        figure=plt.gcf(), ax=axPos, fontsize=fontsize*node_label_scale)

    hi_pos_cor_orbits.sort()
    hi_neg_cor_orbits.sort()

    # highest correlation graphlets
    plt.title("G%d                    G%d                  G%d" % tuple(hi_pos_cor_orbits), fontsize=fontsize, color=fg_color)
#    axNeg = plt.subplot(2,2,4)
    axNeg = plt.subplot(gs[3], frame_on=False)
    drawGraphletOrbits.draw_graphlet_orbits(
        hi_neg_cor_orbits, orbit2color=orbit2color,
        dark_background=dark_background, vertical_layout=False,
        figure=plt.gcf(), ax=axNeg, fontsize=fontsize*node_label_scale)

    fig.set_facecolor(bg_color)
#    axText.set_axis_bgcolor(bg_color)
#    axPos.set_axis_bgcolor(bg_color)
#    axNeg.set_axis_bgcolor(bg_color)

    # lowest correlation graphlets
    #plt.title("\n\norbits with lowest correlation:",
    #    fontsize=fontsize, color=fg_color)
    plt.title("G%d                      G%d                     G%d" % tuple(hi_neg_cor_orbits), fontsize=fontsize, color=fg_color)
    plt.savefig(out_name + '.png', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(out_name + '.pdf', facecolor=fig.get_facecolor(), edgecolor='none')
#    plt.show()

#    cbarFig = plt.figure(facecolor=bg_color)
#    vals = np.arange(-1, 1.01, 0.01)
#    plt.matshow(np.meshgrid(vals, vals)[0], cmap=make_colormap(dark_background))
#    plt.colorbar(ticks=[-1, 0, 1])
#    plt.savefig('cbar.pdf')

#    display_cor_scatterplots(attr_cors, gphl_cors)
#    plt.show()

# test output in fodr/vis_test
def display_cor_scatterplots(attr_cors, gphl_cors):
    attr_cors.sort(key=lambda x:x.correlation)
    gphl_cors.sort(key=lambda x:x.correlation)

    attr_xpos = range(len(attr_cors))
    attr_corvals = [attr.correlation for attr in attr_cors]
    plt.figure()
    plt.bar(attr_xpos, attr_corvals)
    plt.ylim([-1, 1])
    plt.title("economic-attribute correlations (canonical cross-loadings) with graphlet orbits")
    plt.xlabel("economic attribute labels would go here (one per bar)")
    plt.ylabel("correlation with graphlet orbits")
    plt.savefig(out_name + '_attr-crossloadings.pdf')
    plt.savefig(out_name + '_attr-crossloadings.png')

    gphl_xpos = range(len(gphl_cors))
    gphl_corvals = [gphl.correlation for gphl in gphl_cors]
    plt.figure()
    plt.bar(gphl_xpos, gphl_corvals)
    plt.ylim([-1, 1])
    plt.title("graphlet orbit correlations (canonical cross-loadings) with economic attributes")
    plt.xlabel("graphlet orbit labels would go here (one per bar)")
    plt.ylabel("correlation with economic attributes")
    plt.savefig(out_name + '_gphl-crossloadings.pdf')
    plt.savefig(out_name + '_gphl-crossloadings.png')

    print len(attr_xpos)
    print attr_xpos
    print len(attr_corvals)
    print attr_corvals

#    attr_xpos = range(len(attr_cors))
#    attr_corvals = [attr.correlation for attr in attr_cors]
#    plt.figure()
#    plt.bar(attr_xpos, attr_corvals)
#    plt.ylim([-1, 1])
#    plt.title("economic-attribute correlations (canonical cross-loadings) with graphlet orbits")
#    plt.xlabel("economic attribute labels would go here")
#    plt.ylabel("correlation with graphlet orbits")
#    plt.savefig(out_name + '_attr-crossloadings.pdf')
#    plt.savefig(out_name + '_attr-crossloadings.png')
#
#    gphl_xpos = range(len(gphl_cors))
#    gphl_corvals = [gphl.correlation for gphl in gphl_cors]
#    plt.figure()
#    plt.bar(gphl_xpos, gphl_corvals)
#    plt.ylim([-1, 1])
#    plt.title("graphlet orbit correlations (canonical cross-loadings) with economic attributes")
#    plt.xlabel("graphlet orbit labels would go here")
#    plt.ylabel("correlation with economic attributes")
#    plt.savefig(out_name + '_gphl-crossloadings.pdf')
#    plt.savefig(out_name + '_gphl-crossloadings.png')

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "usage: visAttrsVsGraphlets attrs_path orbits_path out_name"
        sys.exit()

    attrs_path = sys.argv[1]
    orbits_path = sys.argv[2]
    out_name = sys.argv[3]

    vis_attrs_vs_graphlets(attrs_path, orbits_path, out_name, attrs2txt=None)
