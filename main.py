# /////////////////////////////// #
# STEP 0: VERIFY THE DATA EXISTS  #
# THE FILES IN DATA_GENERATION    #
# /////////////////////////////// # 


# STEPS
    # 0: make first-generation specimens
    # REPEAT 1-4 for i iterations, where 1 iteration = 2 years, aka 1 breeding cycle
    # 1: features.py
        # of the existing genes, which ones should we focus on improving?
        # genes to focus on = ones that have least amount of variance
    # 2: cluster.py
        # 
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


# VERSIONS TO TEST
    # version 1: 5 alleles per gene
    # version 2: varying number of genes


files = []
recovered_array = []
with open('cheetah-conservation/data_generation/specimens.txt', 'r') as file:
    for line in file:
        bases = [base for base in line.strip().split() if base.isalpha()]
        recovered_array.append(bases)

print(len(recovered_array))
print(recovered_array[0])