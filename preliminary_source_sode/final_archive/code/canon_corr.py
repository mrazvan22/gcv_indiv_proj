from sklearn.cross_decomposition import CCA
import numpy as N


X = N.array([[0., 0., 1.], [1.,0.,0.], [2.,2.,2.], [3.,5.,4.]])
Y = N.array([[0.1, -0.2], [0.9, 1.1], [6.2, 5.9], [11.9, 12.3]])

Z = [
[ 191, 36, 50,  5, 162,  60],
[ 189, 37, 52,  2, 110,  60],
[ 193, 38, 58, 12, 101, 101],
[ 162, 35, 62, 12, 105,  37],
[ 189, 35, 46, 13, 155,  58],
[ 182, 36, 56,  4, 101,  42],
[ 211, 38, 56,  8, 101,  38],
[ 167, 34, 60,  6, 125,  40],
[ 176, 31, 74, 15, 200,  40],
[ 154, 33, 56, 17, 251, 250],
[ 169, 34, 50, 17, 120,  38],
[ 166, 33, 52, 13, 210, 115],
[ 154, 34, 64, 14, 215, 105],
[ 247, 46, 50,  1,  50,  50],
[ 193, 36, 46,  6,  70,  31],
[ 202, 37, 62, 12, 210, 120],
[ 176, 37, 54,  4,  60,  25],
[ 157, 32, 52, 11, 230,  80],
[ 156, 33, 54, 15, 225,  73],
[ 138, 33, 68,  2, 110,  43]
]

print X.shape

#X = N.array(Z)[:,0:3].tolist()
#Y = N.array(Z)[:,3:6].tolist()
print 'X=\n',X
print 'Y=\n',Y


Rx = N.corrcoef(X.T)
Ry = N.corrcoef(Y.T)

cca = CCA(n_components=1)
cca.fit(X, Y)

print "Rx:\n", Rx
print "Ry:\n", Ry
print "x_weights:\n", cca.x_weights_
print "y_weights:\n", cca.y_weights_
print "x_loadings:\n", cca.x_loadings_
print "y_loadings:\n", cca.y_loadings_
print "x_scores_:\n", cca.x_scores_
print "y_scores_:\n", cca.y_scores_

loadings_man_x = N.dot(Rx, cca.x_weights_)
loadings_man_y = N.dot(Ry, cca.y_weights_)
print "loadings_man_x:\n",loadings_man_x
print "loadings_man_y:\n",loadings_man_y

print cca.get_params()

#X_c, Y_c = cca.transform(X, Y)
#print "\n\n", X_c,"\n\n", Y_c

