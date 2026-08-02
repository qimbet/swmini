import random
from pathlib import Path
from config import UNITS

from src.classes.unit_instantiator import UnitInstantiator
from server.GameSession.GameState.mapManager import MapManager


def get_all_units(units_directory=UNITS):
    unit_dir = Path(units_directory)
    return {
        path.stem: str(path)
        for path in unit_dir.glob("**.json")
    }


class Game:
    def __init__(
        self,
        seed=None,
        map_file=None,
        unit_files=get_all_units(),
        players=None
    ):
        self.seed = seed if seed else 1234
        self.rng = random.Random(seed)

        self.factory = UnitInstantiator(unit_files)
        self.map_manager = MapManager(
            rng=self.rng,
            unit_instantiator=self.factory
        )

        self.players = players or []
        self.map_file = map_file
        self.running = False


    def setup(self):
        self.map_manager.load_map(self.map_file)
        for player in self.players:
            self.map_manager.add_player(player)


    # ---------------------------
    # Setup
    # ---------------------------
    def setup_map(self, map_file):
        self.map_manager.load_map(map_file)

    def add_player(self, player):
        self.map_manager.add_player(player)

    def load_armies(self):
        for player in self.map_manager.players:
            self.map_manager.load_army(
                player.army_file,
                side=player.side
            )


    # ---------------------------
    # Game loop
    # ---------------------------
    def start(self):
        self.setup()
        self.load_armies()

        self.running = True
        while self.running:
            self.run_turn()
            #orchestrate turn cycle here


    def run_turn(self):
        print(f"Turn {self.map_manager.turn_number}")
        active_player = (self.map_manager.active_player)

        # Future:
        # - player input
        # - AI decisions
        # - movement
        # - combat
        # - cleanup
        self.map_manager.next_turn()


    def stop(self):
        self.running = False


    # ---------------------------
    # Utilities
    # ---------------------------
    def display(self):
        self.map_manager.map.display()