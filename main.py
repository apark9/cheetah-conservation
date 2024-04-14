# /////////////////////////////// #
# STEP 0: VERIFY THE DATA EXISTS  #
# THE FILES IN DATA_GENERATION    #
# /////////////////////////////// # 
import os

from features import *
from cluster import *
from benchmark import *
from pairing import *


# MAIN FILE STEPS
    # 0: make first-generation specimens
    # REPEAT 1-4 for i iterations, where 1 iteration = 2 years, aka 1 breeding cycle
    # 1: features.py
        # of the existing genes, which ones should we focus on improving?
        # genes to focus on = ones that have least amount of variance
        # OUTPUT: list of specimens but only the genes that matter
    # 2: cluster.py
        # 
        # OUTPUT: list of specimens but only the genes that matter
    # 3:
    # 4:


# WHAT ALL VERSIONS OF OUR TESTS WILL HAVE IN COMMON
    # SPECIMENS
    # first generation = 50 specimens, 25 F 25 M of ages 2-6
    # each specimen has 100 genes
    # each gene will have __ number of alleles/variations, displayed in alphabetical notation
    # for a specific gene, a specimen will have 2 copies of alleles, for ex gene 1 may look like "AB" for that specimen

    # AGE
    # each iteration, age will increase by 2
    # if age is >= 8, remove from breeding pool (too old)


# DIFFERENT VERSIONS TO TEST
    # version 1: constant 5 alleles per gene
    # version 2: varying number of genes
    # version 3: try to optimize the # of features (what is the best # of features to focus on for a given number of genes?)


# FOR TESTING PURPOSES
num_iterations = 5
genes_to_consider = 10


# FOR BENCHMARK PURPOSES
benchmark_results = []
project_results = []


current_dir = os.path.dirname(os.path.abspath(__file__))
first_generation = open(current_dir + '/data_generation/specimens.txt', 'r')
current_generation = first_generation


for i in range(num_iterations):
    features(current_generation, genes_to_consider)
    clustering() # modify prints so that the current_generation file is updated
        # clusters
        # pairs
        # breeds

    part_4_benchmark, part_4_project = benchmark()
    benchmark_results.append(part_4_benchmark)
    project_results.append(part_4_project)


# TO-DO:
    # functions
    # benchmark

