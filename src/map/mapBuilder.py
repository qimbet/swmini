
import random, json, os
from collections import deque

from src.game.config import MAPS_DIR
from src.map.edges import *
from src.map.tiles import *


def load_layout(mapPath=None):
    if not mapPath:
        mapPath = os.path.join(MAPS_DIR, "test_map.json")
    with open(mapPath, "r") as f:
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
    def __init__(self, mapContext, rng=None, max_attempts=5, reserved_positions=None):
        self.rng = rng if rng else random.Random(rng) 

        mapSize = mapContext.get("base")
        if mapSize is None:
            raise KeyError("mapContext missing 'base' key")

        self.width = mapSize.get("width")
        self.height = mapSize.get("height")

        if not (self.height or self.width): 
            raise ValueError("Problem when loading map size. Exiting...")

        self.placed_obstacles = [] #encodes position for randomly-placed objects
        self.spawn_parameters = mapContext.get("spawn_parameters")
        self.featureData = mapContext.get("features", {})

        self.reserved_positions = { 
                tuple(position) 
                for position in mapContext.get("reserved_positions", []) 
            } 

        if reserved_positions: 
            self.reserved_positions.update( 
                tuple(position) 
                for position in reserved_positions 
                )


        for retryCount in range(1, max_attempts + 1):
            self.tiles = [
                [Tile() for _ in range(self.width)]
                for _ in range(self.height)
            ]
            self.edges = {}

            try:
                self.generate_features(self.featureData)
                break
            except(ValueError, RuntimeError) as error:
                print(f"Map generation failed! failure: {retryCount}/{max_attempts}\nERROR: {error}")
                if retryCount > max_attempts:
                    raise RuntimeError(
                        f"Could not build a valid map after {max_attempts} tries"
                    ) from error

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

    def _place_fixed_obstacles(self, obstaclesData):
        for obstacleType, instances in obstaclesData.items():
            feature_cls = FEATURE_REGISTRY.get(obstacleType)
            if not feature_cls:
                continue  

            for instance in instances:
                if instance["position"] is None:
                    continue
                w = instance["width"]
                l = instance["length"]
                x0, y0 = instance["position"]

                self._place_area(
                    feature_cls,
                    x0, y0,
                    w, l
                )

    def _place_random_obstacles(self, obstaclesData, attempts=100):
        for obstacleType, instances in obstaclesData.items():
            feature_cls = FEATURE_REGISTRY.get(obstacleType)
            if not feature_cls:
                continue  

            for instance in instances:
                if instance["position"] is not None:
                    continue
                w = instance["width"]
                l = instance["length"]

                if w > self.width or l > self.height: #naming clash between map layout and obstacle layout
                    raise ValueError( 
                            f"Obstacle {obstacleType} " 
                            f"({w}x{l}) is larger than map " 
                            f"({self.width}x{self.length})" 
                        )
            
                for _ in range(attempts):
                    x0 = self.rng.randint(0, self.width - w)
                    y0 = self.rng.randint(0, self.height - l)
                    if not self._obstacle_can_fit(x0, y0, w, l):
                        continue

                    # Temporarily place it, check connectivity
                    self._place_area(feature_cls, x0, y0, w, l)
                    if self.is_connected():
                        break

                    # Roll back on failure
                    for y in range(y0, y0 + l):
                        for x in range(x0, x0 + w):
                            tile = self.tiles[y][x]
                        
                            tile.features = [
                                feature
                                for feature in tile.features
                                if not isinstance(feature, feature_cls)
                            ]

                else:  
                    raise RuntimeError(
                        f"Could not place non-dividing {obstacleType}")

    def _place_fixed_walls(self, wallsData):
        for orientation, walls in wallsData.items():
            step_x, step_y = WALL_TYPES[orientation]["step"]
            edge_x, edge_y = WALL_TYPES[orientation]["edge"]
            edge_type = WALL_EDGE_TYPE[orientation]

            for wall in walls:
                if wall["position"] is None:
                    continue

                length = wall["length"]
                pos = wall["position"]
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
                        (x,y),
                        (x + edge_x, y + edge_y),
                        edge_type
                    )

    def _place_random_walls(self, wallsData, attempts=100):
        for orientation, walls in wallsData.items():
            step_x, step_y = WALL_TYPES[orientation]["step"]
            edge_x, edge_y = WALL_TYPES[orientation]["edge"]
            edge_type = WALL_EDGE_TYPE[orientation]

            for wall in walls:
                if wall["position"] is not None:
                    continue
                length = wall["length"]

                for _ in range(attempts):
                    x0 = self.rng.randint(0, self.width - 1)
                    y0 = self.rng.randint(0, self.height - 1)

                    if not self._wall_fits(x0, y0, length, step_x, step_y):
                        continue

                    candidate_edges = []

                    for i in range(length):
                        x = x0 + i * step_x
                        y = y0 + i * step_y

                        a = (x, y)
                        b = (x + edge_x, y + edge_y)

                        candidate_edges.append(
                            (a, b, edge_type)
                        )

                    # Temporarily add the wall.
                    for a, b, edge_type in candidate_edges:
                        self.add_wall(a, b, edge_type)

                    # Reject it if it divides the walkable map.
                    if self.is_connected():
                        break
                    else:
                        for a, b, _ in candidate_edges:
                            self.edges.pop(frozenset((a, b)), None)

                    raise RuntimeError(
                        f"Could not place non-dividing random wall "
                        f"orientation='{orientation}', length={length}"
                    )
                else:
                    raise RuntimeError(
                        f"Could not place non-dividing " 
                        f"random wall " 
                        f"orientation='{orientation}', " 
                        f"length={length}")

    def _obstacle_can_fit(self, x0, y0, w, h):
        if x0 < 0 or y0 < 0:
            return False

        if x0 + w > self.width:
            return False

        if y0 + h > self.height:
            return False

        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                #check if another obstacle already occupies tile
                if self.tiles[y][x].features:
                    print("Tile already occupied")
                    return False
        return True

    def _walkable(self, x, y):
        """Return True if a tile can be traversed."""
        return not self._is_solid(x, y)

    def _neighbors(self, x, y):
        """Yield cardinally adjacent cells that can potentially be traversed."""
        directions = (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        )

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            # A wall between the two cells blocks movement.
            if self.get_edge((x, y), (nx, ny)):
                continue

            if not self._walkable(nx, ny):
                continue

            yield nx, ny

    def is_connected(self):
        """
        Return True if all walkable tiles belong to one connected region.
        """

        walkable = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self._walkable(x, y)
        }

        if not walkable:
            return True

        start = next(iter(walkable))

        visited = {start}
        queue = deque([start])

        while queue:
            x, y = queue.popleft()

            for nx, ny in self._neighbors(x, y):
                position = (nx, ny)

                if position not in visited:
                    visited.add(position)
                    queue.append(position)

        return visited == walkable
    #endregion     --------------------------------------------------


    def add_wall(self, a, b, edge_type=EdgeType.BASIS_WALL):
        key = frozenset((a, b))
        self.edges[key] = Edge(edge_type)

    def get_edge(self, cell_a, cell_b):
        return self.edges.get(
            frozenset((cell_a, cell_b))
        )

    def generate_features(self, mapContextData):
        obstaclesData = mapContextData.get("obstacles", {})
        wallsData = mapContextData.get("walls", {})

        self._place_random_walls(wallsData)
        self._place_random_obstacles(obstaclesData)

        self._place_fixed_walls(wallsData)
        self._place_fixed_obstacles(obstaclesData)

        self._build_obstacle_enclosures()

    def display(self, symbol_provider=None):
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row = "|"

            for x in range(self.width):
                if symbol_provider:
                    symbol = symbol_provider(x,y)
                else:
                    symbol = self.tiles[y][x].symbol()

                row += f"{symbol:<3}" #aw <3

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

    def export(self, path):
        data = {
            "width": self.width,
            "height": self.height,
            "tiles": [
                [tile.type for tile in row]
                for row in self.tiles
            ],
            "edges": [
                {
                    "a": list(a),
                    "b": list(b)
                }
                for (a, b) in self.edges
            ]
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2)




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    main(seed=args.seed)