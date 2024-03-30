# ////////////////// #
# CLUSTER ALGORITHM  # 
# ////////////////// #


# How to know if two clustesr are similar?
# look at distance between clusters
# most common distance EQU: Euclidian

# How do we measure distance, as clusters may have multiple points?
# Centroid distance: distance btw centroids
# Complete linkage: distance btw two farthest points
# Single linkages: distance btw two nearest points
# Average linkages: distance btw point and all other points, done for all points, then averaged
# Ward's linkage: distance that minimizes variance within cluster, maximizes variance between clusters

# How can we graphically represent the history of making our clusters?
# Dendrogram

# AgglomerativeClustering object performs a hierarchical clustering using a bottom up approach



# IMPORTS
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

# here is some text
# MODEL 
# X = data matrix with more than 2 variables
model = AgglomerativeClustering(affinity='euclidean', linkage='ward')
clusters = model.fit_predict(X)

