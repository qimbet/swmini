
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

        featureData = mapContext.get("features", {})
        self.generate_features(featureData)


    def add_wall(self, a, b, edge_type=EdgeType.BASIS_WALL):
        key = frozenset((a, b))
        self.edges[key] = Edge(edge_type)

    def get_edge(self, cell_a, cell_b):
        return self.edges.get(
            frozenset((cell_a, cell_b))
        )

    def _place_area(self, feature_cls, x0, y0, w, h):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x].add(feature_cls())

    def generate_features(self, mapContextData):
        #region walls
        wallsData = mapContextData.get("walls", {})
        for orientation, walls in wallsData.items():
            step_x, step_y = WALL_TYPES[orientation]["step"]
            edge_x, edge_y = WALL_TYPES[orientation]["edge"]
            edge_type = WALL_EDGE_TYPE[orientation]

            for wall in walls:
                length = wall["length"]
                pos = wall["position"]

                if pos is None:
                    x0 = self.rng.randint(0, self.width - 1)
                    y0 = self.rng.randint(0, self.height - 1)
                else:
                    x0, y0 = pos

                x1 = x0 + step_x * (length - 1) #compute endpoints (optional)
                y1 = y0 + step_y * (length - 1)

                for i in range(length):
                    x = x0 + i * step_x
                    y = y0 + i * step_y

                    if not (0 <= x < self.width and 0 <= y < self.height):
                        continue  # or break / raise depending on strictness

                    self.add_wall(
                        (x, y),
                        (x + edge_x, y + edge_y),
                        edge_type
                    )
        #endregion


        #region features
        obstaclesData = mapContextData.get("obstacles", {})
        for obstacleType, instances in obstaclesData.items():
            feature_cls = FEATURE_REGISTRY.get(obstacleType)
            if not feature_cls:
                continue  

            for instance in instances:
                w = instance["width"]
                l = instance["length"]
                x0, y0 = instance["position"] or (
                    self.rng.randint(0, self.width - 1),
                    self.rng.randint(0, self.height - 1),
                )

                self._place_area(feature_cls, x0, y0, w, l)

        #endregion

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