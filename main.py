# /////////////////////////////// #
# STEP 0: VERIFY THE DATA EXISTS  #
# THE FILES IN DATA_GENERATION    #
# /////////////////////////////// # 



files = []


recovered_array = []
with open('cheetah-conservation/data_generation/specimens.txt', 'r') as file:
    for line in file:
        bases = [base for base in line.strip().split() if base.isalpha()]
        recovered_array.append(bases)

print(len(recovered_array))
print(recovered_array[0])