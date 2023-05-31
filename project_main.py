import numpy as np
from collections import defaultdict

def distance(i, j):
    d = i + j
    return d

def index(i, p):
    idx = i * num_V + p
    return idx

num_V = 3
alpha = 1

Q = np.zeros((num_V*num_V,num_V*num_V))

# H_obj
for p in range(num_V-1):
    for i in range(num_V):
        for j in range(num_V):
            Q[index(i,p),index(j,p+1)] += distance(i,j)
            Q[index(j,p+1),index(i,p)] += distance(j,i)

# H_hor
for p in range(num_V):
    for i in range(num_V):
        Q[index(i,p),index(i,p)] += -2 * alpha
        for j in range(i, num_V):
            Q[index(i,p),index(j,p)] += alpha

# H_ver
for i in range(num_V):
    for p in range(num_V):
        Q[index(i,p),index(i,p)] += -2 * alpha
        for q in range(p, num_V):
            Q[index(i,p),index(i,q)] += alpha

Q_dict = defaultdict(int)
Q_dict_fake = np.zeros((num_V*num_V,num_V*num_V))
for i in range(num_V*num_V):
    for j in range(i, num_V*num_V):
        Q_dict[(i,j)] = Q[i,j]
        Q_dict_fake[i,j] = Q[i,j]

print(Q_dict_fake)



