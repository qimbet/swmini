from pathlib import Path
import json, random

from src.map.mapBuilder import GameMap
from src.game.deploy_armies import DeploymentManager
from src.classes.unit_instantiator import UnitInstantiator


class MapManager:
    """
    Owns the current game state.

    Responsible for:
    - loading maps
    - loading armies
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
        self.map = GameMap(map_context, seed=self.seed)


    def load_army(self, army_file):
        deployment = DeploymentManager(
            self.map,
            self.unit_instantiator,
            rng=self.rng
        )
        deployment.load_army(army_file)
        self.units.extend(deployment.units)


    # ---------------------------
    # Game state
    # ---------------------------

    def add_player(self, player):
        self.players.append(player)

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
