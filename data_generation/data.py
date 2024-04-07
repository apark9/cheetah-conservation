# //////////////////////////////////// #
# DO NOT RUN THIS MORE THAN ONCE       #
# TO SEE THE RESULTS, SEE SPECIMEN.TXT #
# //////////////////////////////////// #

'''
HIGH-LEVEL NOTES
'''
# 1: we have a reference genome of a health cheetah
# 2: we take one specific specimen from 


# /////////////////////////////// #
# STEP 0: IMPORTS AND GLOBALS     #
# /////////////////////////////// #
import random

gene_size = 150
num_genes = 100
last_gene_size = 177
reference = []
specimen = []
nucleotide_alleles_per_gene = []
letter_alleles_per_gene = []      
allele_distributions = []           # IMPORTANT FOR SARAH: WHICH DISTRIBUTIONS ARE REALLY BAD AKA FOCUS ON?

# /////////////////////////////// #
# STEP 1: GET THE ALIGNMENTS      #
# /////////////////////////////// #


# OPEN ALIGNMENT FILE
with open("cheetah-conservation/data_generation/D2_Alignment.txt", "r") as file:
    lines = file.readlines()
def extract_sequence(line):
    return line.split()[2]


# GRAB THE SEQUENCE
  # Initialize variables to store sequences
  # subject = reference genome
  # query = our specimen's sra
  # Iterate through the lines to find and concatenate sequences
for line in lines:
    if line.startswith("Query"):
        specimen.append(extract_sequence(line))
    elif line.startswith("Sbjct"):
        reference.append(extract_sequence(line))
specimen_full = "".join(specimen)
reference_full = "".join(reference)


# RESIZE THE SEQUENCE
  # cut down on size for ability of computation: we can increase this after proof of concept
  # 15,027
specimen_full = specimen_full[:int(len(specimen_full) / 244)]
reference_full = reference_full[:int(len(reference_full) / 244)]


# FIND ALL MISMATCHES AND THEIR INDICES BETWEEN THE SEQUENCES
  # Create another output variable for mismatches
  # Check each sequence to populate it
mismatches_indices = []
nucleotides = []
for i in range(len(reference_full)):
    if reference_full[i] != specimen_full[i]:
      # If the reference doesn't have data, then don't include that loci
      if reference_full[i] != "-":
        mismatches_indices.append((i, reference_full[i]))
        nucleotides.append(reference_full[i])
mismatches_indices = mismatches_indices[:-1]
nucleotides = nucleotides[:-1]


# BREAK UP MISMATCHES INTO GENES
  # WLOG, let there be 100 genes each having 150 nucloetides that can change
genes = [''.join(nucleotides[i:i + gene_size]) for i in range(0, len(nucleotides) - last_gene_size, gene_size)]
genes.append(nucleotides[-last_gene_size:])


# FOR EACH GENE, DETERMINE ITS ALLELES
  # WLOG, let each gene have 2 variances of it, which are chosen from a random sampling of the original mismatch
  # the code is set up to allow for easy manipulation of more than 2 variances.  you just change the line that says CAN CHANGE
  # index i = alleles possible for gene i
def mutate_sequence(seq):
    seq_list = list(seq)
    mutations = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    dont_rechoose = []
    for _ in range(10):
       i = random.randint(0, len(seq) - 1)
       if i not in dont_rechoose:
          dont_rechoose.append(i)
          seq_list[i] = mutations.get(seq[i])
    return ''.join(seq_list)

for i in range(len(genes)):
  single_gene_alleles = []
  j = 0
  number_alleles = random.randint(2, 10) # CAN CHANGE
  while j < number_alleles:
    new_seq = mutate_sequence(genes[i])
    if new_seq not in single_gene_alleles:
        single_gene_alleles.append(new_seq)
        j += 1
  nucleotide_alleles_per_gene.append(single_gene_alleles)

# MAKE PSEUDO-ALLELE NAMES FOR THESE SEQUENCES
def number_to_alphabet_list(num):
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  return list(alphabet[:num])

for alleles in nucleotide_alleles_per_gene:
  num_alleles = len(alleles)
  pseudo_alleles = number_to_alphabet_list(num_alleles)
  letter_alleles_per_gene.append(pseudo_alleles)


# /////////////////////////////// #
# STEP 2: CREATE SYNTHETIC        #
# AND PUT INTO TEXT FILES         #
# /////////////////////////////// #


# VARIABLES
num_specimens = 50
pairings = {"A" : "T", "T" : "A", "G" : "C", "C" : "G"}
synthetic_specimens = []
genes = []


# FUNCTIONS
def skewed_distribution(num_items, skewness_factor):
    distribution = []
    # Generate a random distribution with values between 0 and 1
    for _ in range(num_items):
        value = random.random()
        distribution.append(value)
    
    # Sort the distribution in descending order
    distribution.sort(reverse=True)
    
    # Apply skewness by adjusting the values
    for i in range(num_items):
        distribution[i] = distribution[i] ** skewness_factor
    
    # Normalize the distribution to ensure the values add up to 1
    total = sum(distribution)
    distribution = [round(item / total, 2) for item in distribution]
    return distribution

def choose_allele(letters, probabilities):
  choice = random.random()
  cumulative_prob = 0
  for allele, prob in zip(letters, probabilities):
      cumulative_prob += prob
      if choice < cumulative_prob:
          return allele
  return letters[-1] 

# CREATE SPECIMEN
for i in range(num_specimens):   
  metadata = []
  alleles = []
  new_specimen = []

  # METADATA
  if i < 25:
     metadata.append("F")
  else:
     metadata.append("M")
  age = random.randint(2, 6) # our first batch of cheetahs should be young
  metadata.append(age)

  # ALLELES
    # we want alleles to be initially skewed towards very low variance, aka one gene dominating
  for gene in range(num_genes):
    # with 80% probability it is skewed, otherwise 20%
    if random.random() < 0.8:
      distribution = skewed_distribution(len(letter_alleles_per_gene[gene]), 4) # more skewed
    else:
       distribution = skewed_distribution(len(letter_alleles_per_gene[gene]), 0.2) # less skewed
    allele_distributions.append(distribution)

    letters = letter_alleles_per_gene[gene]
    allele_1 = choose_allele(letters, distribution)
    allele_2 = choose_allele(letters, distribution)
    
    combined = allele_1 + allele_2
    alleles.append(combined)
  
  new_specimen = [metadata, alleles]
  synthetic_specimens.append(new_specimen)

# Save to a file
with open('cheetah-conservation/data_generation/specimens.txt', 'w') as file:
    for sublist in synthetic_specimens:
        file.write(' '.join(map(str, sublist)) + '\n')

