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
import numpy as np
import random
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import squareform
# from data_generation.data import synthetic_specimens

'''
SYNTHETIC DATASET
- take in a set of nucleotide sequences
- convert to binary encoding
'''

def generate_nucleotide_sequences(num_sequences, sequence_length):

    # want to generate nucleotides (gene reference) for multiple cheetahs
    # will remove this function once dataset is generated from features

    nucleotides = ['A', 'C', 'G', 'T']
    sequences = [''.join([random.choice(nucleotides) for _ in range(sequence_length)]) 
                 for _ in range(num_sequences)]
    return sequences

def custom_distance_matrix(sequences):
    # function that counts the number of differences between two sequences

    matrix_size = len(sequences)
    distance_matrix = np.zeros((matrix_size, matrix_size))

    for i, seq1 in enumerate(sequences):
        for j, seq2 in enumerate(sequences):
            if i != j:
                distance_matrix[i][j] = sum(el1 != el2 for el1, el2 in zip(seq1, seq2))
    return distance_matrix

def calculate_variance(cluster_labels, nucleotides):
    variance = 0
    cluster_count = np.unique(cluster_labels)

    for label in cluster_count:
        cluster_indices = [i for i, cl_label in enumerate(cluster_labels) if cl_label == label]
        if len(cluster_indices) > 1:
            cluster = [nucleotides[i] for i in cluster_indices]
            new_distance_matrix = custom_distance_matrix(cluster)
            cluster_mean = np.mean(new_distance_matrix)
            variance += cluster_mean

    return variance

def breed_children(cluster_labels, nucleotides):
    distance_matrix = custom_distance_matrix(nucleotides)
    max_distance = 0
    parents = None

    # Compare sequences from different clusters to find the maximum distance
    for i in range(len(nucleotides)):
        for j in range(i + 1, len(nucleotides)):
            if cluster_labels[i] != cluster_labels[j] and distance_matrix[i][j] > max_distance:
                max_distance = distance_matrix[i][j]
                parents = (nucleotides[i], nucleotides[j])
    
    parent1, parent2 = parents

    for _ in range(3):
        child = ''.join([random.choice([el1, el2]) for el1, el2 in zip(parent1, parent2)])
        nucleotides.append(child)

def graph_results(Z):
    plt.figure(figsize=(10, 7))
    dendrogram(Z)
    plt.title('Dendrogram for Divisive Clustering')
    plt.xlabel('Specimen Index')
    plt.ylabel('Distance')
    plt.show()

'''
EXECUTION
'''

global nucleotides

def main():

    # preset data before iterating
    specimens = 20
    nucleotides = generate_nucleotide_sequences(specimens, 100)
    max_variance = 0
    max_iter = 5
    label_hist = []
    highest_var_iter = 0
    early_stopping = False

    for iter in range(max_iter):

        print('iteration:', iter + 1)

        distance_matrix = custom_distance_matrix(nucleotides)
        condensed_matrix = squareform(distance_matrix)
        Z = linkage(condensed_matrix, method='complete')
    
        # need to come up with a way to predefine how many clusters there should be
        cluster_labels = fcluster(Z, t=20, criterion='maxclust')
        label_hist.append(cluster_labels)

        if iter == 0:
            initial_variance = calculate_variance(cluster_labels, nucleotides)

        # if we do variance across clusters and then increase the number of clusters, the overall variance would decrease which is not ideal
        # we are presetting the number of clusters though
        variance = calculate_variance(cluster_labels, nucleotides)

        if variance > max_variance:
            max_variance = variance
            highest_var_iter = iter
        elif (max_variance - variance) < 0.001:
            # allow for two cases in which the max variance might not be reached
            if early_stopping:
                break
            else:
                early_stopping = True

        breed_children(cluster_labels, nucleotides)

    print('final nucleotides:', nucleotides)
    print('initial variance:', initial_variance)
    print('highest variance:', max_variance)
    print('highest variance iteration:', highest_var_iter + 1)
    # print('final cluster labels:', label_hist[highest_var_iter])
    graph_results(Z)

main()