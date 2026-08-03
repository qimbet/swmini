import json

from src.map.mapBuilder import GameMap
from src.game.deploy_armies import DeploymentManager


class MapManager:
    """
    Owns the current game state.

    Responsible for:
    - loading maps
    - loading and placing armies
    - tracking units
    - saving/loading state
    """


    def __init__(self, rng):
        self.rng = rng
        self.map = None
        self.units = []
        self.players = []


        self.turn_number = 0
        self.active_player = None


    # ---------------------------
    # Loading
    # ---------------------------
    def load_map(self, map_file):
        with open(map_file) as f:
            map_context = json.load(f)
        self.map = GameMap(map_context, rng=self.rng)

    # ---------------------------
    # Game setup
    # ---------------------------
    def add_player(self, player):
        self.players.append(player)

    def load_army(self, player):
        self.units.extend(player.army.units)

    def place_army(self, player):
        deployment = DeploymentManager(
            self,
            rng=self.rng
        )
        deployment.deploy(player.army)

    # ---------------------------
    # Game state
    # ---------------------------
    def next_turn(self):
        self.turn_number += 1

    def can_place(self, position, obstacle_types=("solid",)):
        x, y = position
        if not (
            0 <= x < self.map.width and
            0 <= y < self.map.height
        ):
            return False

        tile = self.map.tiles[y][x]

        for feature in tile.features:
            if any(
                tag in feature.tags
                for tag in obstacle_types
            ):
                return False

        if self.get_unit_at(position):
            return False
        return True

    def place_unit(self, unit, position):
        if not self.can_place(position):
            return False
        unit.position = position
        return True

    def build_map_symbol(self, x, y): #Renders symbol for a tile; combines terrain + units
        tile = self.map.tiles[y][x]
        
        terrain = tile.symbol() #Terrain
        unit = self.get_unit_at((x, y)) #Unit

        if unit:
            symbol = terrain + unit.symbol
        else:
            symbol = terrain
        return symbol[:3]

    def get_unit_at(self, position):
        for unit in self.units:
            if unit.position == position:
                return unit
        return None


    # ---------------------------
    # Serialization
    # ---------------------------

    def save(self, path):
        state = {
            "seed": self.seed,
            "turn": self.turn_number,
            "units": [
                unit.exportUnit()
                for unit in self.units
            ]
        }

        with open(path, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self, path):
        with open(path) as f:
            state = json.load(f)
        self.turn_number = state["turn"]

