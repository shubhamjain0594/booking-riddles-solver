"""Points for the various parties."""

"""
Now for every feature 'i',
has say strength S_i and it decreases by say D_i every step,
until it reaches a threshold T_i, and after F_i steps it becomes 0
"""
POINTS = [
    (-45, 1, 4),  # bug
    (15, 5, None),  # snippet nearer to me than opponent
    (10, 4, None),  # weapon
    (-45, 1, 4),  # opponent with weapon but I don't
    (8, 3, None)   # opponent without weapon but I have
]
