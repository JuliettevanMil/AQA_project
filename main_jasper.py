import numpy as np
from functions_dwave import find_solution
from check_and_correct import check_instances


if __name__ == "__main__":
    input_matrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])
    alpha = 1
    beta = 3

    solution_dict, lowest_energy = find_solution(
        input_matrix,
        alpha,
        beta,
        cluster_dim="col",  # choose from ["col", "row"]
        scale="treshold",  # choose from ["linear","treshold","id"]
        show_results=False,  # choose from [True, False]
    )
    # checked = check_instances(solution_dict, fix=False)
    checked, checked_corrections = check_instances(solution_dict, fix=True)

    num_correct = 0
    for sample in checked:
        if checked[sample][-1] == True:
            num_correct += 1
    print(checked, num_correct)

    num_correct = 0
    for sample in checked_corrections:
        for correction in checked_corrections[sample]:
            if checked_corrections[sample][correction][-1] == True:
                num_correct += 1
                break
    print(checked_corrections, num_correct)
