import numpy as np
from itertools import permutations


def check_size(sample):
    """
    Checks if the size of the sample is correct.
    """
    try:
        if np.shape(sample)[1] == 1:
            return sample, True
        else:
            return sample, False
    except:
        return sample, False


def check_mece(sample):
    """
    Checks if all elements in the sample are unique
    """
    if len(set(sample)) == len(sample):
        return sample, True
    else:
        return sample, False


def check_order(sample):
    """
    Checks if the order is correct. For our specific case, this means that even and odd numbers are split into two groups.
    Sample is converted to list of zeros and ones. We want that there is only one point where the 0s turn into 1s (or vice versa).
    """
    lst_mod = np.array(sample) % 2
    jumps = 0
    for i in range(len(lst_mod) - 1):
        if lst_mod[i] != lst_mod[i + 1]:
            jumps += 1
    if jumps == 1:
        return sample, True
    else:
        return sample, False


def fix_size(sample):
    corrections = []
    len_items = np.array([len(item) for item in sample])

    # The code is not made for sublists larger than 3
    if max(len_items) >= 3:
        print("Cannot find a fix for sample ", sample)
        return corrections

    idx_0 = np.where(len_items == 0)[0]
    idx_1 = np.where(len_items == 1)[0]
    idx_2 = np.where(len_items == 2)[0]

    # Remove doubles.
    # e.g. [[2,0], [0], [1]] -> [[2], [0], [1]]
    idxs = np.concatenate((idx_0, idx_1))
    items_without_2s = [
        item for sublst in [sample[idx] for idx in idxs] for item in sublst
    ]
    new_sample = list(sample)
    for i in idx_2:
        new_sample[i] = [x for x in new_sample[i] if x not in items_without_2s]

    # Recalculate
    len_items = np.array([len(item) for item in new_sample])
    idx_0 = np.where(len_items == 0)[0]
    idx_1 = np.where(len_items == 1)[0]
    idx_2 = np.where(len_items == 2)[0]

    if len(idx_0) > len(idx_2):
        print("Cannot find a fix for sample ", sample)
        return corrections
    elif len(idx_0) < len(idx_2):
        print("Cannot find a fix for sample ", sample)
        return corrections

    # Check if number of empty spots is equal to number of sublists with size 2.
    # If so, permute the items from sublists with size 2 over all sublsts of size 0 and 2.
    # e.g. [[2,0], [], [1]] -> [[2], [0], [1]] and [[0], [2], [1]]
    elif len(idx_0) == len(idx_2):
        sample = list(new_sample)
        idxs = np.concatenate((idx_0, idx_2))
        items = [[item] for sublst in [sample[idx] for idx in idx_2] for item in sublst]
        item_permutations = list(permutations(items))
        for permutation in item_permutations:
            new_sample = list(sample)  # copy original sample
            for i in range(len(permutation)):
                new_sample[idxs[i]] = permutation[i]
            corrections.append(new_sample)
    else:
        corrections.append(sample)

    return corrections


def fix_mece(sample):
    # e.g. [0,0,1] -> [2,0,1] or [0,2,1]
    corrections = []
    return corrections


def fix_order(sample):
    # only if #jumps == 2, e.g. [1,0,2,3] -> [1,3,0,2]
    corrections = []
    return corrections


def check_instances(solution_dict, fix=False):
    """
    Function that combines the checks and corrections (iff fix==True).
    - input: dictionary of solutions e.g. {'Sample 1': [[2],[0],[1]], 'Sample 2': ... }
    - output: same dictionary, but with "True" or "False" at the end of each solution, indicating if it is correct. e.g. {'Sample 1': [2,0,1,True], 'Sample 2': ... }
    if fix==True, also output a dictionary with possible corrections
        - 'Sample 1.s0', 'Sample 1.s1', ... indicate corrections from 'Sample 1' with an error in the size
        - 'Sample 1.m0', 'Sample 1.m1', ... indicate corrections from 'Sample 1' with an error in the uniqueness of the numbers
        - 'Sample 1.o0', 'Sample 1.o1', ... indicate corrections from 'Sample 1' with an error in the order
    """

    corrections_dict = {}

    for sample in solution_dict:
        solution = solution_dict[sample]

        # Check size: [[2],[0],[1]] is True, [[2,0],[0],[1]] is False
        solution, bool_size = check_size(solution)
        if bool_size == True:
            pass
        else:
            if fix == True:
                corrections = fix_size(solution)
                if len(corrections) == 0:
                    solution.append(bool_size)
                    solution_dict[sample] = solution
                    continue
                else:
                    for i in range(len(corrections)):
                        corrections_dict[sample + ".s{}".format(i)] = corrections[i]
                    continue
            else:
                solution.append(bool_size)
                solution_dict[sample] = solution
                continue

        # Flatten list: [[2],[0],[1]] -> [2,0,1]
        solution = [item for sublist in solution for item in sublist]

        # Check if all numbers occur once: [2,0,1] is True, [0,0,1] is False
        solution, bool_mece = check_mece(solution)
        if bool_mece == True:
            pass
        else:
            if fix == True:
                corrections = fix_mece(solution)
                if len(corrections) == 0:
                    solution.append(bool_mece)
                    solution_dict[sample] = solution
                    continue
                else:
                    for i in range(len(corrections)):
                        corrections_dict[sample + ".m{}".format(i)] = corrections[i]
                    continue
            else:
                solution.append(bool_mece)
                solution_dict[sample] = solution
                continue

        # Check if order is correct
        solution, bool_order = check_order(solution)
        if bool_order == True:
            pass
        else:
            if fix == True:
                corrections = fix_order(solution)
                if len(corrections) == 0:
                    solution.append(bool_mece)
                    solution_dict[sample] = solution
                    continue
                else:
                    for i in range(len(corrections)):
                        corrections_dict[sample + ".o{}".format(i)] = corrections[i]
                    continue
            else:
                solution.append(bool_order)
                solution_dict[sample] = solution
                continue

        solution.append(True)
        solution_dict[sample] = solution

    if fix == False:
        return solution_dict
    else:
        return solution_dict, corrections_dict


if __name__ == "__main__":
    # ------- Test dictionary -------
    test_dict = {}
    test_dict["Sample 1"] = [[2], [0], [1]]
    test_dict["Sample 2"] = [[2, 0], [0], [1]]
    test_dict["Sample 3"] = [[0], [0], [1]]
    test_dict["Sample 4"] = [[0], [1], [2]]

    # print(test_dict)
    # checked = check_instances(test_dict)
    # checked, corr = check_instances(test_dict, True)
    # print(checked)
    # print(corr)

    # ---- test fixes ---

    print(fix_size([[2, 0], [0], [1]]))
    print(fix_size([[2, 0], [], [1]]))
    print(fix_size([[2, 0], [1, 3], [1], []]))
    print(fix_size([[2, 0], [0], []]))
