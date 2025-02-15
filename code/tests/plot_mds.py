"""
=========================
Multi-dimensional scaling
=========================

An illustration of the metric and non-metric MDS on generated noisy data.

The reconstructed points using the metric MDS and non metric MDS are slightly
shifted to avoid overlapping.
"""

# Author: Nelle Varoquaux <nelle.varoquaux@gmail.com>
# Licence: BSD

print(__doc__)
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

n_samples = 20
seed = np.random.RandomState(seed=3)
X_true = seed.randint(0, 10, 5 * n_samples)
Y_true = [x + 30 for x in X_true]
X_true += Y_true

X_true = np.array(X_true)
print X_true

X_true = X_true.reshape((2 * n_samples, 5))

# Center the data
#X_true -= X_true.mean()


similaritiesX = euclidean_distances(X_true)

# Add noise to the similarities
#noise = np.random.rand(n_samples, n_samples)
#noise = noise + noise.T
#noise[np.arange(noise.shape[0]), np.arange(noise.shape[0])] = 0
#similarities += noise

mds = manifold.MDS(n_components=3, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
posX = mds.fit(similaritiesX).embedding_


#print "similarities:", similarities
#print "(",len(similarities), ",", len(similarities[0]),")"

#nmds = manifold.MDS(n_components=2, metric=False, max_iter=3000, eps=1e-12,
#                    dissimilarity="precomputed", random_state=seed, n_jobs=1,
 #                   n_init=1)
#npos = nmds.fit_transform(similarities, init=pos)

# Rescale the data
#pos *= np.sqrt((X_true ** 2).sum()) / np.sqrt((pos ** 2).sum())
#npos *= np.sqrt((X_true ** 2).sum()) / np.sqrt((npos ** 2).sum())

print "pos:",posX

print X_true
# Rotate the data
#clf = PCA(n_components=3)
#X_true = clf.fit_transform(X_true)

#pos = clf.fit_transform(pos)

#npos = clf.fit_transform(npos)

#print X_true

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(posX[:, 0], posX[:, 1], posX[:,2], c='r', marker='o')
#ax.scatter(posY[:, 0], posY[:, 1], posY[:,2], c='g', marker='o')
plt.show()

#ax = plt.axes([0., 0., 1., 1.])

#plt.scatter(X_true[:, 0], X_true[:, 1], c='r', s=20)
#plt.scatter(pos[:, 0], pos[:, 1], s=20, c='g')
#plt.scatter(npos[:, 0], npos[:, 1], s=20, c='b')
#plt.legend(('True position', 'MDS', 'NMDS'), loc='best')

#similarities = similarities.max() / similarities * 100
#similarities[np.isinf(similarities)] = 0


# Plot the edges
#start_idx, end_idx = np.where(pos)
#a sequence of (*line0*, *line1*, *line2*), where::
#            linen = (x0, y0), (x1, y1), ... (xm, ym)
#segments = [[X_true[i, :], X_true[j, :]]
#            for i in range(len(pos)) for j in range(len(pos))]
#values = np.abs(similarities)
#lc = LineCollection(segments,
#                    zorder=0, cmap=plt.cm.hot_r,
#                    norm=plt.Normalize(0, values.max()))
#lc.set_array(similarities.flatten())
#lc.set_linewidths(0.5 * np.ones(len(segments)))
#ax.add_collection(lc)

