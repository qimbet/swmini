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


    def __init__(self, rng, unit_instantiator):
        self.rng = rng
        self.map = None
        self.units = []
        self.players = []

        self.factory = unit_instantiator

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
    # Game state
    # ---------------------------

    def add_player(self, player):
        self.players.append(player)

    def load_army(self, player):
        self.units.extend(player.army.units)

    def place_army(self, player):
        deployment = DeploymentManager(
            self.map,
            rng=self.rng
        )
        deployment.deploy(player.army)

    def next_turn(self):
        self.turn_number += 1

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

        # reconstruct units here
        # using UnitFactory
