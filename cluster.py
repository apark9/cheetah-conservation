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


# SAMPLEp

import numpy as np

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

# Import iris data 
iris = datasets.load_iris()

iris_data = pd.DataFrame(iris.data)
iris_data.columns = iris.feature_names
iris_data['flower_type'] = iris.target
iris_data.head()

print("here!")