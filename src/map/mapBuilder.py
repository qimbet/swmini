
import random, json
from src.game.config import ASSETS, MAPS_DIR
from src.map.edges import *
from src.map.tiles import *


def load_layout():
    path = MAPS_DIR / "mapLayout.json"
    with open(path, "r") as f:
        return json.load(f)
    
def main(seed=None):
    layout = load_layout()

    game_map = GameMap(layout)

    if seed is not None:
        random.seed(seed)

    game_map.display()

FEATURE_REGISTRY = {
    "solid_obstacle": SolidObstacle,
    "light_cover": LightCover,
    "dense_cover": DenseCover,
    "shallow_pit": ShallowPit,
    "pit": Pit,
}

WALL_EDGE_TYPE = {
    "vertical": EdgeType.BASIS_WALL,
    "horizontal": EdgeType.BASIS_WALL,
    "diag_down": EdgeType.DIAGONAL_NE,
    "diag_up": EdgeType.DIAGONAL_NW,
}

class GameMap:
    def __init__(self, mapContext, seed=None):
        self.rng = random.Random(seed)
        mapSize = mapContext.get("base")
        if mapSize is None:
            raise KeyError("mapContext missing 'base' key")

        self.width = mapSize.get("width", None)
        self.height = mapSize.get("height", None)

        if not (self.height and self.width): 
            raise ValueError("Problem when loading map size. Exiting...")

        self.tiles = [
            [Tile() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.edges = {}
        self.placed_obstacles = [] #encodes position for randomly-placed objects

        featureData = mapContext.get("features", {})
        self.generate_features(featureData)

    #region helper functions    -------------------------------------

    def _is_solid(self, x, y):
        return any("solid" in f.tags for f in self.tiles[y][x].features)

    def _wall_fits(self, x0, y0, length, step_x, step_y):
        x1 = x0 + step_x * (length - 1)
        y1 = y0 + step_y * (length - 1)

        return (
            0 <= x0 < self.width and
            0 <= y0 < self.height and
            0 <= x1 < self.width and
            0 <= y1 < self.height
        )

    def _place_area(self, feature_cls, x0, y0, w, h):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x].add(feature_cls())

    def _build_obstacle_enclosures(self):
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]

        for y in range(self.height):
            for x in range(self.width):

                if not self._is_solid(x, y):
                    continue

                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy

                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        self.add_wall((x,y), (nx,ny), EdgeType.BASIS_WALL)
                        continue

                    if not self._is_solid(nx, ny):
                        self.add_wall((x,y), (nx,ny), EdgeType.BASIS_WALL)

    def _place_obstacles(self, obstaclesData):
        for obstacleType, instances in obstaclesData.items():
            feature_cls = FEATURE_REGISTRY.get(obstacleType)
            if not feature_cls:
                continue  

            for instance in instances:
                w = instance["width"]
                l = instance["length"]
                if instance["position"] is not None:
                    x0, y0 = instance["position"]

                else:
                    for _ in range(100):
                        x0 = self.rng.randint(0, self.width - w)
                        y0 = self.rng.randint(0, self.height - l)

                        if self._obstacle_can_fit(x0, y0, w, l):
                            break
                    else:
                        raise RuntimeError(
                            f"Could not place {obstacleType}"
                        )

                self._place_area(feature_cls, x0, y0, w, l)

    def _place_walls(self, wallsData):
        for orientation, walls in wallsData.items():
            step_x, step_y = WALL_TYPES[orientation]["step"]
            edge_x, edge_y = WALL_TYPES[orientation]["edge"]
            edge_type = WALL_EDGE_TYPE[orientation]

            for wall in walls:
                length = wall["length"]
                pos = wall["position"]

                if pos is None:
                    while True:
                        x0 = self.rng.randint(0, self.width - 1)
                        y0 = self.rng.randint(0, self.height - 1)
                        if self._wall_fits(x0, y0, length, step_x, step_y):
                            break
                else:
                    x0, y0 = pos
                    if not self._wall_fits(x0, y0, length, step_x, step_y):
                        raise ValueError(
                            f"Wall at {(x0, y0)} length={length} "
                            f"orientation='{orientation}' extends outside map"
                        )

                for i in range(length):
                    x = x0 + i * step_x
                    y = y0 + i * step_y

                    self.add_wall(
                        (x, y),
                        (x + edge_x, y + edge_y),
                        edge_type
                    )

    def _obstacle_can_fit(self, x0, y0, w, h):
        if x0 < 0 or y0 < 0:
            return False

        if x0 + w > self.width:
            return False

        if y0 + h > self.height:
            return False

        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):

                # another obstacle already occupies tile
                if self.tiles[y][x].features:
                    return False

                # any wall touching this tile
                neighbors = (
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                )

                for nx, ny in neighbors:
                    if self.get_edge((x, y), (nx, ny)):
                        return False

        return True

    #endregion     --------------------------------------------------


    def add_wall(self, a, b, edge_type=EdgeType.BASIS_WALL):
        key = frozenset((a, b))
        self.edges[key] = Edge(edge_type)

    def get_edge(self, cell_a, cell_b):
        return self.edges.get(
            frozenset((cell_a, cell_b))
        )

    def generate_features(self, mapContextData):
        wallsData = mapContextData.get("walls", {})
        self._place_walls(wallsData)

        obstaclesData = mapContextData.get("obstacles", {})
        self._place_obstacles(obstaclesData)
        self._build_obstacle_enclosures()


    def display(self):
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row = "|"

            for x in range(self.width):
                row += f" {self.tiles[y][x].symbol()} "
                if x < self.width - 1:
                    edge = self.get_edge(
                        (x, y),
                        (x + 1, y)
                    )
                    row += "|" if edge else " "
                else:
                    row += "|"

            print(row)
            border = "+"

            for x in range(self.width):

                if y < self.height - 1:
                    edge = self.get_edge(
                        (x, y),
                        (x, y + 1)
                    )
                    border += "---+" if edge else "   +"
                else:
                    border += "---+"

            print(border)





if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    main(seed=args.seed)