"""Graph dataset from the class lecture slide."""

NODES = [1, 2, 3, 4, 5, 6]

EDGES = [
    (1, 2),
    (1, 3),
    (3, 6),
    (4, 2),
    (4, 6),
    (6, 5),
]

POSITIVE_PATHS = [
    (1, 2),
    (1, 3),
    (1, 6),
    (1, 5),
    (3, 6),
    (3, 5),
    (4, 2),
    (4, 6),
    (4, 5),
    (6, 5),
]
