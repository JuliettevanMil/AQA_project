import numpy as np
from functions_dwave import find_solution
from check_and_correct import check_instances

input_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
alpha = 1  # reward
beta = 4  # penalty

solution_dict, lowest_energy = find_solution(
    input_matrix, alpha, beta, show_results=False
)
print(solution_dict)
print(check_instances(solution_dict))
