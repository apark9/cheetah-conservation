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

'''
TO FIGURE OUT LATER
'''
# understand HiPart / DePDDP
# have to figure out how to merge parents, how do we select two specific datapoints to merge?

# IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import random
from HiPart.clustering import DePDDP
# from sklearn.datasets import make_blobs
# from data_generation.data import synthetic_specimens

'''
SYNTHETIC DATASET
- take in a set of nucleotide sequences
- convert to binary encoding
'''
# want to generate nucleotides (gene reference) for multiple cheetahs
def generate_nucleotide_sequences(num_sequences, sequence_length):
    nucleotides = ['A', 'C', 'G', 'T']
    sequences = [''.join([random.choice(nucleotides) for _ in range(sequence_length)]) 
                 for _ in range(num_sequences)]
    return sequences

def binary_conversion(nucleotide_sequence):
    binary_map = {'A': [0, 0], 'C': [0, 1], 'G': [1, 0], 'T': [1, 1]}
    return [bit for nucleotide in nucleotide_sequence for bit in binary_map[nucleotide]]

def graph_results(clustered_class, X):
    plt.scatter([x[0] for x in X], [x[1] for x in X], c=clustered_class)
    plt.title('Divisive Clustering Results')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

'''
EXECUTION
'''

def main():

    specimens = 10

    # nucleotides = generate_nucleotide_sequences(specimens, 10)
    # print('random nucleotides: ', nucleotides)   
    # X = np.array([binary_conversion(seq) for seq in nucleotides])
    # print('binary converted data: ', X)

    '''
    preset synthetic data for testing
    '''

    nucleotides = ['TCTTTGCTAA', 'CAGCTAACAG', 'GGTAGAGATT', 'TCTTTTTCCG', 'AGTACCAGGT', 'CCATCTCCAC', 'CAATTTGAAA', 'GAGTGCCCGA', 'CCTAAACCGC', 'GATGGAAATT']
    X = np.array([binary_conversion(seq) for seq in nucleotides])

    # need to see if there's an empirical way to test max_clusters_number, otherwise just setting it equal to the highest value where the cluster class doesn't change
    clustered_class = DePDDP(max_clusters_number=3).fit_predict(X)
    print('clustered_class: ', clustered_class)
    graph_results(clustered_class, X)

main()