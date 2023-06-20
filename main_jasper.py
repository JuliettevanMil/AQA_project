# ------- Import functions -------
import numpy as np
from matplotlib import pyplot as plt

from QUBO_formulation import (
    define_qubo,
    distance_cols,
    distance_rows,
    total_meas_eff,
    qubo_to_dict,
    index_rev,
)
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import networkx as nx
import dwave.inspector
from functools import partial
from dwave.embedding.chain_strength import uniform_torque_compensation


# ------- Print results to user -------
def print_results(data, num_V):
    """
    Print the results in columns.
    Input data should be response.data(fields=["sample", "energy"])
    """
    # Header
    print("-" * 15 * (num_V + 1))
    header = ["Column {}".format(i) for i in range(num_V)]
    header.append("Energy")
    header_format = "{:>" + str(15) + "s}"
    header_format *= num_V + 1
    print(header_format.format(*header))
    print("-" * 15 * (num_V + 1))

    # Data
    for sample, E in data:
        set_ones = [k for k, v in sample.items() if v == 1]
        set_idx = [index_rev(i, num_V) for i in set_ones]

        S = [[] for _ in range(num_V)]
        for i, p in set_idx:
            if 0 <= i < num_V:
                S[i].append(p)

        S_strings = [str(s) for s in S]

        print(header_format.format(*S_strings, str(E)))

    return


def read_samples(samples_dict, num_V):
    """
    - input: list of samples in term of a dictionary
    - output: solution dictionary each solution is in terms of columns
    """
    sample_num = 0
    solution_dict = {}
    for sample in samples_dict:
        sample_num += 1
        set_ones = [k for k, v in sample.items() if v == 1]
        set_idx = [index_rev(i, num_V) for i in set_ones]

        S = [[] for _ in range(num_V)]
        for i, p in set_idx:
            if 0 <= i < num_V:
                S[i].append(p)

        solution_dict["Sample {}".format(sample_num)] = S

    return solution_dict


def find_solution(input_matrix, alpha, beta, cluster_dim="col", show_results=False):
    """
    Input:
    - input matrix
    - Distance function + scaled

    Generates QUBO and solves it using DWAVE

    Output:
    - ourcomes with lowest energy
    """
    num_V = np.shape(input_matrix)[1]

    # ------- Define QUBO -------
    if cluster_dim == "col":
        Q_col = define_qubo(input_matrix, distance_cols, num_V, alpha, beta)
        Q = qubo_to_dict(Q_col, num_V)
    elif cluster_dim == "row":
        Q_row = define_qubo(input_matrix, distance_rows, num_V, alpha, beta)
        Q = qubo_to_dict(Q_row, num_V)
    else:
        raise ValueError(
            "Dimension to cluster on is not determined or unknown. Choose cluster_dim from ['col', 'row']."
        )

    # ------- Run our QUBO on the QPU -------
    # Set up QPU parameters
    chainstrength = 8
    chain_strength = partial(uniform_torque_compensation, prefactor=1.5)  # up to 2
    numruns = 10

    # Run the QUBO on the solver from your config file
    sampler = EmbeddingComposite(DWaveSampler())
    response = sampler.sample_qubo(
        Q, chain_strength=chain_strength, num_reads=numruns, label="Try - Clustering"
    )

    # ------- Show results -------
    if show_results == True:
        print_results(response.data(fields=["sample", "energy"]), num_V)

    # ------- Find lowest energy and corresponding samples -------
    lowest_energy = response.first.energy
    lowest_energy_samples = []
    for sample in response.data(["sample", "energy"]):
        if sample.energy == lowest_energy:
            lowest_energy_samples.append(sample.sample)

    solution_dict = read_samples(lowest_energy_samples, num_V)

    return solution_dict, lowest_energy


# ------- Check and correct results -------
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
