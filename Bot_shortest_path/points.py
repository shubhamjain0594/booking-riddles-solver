"""Points for the various parties."""

"""
Now for every feature 'i',
has say strength S_i and it decreases by say D_i every step,
until it reaches a threshold T_i, and after F_i steps it becomes 0
"""
POINTS = [
    (-30, 3, -1, 15),  # bug
    (10, -0.5, 1, 20),  # snippet nearer to me than opponent
    (10, -1, 1, 20),  # weapon
    (-30, 5, -1, 7),  # opponent with weapon but I don't
    (10, -2, 1, 10)   # opponent without weapon but I have
]
