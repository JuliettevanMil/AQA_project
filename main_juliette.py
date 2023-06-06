import numpy as np
from QUBO_formulation import define_qubo, distance_cols, distance_rows, total_meas_eff, qubo_to_dict, index_rev
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import networkx as nx
import dwave.inspector

import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt

input_matrix = np.array([[1, 0, 1], 
                         [0, 0, 0], 
                         [1, 0, 1]])

# Q_row = define_qubo(input_matrix, distance_rows, np.shape(input_matrix)[0], 1)
Q_col = define_qubo(input_matrix, distance_cols, np.shape(input_matrix)[1], 2)

#print(Q_col)

### Total measure of effectiveness example
matrix1 = np.array(
    [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
    ]
)
matrix2 = np.array(
    [
        [1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
    ]
)
print(total_meas_eff(matrix1))
print(total_meas_eff(matrix2))

Q = qubo_to_dict(Q_col, 3)
#print(Q)

# ------- Run our QUBO on the QPU -------
# Set up QPU parameters
chainstrength = 8
numruns = 10

# Run the QUBO on the solver from your config file
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               chain_strength=chainstrength,
                               num_reads=numruns,
                               label='Try - Clustering')

dwave.inspector.show(response)

# ------- Print results to user -------
print('-' * 60)
print('{:>15s}{:>15s}{:^15s}{:^15s}'.format('Set 0','Set 1','Set 2','Energy'))
print('-' * 60)
for sample, E in response.data(fields=['sample','energy']):
    set_ones = [k for k,v in sample.items() if v == 1]
    set_idx = [index_rev(i,3) for i in set_ones]
    S0 = [p for i,p in set_idx if i==0]
    S1 = [p for i,p in set_idx if i==1]
    S2 = [p for i,p in set_idx if i==2]
    print('{:>15s}{:>15s}{:^15s}{:^15s}'.format(str(S0),str(S1),str(S2),str(E)))

# ------- Display results to user -------
# Grab best result
# Note: "best" result is the result with the lowest energy
# Note2: the look up table (lut) is a dictionary, where the key is the node index
#   and the value is the set label. For example, lut[5] = 1, indicates that
#   node 5 is in set 1 (S1).
lut = response.first.sample
print(lut)

# Interpret best result in terms of nodes and edges
# S0 = [node for node in G.nodes if not lut[node]]
# S1 = [node for node in G.nodes if lut[node]]
# cut_edges = [(u, v) for u, v in G.edges if lut[u]!=lut[v]]
# uncut_edges = [(u, v) for u, v in G.edges if lut[u]==lut[v]]

# Display best result
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos, nodelist=S0, node_color='r')
# nx.draw_networkx_nodes(G, pos, nodelist=S1, node_color='c')
# nx.draw_networkx_edges(G, pos, edgelist=cut_edges, style='dashdot', alpha=0.5, width=3)
# nx.draw_networkx_edges(G, pos, edgelist=uncut_edges, style='solid', width=3)
# nx.draw_networkx_labels(G, pos)

# filename = "maxcut_plot.png"
# plt.savefig(filename, bbox_inches='tight')
# print("\nYour plot is saved to {}".format(filename))