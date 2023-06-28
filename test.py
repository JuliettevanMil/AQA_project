dct = {
    "Sample 1": {".o0": [0, 2, 1, 3, True], ".o1": [0, 2, 1, 3, True]},
    "Sample 3": {".s0": [2, 0, 3, 1, True]},
    "Sample 4": {".n0": [3, 1, 2, 0, True]},
}
for sample in dct:
    for item in dct[sample]:
        if item[1] == "n" or item[1] == "s":
            print(1)
        else:
            print(2)
