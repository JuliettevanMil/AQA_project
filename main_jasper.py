import numpy as np
from functions_dwave import find_solution


if __name__ == "__main__":
    # ------- Initialization -------
    input_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    input_matrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])
    output_matrix = np.array([[1, 1, 0], [1, 1, 0], [0, 0, 1]])

    num_V = np.shape(input_matrix)[1]
    alpha = 1  # reward
    beta = 4  # penalty

    # ------- Solution -------
    # solution_dict, lowest_energy = find_solution(input_matrix, alpha, beta)
    # print(solution_dict)
    # print(check_instances(solution_dict))
