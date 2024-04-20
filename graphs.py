# ////////// #
# GRAPHING   # 
# ////////// #
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def generate_color_list(size):
    cmap = LinearSegmentedColormap.from_list('red_to_blue', ['red', 'blue'])
    colors = [cmap(i / size) for i in range(size)]
    return colors

"""
def graph_benchmark(benchmark, project, num_iterations):
    num_genes = 10
    ind = np.arange(num_genes)  
    width = 0.05

    project = np.array(project)
    project_num_genes = project[:, :num_genes]

    bars = []
    for i in range(num_iterations):
        bars.append(plt.bar(ind+width*i, project_num_genes[i], width, color = 'r'))

    plt.xlabel("Genes") 
    plt.ylabel('Average Frequency') 
    plt.title("Cheetah Gene Frequencies") 
    plt.show() 
"""

def graph_benchmark(project1, project2, num_iterations):
    num_genes = 5
    ind = np.arange(num_genes)
    width = 0.1  # Adjust width for better spacing between subplots
    color_list = generate_color_list(num_iterations)

    project1 = np.array(project1)
    project2 = np.array(project2)
    project1_num_genes = project1[:, :num_genes]
    project2_num_genes = project2[:, :num_genes]

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Create a figure with two subplots

    # Plotting bars for project1 in the first subplot
    bars1 = []
    for i in range(num_iterations):
        bars1.append(axs[0].bar(ind + width * i, project1_num_genes[i], width, color=color_list[i]))

    axs[0].set_xlabel("Genes")
    axs[0].set_ylabel('Average Frequency')
    axs[0].set_title("Benchmark Frequencies")

    # Plotting bars for project2 in the second subplot
    bars2 = []
    for i in range(num_iterations):
        bars2.append(axs[1].bar(ind + width * i, project2_num_genes[i], width, color=color_list[i]))

    axs[1].set_xlabel("Genes")
    axs[1].set_ylabel('Average Frequency')
    axs[1].set_title("Project Frequencies")

    plt.tight_layout()  # Adjust subplot parameters to give enough space for labels
    plt.show()