import numpy as np
from functions_dwave import find_solution
from check_and_correct import check_instances

input_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
input_matrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])

alpha = 1  # reward
beta = 4  # penalty

solution_dict, lowest_energy = find_solution(
    input_matrix,
    alpha,
    beta,
    cluster_dim="col",  # choose from ["col", "row"]
    scale="id",  # choose from ["linear","treshold","id"]
    show_results=False,  # choose from [True, False]
)
print(solution_dict)
print(check_instances(solution_dict))
