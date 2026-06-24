from enum import Enum, auto



WALL_TYPES = {
    "vertical": {
        "step": (0, 1),
        "edge": (1, 0),
    },
    "horizontal": {
        "step": (1, 0),
        "edge": (0, 1),
    },
    "diag_down": {
        "step": (1, 1),
        "edge": (1, 1),
    },
    "diag_up": {
        "step": (1, -1),
        "edge": (1, -1),
    },
}


class EdgeType(Enum):
    BASIS_WALL = auto()
    DIAGONAL_NE = auto()   # /
    DIAGONAL_NW = auto()   # \

class Edge:
    def __init__(self, edge_type):
        self.edge_type = edge_type

    def blocks_movement(self):
        return True
    
    def is_diagonal(self):
        return self.edge_type in {
            EdgeType.DIAGONAL_NE,
            EdgeType.DIAGONAL_NW
        }