# ////////////////// #
# CLUSTER ALGORITHM  # 
# ////////////////// #

'''
HIGH-LEVEL NOTES
'''
# 1. initial clustering: split dataset into two clusters
# 2. select parents: two most dissimilar datapoints (could do this through scipy.spatial.distance)
# 3. generate children: merge parents and create children
# 4. add children: add children to dataset
# 5. repeat: repeat steps 2-4 until stopping criterion is met
# 6. stopping criterion: number of clusters is equal to the number of clusters specified

# IMPORTS
import matplotlib.pyplot as plt

'''
TO FIGURE OUT LATER
'''
# understand HiPart / DePDDP
# have to figure out how to merge parents, how do we select two specific datapoints to merge?

# DIVISIVE PACKAGE ATTEMPT
from HiPart.clustering import DePDDP
from sklearn.datasets import make_blobs

# for later, HiPart allows for PCA / other dimensionality reduction steps
# for now, we will just use the data as is

X, y = make_blobs(n_samples=100, centers=6, n_features=2, random_state=42)
clustered_class = DePDDP(max_clusters_number=6).fit_predict(X)

plt.scatter([x[0] for x in X], [x[1] for x in X], c=clustered_class)
plt.title('Divisive Clustering Results')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
