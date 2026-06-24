from src.map.edges import EdgeType
from src.map.tiles import Tile

def can_move(self, start, end):
    edge = self.get_edge(start, end)

    if edge is None:
        return True

    if edge.edge_type == EdgeType.WALL:
        return False

    if edge.edge_type in (
        EdgeType.DIAGONAL_NE,
        EdgeType.DIAGONAL_NW,
    ):
        return self.diagonal_allows_crossing(
            start,
            end,
            edge
        )

    return True

def can_end_turn(self, tile):
    if tile.has_diagonal_wall:
        return False

    if tile.type == "P":
        return False

    return True


def blocks_los(ray, diagonal):
    crossing = ray.intersects(diagonal)

    if not crossing:
        return False

    if ray.parallel_to(diagonal):
        return False

    return True