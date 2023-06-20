import numpy as np
from functions_qubo import (
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


import matplotlib

matplotlib.use("agg")
from matplotlib import pyplot as plt

input_matrix = np.array(
    [
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1],
    ]
)
# input_matrix = np.array([[1, 0, 1, 0, 1],
#                          [0, 1, 0, 1, 0],
#                          [1, 0, 1, 0, 1],
#                          [0, 1, 0, 1, 0],
#                          [1, 0, 1, 0, 1]])
# input_matrix = np.array([[1,0,1,0],
#                          [0,1,0,1],
#                          [1,0,1,0],
#                          [0,1,0,1]])
# input_matrix = np.array([[1, 0, 1],
#                          [0, 1, 0],
#                          [1, 0, 1]])
# input_matrix = np.array([[0, 0],
#  [0, 0]])
# print(np.triu(input_matrix))
num_V = np.shape(input_matrix)[1]
alpha = 1  # reward
beta = 4  # penalty

# Q_row = define_qubo(input_matrix, distance_rows, np.shape(input_matrix)[0], 1)
Q_col = define_qubo(input_matrix, distance_cols, num_V, alpha, beta)

# print(Q_col)

Q = qubo_to_dict(Q_col, num_V)
# print(Q)

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

dwave.inspector.show(response)

# ------- Print results to user -------
print("-" * 60)
print(
    "{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}{:^15s}".format(
        "Column 0",
        "Column 1",
        "Column 2",
        "Column 3",
        "Column 4",
        "Column 5",
        "Column 6",
        "Energy",
    )
)
print("-" * 60)
for sample, E in response.data(fields=["sample", "energy"]):
    set_ones = [k for k, v in sample.items() if v == 1]
    set_idx = [index_rev(i, num_V) for i in set_ones]
    S0 = [p for i, p in set_idx if i == 0]
    S1 = [p for i, p in set_idx if i == 1]
    S2 = [p for i, p in set_idx if i == 2]
    S3 = [p for i, p in set_idx if i == 3]
    S4 = [p for i, p in set_idx if i == 4]
    S5 = [p for i, p in set_idx if i == 5]
    S6 = [p for i, p in set_idx if i == 6]
    print(
        "{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}{:>15s}{:^15s}".format(
            str(S0), str(S1), str(S2), str(S3), str(S4), str(S5), str(S6), str(E)
        )
    )

lut = response.first.sample
# print(lut)
