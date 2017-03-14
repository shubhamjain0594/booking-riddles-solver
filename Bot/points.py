"""Points for the various parties."""

"""
Now for every feature 'i',
has say strength S_i and it decreases by say D_i every step,
until it reaches a threshold T_i, and after F_i steps it becomes 0
"""
POINTS = [
    (-30, 7, -1, 5),  # bug
    (20, -0.5, 1, 30),  # snippet nearer to me than opponent
    (15, -0.5, 1, 30),  # weapon
    (-30, 7, -1, 5),  # opponent with weapon but I don't
    (15, -3, 1, 7)   # opponent without weapon but I have
]
