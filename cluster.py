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
import ast
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from scipy.spatial.distance import squareform
# from data_generation.data import synthetic_specimens



def generate_sequences(file_path):
    metadata, alleles = [], []
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    for datapoint in data:
        # Assuming the datapoint is a string like "['F', 6] ['BB', 'AB', 'CD']"
        parts = datapoint.split('] [')
        metadata_str = parts[0] + ']'
        alleles_str = '[' + parts[1]
        # Convert the string representations into Python lists
        metadata.append(ast.literal_eval(metadata_str))
        alleles.append(ast.literal_eval(alleles_str))
    return metadata, alleles
    


def custom_distance_matrix(alleles):
    # takes in the alleles and calculates the total number of alleles that differ
    matrix_size = len(alleles)
    distance_matrix = np.zeros((matrix_size, matrix_size))
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i != j:
                differences = sum(1 for a, b in zip(alleles[i], alleles[j]) if a != b)
                distance_matrix[i][j] = differences
    return distance_matrix



def parent_distance_matrix(metadata, alleles, cluster_labels):
    # compares each female to all males and returns the distance matrix
    matrix_size = len(alleles)
    females = [i for i in range(matrix_size) if metadata[i][0] == 'F']
    males = [j for j in range(matrix_size) if metadata[j][0] == 'M']
    distance_matrix = np.zeros((len(females), len(males)))
    for fi, f in enumerate(females):
        for mi, m in enumerate(males):
            if cluster_labels[f] != cluster_labels[m]:
                differences = sum(1 for a, b in zip(alleles[f], alleles[m]) if a != b)
                distance_matrix[fi][mi] = differences
    return distance_matrix



def calculate_variance(cluster_labels, alleles):
    variance = 0
    cluster_count = np.unique(cluster_labels)

    for label in cluster_count:
        cluster_indices = [i for i, cl_label in enumerate(cluster_labels) if cl_label == label]
        if len(cluster_indices) > 1:
            cluster = [alleles[i] for i in cluster_indices]
            new_distance_matrix = custom_distance_matrix(cluster)
            cluster_mean = np.mean(new_distance_matrix)
            variance += cluster_mean
    return variance



def update_age(metadata, alleles):
    for i in reversed(range(len(metadata))):
        metadata[i][1] += 2
        if metadata[i][0] == "F" and metadata[i][1] >= 10:
            metadata.pop(i)
            alleles.pop(i)
        elif metadata[i][0] == "M" and metadata[i][1] >= 10:
            metadata.pop(i)
            alleles.pop(i)



def punnett_square(allele1, allele2):
    square = []
    for allele1 in allele1:
        for allele2 in allele2:
            square.append(allele1 + allele2)
    return square



def breed_children(cluster_labels, metadata, alleles, parent_metadata, parent_alleles, iter):
    distance_matrix = custom_distance_matrix(alleles)
    max_distance = 0
    kids_metadata = []
    kids_alleles = []
    
    # Compare sequences from different clusters to find the maximum distance
    for i in range(len(alleles) - 1):
        for j in range(i + 1, len(alleles) - 2):
            # different groups, max distance, different gender
            if cluster_labels[i] != cluster_labels[j] and distance_matrix[i][j] > max_distance and metadata[i][0] != metadata[j][0]:
                max_distance = distance_matrix[i][j]
                parent1 = alleles[i]
                parent2 = alleles[j]

                for _ in range(4):
                    child = [random.choice(punnett_square(el1, el2)) for el1, el2 in zip(parent1, parent2)]
                    kids_metadata.append([random.choice(['F', 'M']), 2]) # we're updating it to 2 because in the next iteration/2 years they will be of breeding age
                    kids_alleles.append(child)

    metadata += kids_metadata
    alleles += kids_alleles
    
    return kids_metadata, kids_alleles, metadata, alleles


def breed_children_multiple_dads(cluster_labels, metadata, alleles, max_pairs=6, max_fathers=2, max_kids=2):
    distance_matrix = parent_distance_matrix(metadata, alleles, cluster_labels)
    results = []
    # top two males per female
    for fi, distances in enumerate(distance_matrix):
        if np.any(distances): 
            top_two_males = np.argpartition(distances, -2)[-2:]
            top_two_males_sorted = top_two_males[np.argsort(-distances[top_two_males])]
            cumulative = 0
            for mi in top_two_males_sorted:

                cumulative += distances[mi]

                results.append({
                    'female_index': fi,
                    'male_index': mi,
                    'distance': distances[mi],
                    'cumulative': 0 if cumulative == distances[mi] else cumulative
                })

    max_pair_results = sorted(results, key=lambda x: x['cumulative'], reverse=True)[:max_pairs]
    female_indices = set(result['female_index'] for result in max_pair_results)
    parent_indices = {}
    for female in female_indices:
        female_results = [result for result in results if result['female_index'] == female]
        top_two = sorted(female_results, key=lambda x: x['distance'], reverse=True)[:2]
        parent_indices[female] = [entry['male_index'] for entry in top_two]
    
    kids_metadata = []
    kids_alleles = []
            
    # breed children
    for key_m, val in parent_indices.items():
        mother = alleles[key_m]
        for key_f in range(max_fathers):
            for _ in range(max_kids):
                father = alleles[val[key_f]]
                child = [random.choice(punnett_square(mother, father)) for mother, father in zip(mother, father)]
                kids_metadata.append([random.choice(['F', 'M']), 2])
                kids_alleles.append(child)

    metadata += kids_metadata
    alleles += kids_alleles

    return kids_metadata, kids_alleles, metadata, alleles



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



def clustering(features, current_generation):
    print("Clustering")

    # preset data before iterating
    metadata, alleles = generate_sequences(features)
    general_metadata, general_alleles = generate_sequences(current_generation)

    max_variance = 0
    max_iter = 5
    parent_metadata = [(_, _) for _ in range(max_iter)]
    parent_alleles = [(_, _) for _ in range(max_iter)]
    label_hist = []
    highest_var_iter = 0
    early_stopping = False
    # number of specimens + children - deaths
    exp_specimens = 50 + 3 * max_iter - 1 * max_iter

    
    iter = 0
    # print('iteration:', iter + 1)

    distance_matrix = custom_distance_matrix(alleles)
    condensed_matrix = squareform(distance_matrix)
    Z = linkage(condensed_matrix, method='complete')

    cluster_labels = fcluster(Z, t=exp_specimens, criterion='maxclust')
    label_hist.append(cluster_labels)

    if iter == 0:
        initial_variance = calculate_variance(cluster_labels, alleles)

    variance = calculate_variance(cluster_labels, alleles)

    if variance > max_variance:
        max_variance = variance
        highest_var_iter = iter
    elif (max_variance - variance) < 0.001:
        # allow for two cases in which the max variance might not be reached
        if early_stopping:
            print("stop?")
        else:
            early_stopping = True

    update_age(general_metadata, general_alleles)
    kids_1, kids_2, result1, result2 = breed_children_multiple_dads(cluster_labels, general_metadata, general_alleles, parent_metadata, parent_alleles, iter)
    # result1, result2 = breed_children_multiple_dads(cluster_labels, general_metadata, general_alleles, parent_metadata, parent_alleles, iter)
    # Save to a file
    synthetic_specimens = [[e1, e2] for e1, e2 in zip(result1, result2)]
    
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(current_dir + '/specimens/current_generation.txt', 'w') as file:
        for sublist in synthetic_specimens:
            file.write(' '.join(map(str, sublist)) + '\n')

    return kids_1, kids_2