import numpy as np
from collections import defaultdict


def distance_rows(A, r, s):
    """
    Calculate the distance between rows r and s for matrix A.
    """
    d = 0
    for j in range(np.shape(A)[0]):
        d -= 2 * A[r, j] * A[s, j]

    return d 


def distance_cols(A, r, s):
    """
    Calculate the distance between columns r and s for matrix A.
    """
    d = 0
    for k in range(np.shape(A)[1]):
        d -= 2 * A[k, r] * A[k, s]

    return d / np.shape(A)[0]


def total_meas_eff(A):
    """
    Calculate the total measure of effectiveness for matrix A.
    """
    TME = 0
    for i in range(np.shape(A)[1] - 1):
        TME -= distance_cols(A, i, i + 1)

    for j in range(np.shape(A)[0] - 1):
        TME -= distance_rows(A, j, j + 1)

    return TME


def index(i, p, num_V):
    idx = i * num_V + p
    return idx


def index_rev(idx, num_V):
    i = idx // num_V
    p = idx % num_V
    return i, p


def define_qubo(A, distance_func, num_V, alpha, beta):
    Q = np.zeros((num_V * num_V, num_V * num_V))

    # H_obj
    for p in range(num_V - 1):
        for i in range(num_V):
            for j in range(num_V):
                Q[index(i, p, num_V), index(j, p + 1, num_V)] += distance_func(A, i, j)
                Q[index(j, p + 1, num_V), index(i, p, num_V)] += distance_func(A, j, i)            

    # H_rc
    for p in range(num_V):
        for i in range(num_V):
            Q[index(i, p, num_V), index(i, p, num_V)] -= alpha
            for j in range(i+1, num_V):
                Q[index(i, p, num_V), index(j, p, num_V)] += beta

    # H_path
    for i in range(num_V):
        for p in range(num_V):
            Q[index(i, p, num_V), index(i, p, num_V)] -= alpha
            for q in range(p+1, num_V):
                Q[index(i, p, num_V), index(i, q, num_V)] += beta
    
    Q = np.triu(Q)
    
    return Q


def qubo_to_dict(Q, num_V):
    Q_dict = defaultdict(int)
    for i in range(num_V * num_V):
        for j in range(num_V * num_V):
            Q_dict[(i, j)] = Q[i, j]

    return Q_dict


if __name__ == "__main__":
    set_ones = [1,3,6,8]
    set_idx = [index_rev(i,3) for i in set_ones]
    print(set_idx)
    
    
    input_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

    # Q_row = define_qubo(input_matrix, distance_rows, np.shape(input_matrix)[0], 1)
    Q_col = define_qubo(input_matrix, distance_cols, np.shape(input_matrix)[1], 1)

    print(Q_col)

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
    #print(total_meas_eff(matrix1))
    #print(total_meas_eff(matrix2))
