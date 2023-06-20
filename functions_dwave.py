import numpy as np
from functions_qubo import (
    define_qubo,
    qubo_to_dict,
    distance_cols,
    distance_rows,
    index_rev,
)
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from functools import partial
from dwave.embedding.chain_strength import uniform_torque_compensation
import dwave.inspector  # --> dwave.inspector.show(response)


def print_results(response, num_V):
    """
    Print the results in columns.
    Input response should be from dwave.
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
    for sample, E in response.data(fields=["sample", "energy"]):
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


def find_solution(
    input_matrix, alpha, beta, cluster_dim="col", scale="id", show_results=False
):
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
        Q_col = define_qubo(input_matrix, distance_cols, num_V, alpha, beta, scale)
        Q = qubo_to_dict(Q_col, num_V)
    elif cluster_dim == "row":
        Q_row = define_qubo(input_matrix, distance_rows, num_V, alpha, beta, scale)
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
        print_results(response, num_V)

    # ------- Find lowest energy and corresponding samples -------
    lowest_energy = response.first.energy
    lowest_energy_samples = []
    for sample in response.data(["sample", "energy"]):
        if sample.energy == lowest_energy:
            lowest_energy_samples.append(sample.sample)

    solution_dict = read_samples(lowest_energy_samples, num_V)

    return solution_dict, lowest_energy
