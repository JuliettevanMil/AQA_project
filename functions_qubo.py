import numpy as np
from collections import defaultdict


def distance_rows(A, r, s, scale_func, val):
    """
    Calculate the distance between rows r and s for matrix A.
    """
    d = 0
    for j in range(np.shape(A)[0]):
        d -= 2 * A[r, j] * A[s, j]

    return scale_func(d, val)


def distance_cols(A, r, s, scale_func, val):
    """
    Calculate the distance between columns r and s for matrix A.
    """
    d = 0
    for k in range(np.shape(A)[1]):
        d -= 2 * A[k, r] * A[k, s]

    return scale_func(d, val)


def scale_id(d, dummy):
    return d


def scale_th(d, th):
    if d <= th:  # distance is negative
        return -1
    else:
        return 0


def scale_lin(d, max_val):
    return d / max_val


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


def define_qubo(A, distance_func, num_V, alpha, beta, scale="id"):
    Q = np.zeros((num_V * num_V, num_V * num_V))

    if scale == "linear":
        scale_func = scale_lin
        val = num_V  # in our case, the max value is num_V. So to scale it, only num_V is required. However, dividing by 2*num_V holds for the general case.
    elif scale == "treshold":
        scale_func = scale_th
        val = -num_V  # this treshold works for our case
    else:
        scale_func = scale_id
        val = 0

    # H_obj
    for p in range(num_V - 1):
        for i in range(num_V):
            for j in range(num_V):
                Q[index(i, p, num_V), index(j, p + 1, num_V)] += distance_func(
                    A, i, j, scale_func, val
                )
                Q[index(j, p + 1, num_V), index(i, p, num_V)] += distance_func(
                    A, j, i, scale_func, val
                )

    # H_rc
    for p in range(num_V):
        for i in range(num_V):
            Q[index(i, p, num_V), index(i, p, num_V)] -= alpha
            for j in range(i + 1, num_V):
                Q[index(i, p, num_V), index(j, p, num_V)] += beta

    # H_path
    for i in range(num_V):
        for p in range(num_V):
            Q[index(i, p, num_V), index(i, p, num_V)] -= alpha
            for q in range(p + 1, num_V):
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
    set_ones = [1, 3, 6, 8]
    set_idx = [index_rev(i, 3) for i in set_ones]

    input_matrix = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    input_matrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]])

    alpha = 0
    beta = 0

    print(
        define_qubo(
            input_matrix,
            distance_cols,
            np.shape(input_matrix)[1],
            alpha,
            beta,
            scale="treshold",
        )
    )

    # Q_row = define_qubo(input_matrix, distance_rows, np.shape(input_matrix)[0], alpha, beta)
    # Q_col = define_qubo(input_matrix, distance_cols, np.shape(input_matrix)[1], alpha, beta)

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
    # print(total_meas_eff(matrix1))
    # print(total_meas_eff(matrix2))
