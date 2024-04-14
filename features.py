import pandas as pd
import numpy as np


iter = 0

genes_to_consider = 10


def remove_brackets(value):
    return value.replace('[', '').replace(']', '').replace(',', '').replace('\'', '')


data = pd.read_csv('data_generation/specimens.txt', sep=" ", header=None)

data = data.applymap(remove_brackets)

df = data.iloc[:, 2:]


#get frequency of each unique val in series
def calculate_frequency(series):
    return series.value_counts()

#apply function to each column
frequency_data = df.apply(calculate_frequency).fillna(0)

#calculate variance of frequencies for each column
variance_of_frequencies = frequency_data.var()

#sort the columns based on variance of frequencies and get the sorted indexes
sorted_column_indexes = variance_of_frequencies.sort_values().index

#get the first N genes of lowest variance (that we want to consider)
indexes_of_genes_to_consider = sorted_column_indexes[0:genes_to_consider]
print("gene indexes to use:")
print(indexes_of_genes_to_consider)

#readd m/f & age
idx1 = pd.Index([0])
idx2 = pd.Index([1])
indexes_of_genes_to_consider = indexes_of_genes_to_consider.union(idx1).union(idx2)


#print final data to consider for clustering :)
final_data = data.iloc[:, indexes_of_genes_to_consider]
print(final_data)

final_data.to_csv("pandas_features_selected/"+str(iter)+".csv")

indexes_of_genes_to_consider = indexes_of_genes_to_consider[2:]

f = open("features_selected/"+str(iter)+".txt", "w")
for index, row in final_data.iterrows():
    f.write('['+row[0]+','+row[1]+']')
    f.write('[')
    firstRound = True
    for i in range(len(indexes_of_genes_to_consider)):
        if firstRound == False:
            f.write(',')
        f.write(row[indexes_of_genes_to_consider[i]])
        firstRound = False
    f.write(']')
    f.write('\n')
f.close()




# ['F', 6] ['BB', 'BA', 'DC', 'BA', 'GE’]