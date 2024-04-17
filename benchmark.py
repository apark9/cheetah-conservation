
# /////////// #
# BENCHMARK   # 
# /////////// #
import os
import ast
import random
from collections import Counter
from cluster import *


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



def pair_random(shorter, larger, random_pairings):
    for specimen in shorter:
        other_specimen = random.choice(larger)
        larger.remove(other_specimen)
        random_pairings.append([specimen, other_specimen])
    return random_pairings

def punnett_square(allele1, allele2):
    square = []
    for allele1 in allele1:
        for allele2 in allele2:
            square.append(allele1 + allele2)
    return square


def breed_children(pairings, alleles, metadata):
    kids_metadata = []
    kids_alleles = []
    for pair in pairings:
        parent1 = alleles[pair[0]]
        parent2 = alleles[pair[1]]
        for _ in range(3):
            child = [random.choice(punnett_square(el1, el2)) for el1, el2 in zip(parent1, parent2)]
            kids_metadata.append([random.choice(['F', 'M']), 0]) # we're updating it to 2 because in the next iteration/2 years they will be of breeding age
            kids_alleles.append(child)
    metadata += kids_metadata
    alleles += kids_alleles
    return metadata, alleles


def random_generation(file_path):

    # RANDOM BENCHMARK
    # get indices of the specimens from the metadata
    metadata, alleles = generate_sequences(file_path)
    females = []
    males = []
    for i in range(len(metadata)):
        if metadata[i][0] == "F":
            females.append(i)
        else:
            males.append(i)

    # pairings are indices so like metadata[1] and metadata[3]
    shorter = females if len(females) < len(males) else males
    larger = females if len(females) >= len(males) else males
    pairings = pair_random(shorter, larger, [])
    metadata, alleles = breed_children(pairings, alleles, metadata)
    update_age(metadata, alleles)

    # Save to a file
    synthetic_specimens = [[e1, e2] for e1, e2 in zip(metadata, alleles)]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(current_dir + '/specimens/random_generation.txt', 'w') as file:
        for sublist in synthetic_specimens:
            file.write(' '.join(map(str, sublist)) + '\n')
    return alleles


def compute_variance(alleles):
    variances = []
    num_entries = len(alleles[0])

    
    
    for i in range(num_entries - 1):
        one_allele_all_specimens = []
        for j in range(len(alleles) - 1):   
            one_allele_all_specimens.append(alleles[j][i])
        
        # now
        vocabulary = set(one_allele_all_specimens)
        counts = Counter(one_allele_all_specimens)

        frequencies = [round(counts[value] / len(one_allele_all_specimens), 2) for value in vocabulary]
        bottleneck_frequency = max(frequencies)
        variances.append(bottleneck_frequency)
    
    return variances
            



def benchmark(file_path_random, file_path_current):
    print("Benchmark")

    # get the benchmark = random plus the current generation
    random_alleles = random_generation(file_path_random)
    _, current_alleles = generate_sequences(file_path_current)

    # compute variance of random and current
    variance_random = compute_variance(random_alleles)
    variance_current = compute_variance(current_alleles)
    return variance_random, variance_current

    
