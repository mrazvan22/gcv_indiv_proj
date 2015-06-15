
import sys
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import scipy.stats



OUT_PERFECT = "final_results/spear_images/perfect"
OUT_SPREAD = "final_results/spear_images/spread"
OUT_OUTLIERS = "final_results/spear_images/outliers"


x_perf = [float(x) / 10 for x in range(-10,10)]
y_perf = [math.pow(x,3) for x in x_perf]

x_spread = np.random.uniform(-1, 1, 80)
y_spread = np.random.uniform(-1, 1, 80)

mean = [-5, 0.0]
cov = [[5,5],[0.2,-0.2]]
sample = np.random.multivariate_normal(mean, cov, 80)
x_outliers = [x/10 for x in sample[:,0]]
y_outliers = [x/10 for x in sample[:,1]]

outliers = [(0.6,0.0),(0.7,-0.1),(0.63,-0.15),(0.65,0.05),(0.72,0.2),(0.5,0.0)]

x_outliers += [x for (x,y) in outliers]
y_outliers += [y for (x,y) in outliers]


pears_perf = scipy.stats.pearsonr(x_perf, y_perf)
pears_spread = scipy.stats.pearsonr(x_spread, y_spread)
pears_outliers = scipy.stats.pearsonr(x_outliers, y_outliers)

spear_perf = scipy.stats.spearmanr(x_perf, y_perf)
spear_spread = scipy.stats.spearmanr(x_spread, y_spread)
spear_outliers = scipy.stats.spearmanr(x_outliers, y_outliers)

print pears_perf

print "perf: pears (%.3f, %.3f) spear (%.3f, %.3f)" % (pears_perf[0], pears_perf[1], spear_perf[0], spear_perf[1])
print "spread: pears (%.3f, %.3f) spear (%.3f, %.3f)" % (pears_spread[0], pears_spread[1], spear_spread[0], spear_spread[1])
print "outliers: pears (%.3f, %.3f) spear (%.3f, %.3f)" % (pears_outliers[0], pears_outliers[1], spear_outliers[0], spear_outliers[1])


fig = plt.figure(figsize=(6, 6))
# Create an Axes object.
ax1 = fig.add_subplot(1,1,1) # one row, one column, first plot

#np.random.seed(seed=1)

#x = np.random.uniform(0, 1, NR_NODES)
#y = np.random.uniform(0, 1, NR_NODES)

ax1.set_xlim([-1, 1])
ax1.set_ylim([-1, 1])

ax1.set_xlabel('X', fontsize=16)
ax1.set_ylabel('Y', fontsize=16)

# Plot non-ordered points
#ax1.scatter(x_perf, y_perf, marker="o")
#ax1.scatter(x_spread, y_spread, marker="o")
ax1.scatter(x_outliers, y_outliers, marker="o")
plt.show()


