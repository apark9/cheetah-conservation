# //////////////////////////////////// #
# DO NOT RUN THIS MORE THAN ONCE       #
# TO SEE THE RESULTS, SEE SPECIMEN.TXT #
# //////////////////////////////////// #



# /////////////////////////////// #
# STEP 0: IMPORTS AND GLOBALS     #
# /////////////////////////////// #
import random



# /////////////////////////////// #
# STEP 1: GET THE ALIGNMENTS      #
# /////////////////////////////// #


# Open the input file
with open("cheetah-conservation/data_generation/alignment.txt", "r") as file:
    lines = file.readlines()
def extract_sequence(line):
    return line.split()[2]


# Initialize variables to store sequences
# subject = reference genome
# query = our specimen's sra
# Iterate through the lines to find and concatenate sequences
reference = []
specimen = []
for line in lines:
    if line.startswith("Query"):
        specimen.append(extract_sequence(line))
    elif line.startswith("Sbjct"):
        reference.append(extract_sequence(line))
specimen_full = "".join(specimen)
reference_full = "".join(reference)


# Cut down on size for ability of computation: we can increase this after proof of concept
specimen_full = specimen_full[:int(len(specimen_full) / 20)]
reference_full = reference_full[:int(len(reference_full) / 20)]


# Create another output variable for mismatches
# Check each sequence to populate it
mismatches = []
for i in range(len(reference_full)):
    if reference_full[i] != specimen_full[i]:
      # If the reference doesn't have data, then don't include that loci
      if reference_full[i] != "-":
        mismatches.append((i, reference_full[i]))
mismatches = mismatches[:-1]


# /////////////////////////////// #
# STEP 2: CREATE SYNTHETIC        #
# AND PUT INTO TEXT FILES         #
# /////////////////////////////// #


# Variables
num_specimens = 20
pairings = {"A" : "T", "T" : "A", "G" : "C", "C" : "G"}
synthetic_specimens = []


# Create data
for i in range(num_specimens):   
  new_specimen = []
  print(i)
  for mismatch in mismatches:
    nucleotide_1 = mismatch[1]
    nucleotide_2 = pairings[nucleotide_1]
    chosen_nucleotide = random.choices(population=[1, 2], weights=[0.8, 0.2],k=1)
    if chosen_nucleotide == 1: 
      new_specimen.append(nucleotide_1)
    else:
      new_specimen.append(nucleotide_2)
  synthetic_specimens.append(new_specimen)

# Save to a file
with open('cheetah-conservation/data_generation/specimens.txt', 'w') as file:
    for sublist in synthetic_specimens:
        file.write(' '.join(map(str, sublist)) + '\n')

