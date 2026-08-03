import random
from pathlib import Path
from src.game.config import UNITS, MAPS_DIR

from src.classes.army import ArmyBuilder
from src.classes.players import Player
from src.classes.unit_instantiator import UnitInstantiator
from server.GameSession.GameState.mapManager import MapManager


def get_all_units(units_directory=UNITS):
    print(f"get_all_units(): units_directory: {units_directory}")

    unit_dir = Path(units_directory)
    return {
        path.stem: str(path)
        for path in unit_dir.glob("*.json")
    }


class Game:
    def __init__(self, seed=1234, map_file=None, unit_files=None, players=None):
        self.rng = random.Random(seed)
        self.factory = UnitInstantiator(unit_files or get_all_units())
        self.army_builder = ArmyBuilder(self.factory)
        self.map_manager = MapManager(rng=self.rng,)

        self.players = players or []


        if not map_file: #choose random map from dir if not specified
            maps = list(Path (MAPS_DIR).glob("*.json"))
            self.map_file =  str(random.choice(maps))
        else:
            self.map_file = map_file 

        self.running = False


    def create_armies(self):
        for player in self.players:
            player.army = self.army_builder.load_army(
                player.path_to_army,
                owner=player
            )
            player.assign_army(player.army)

    def setup(self):
        self.map_manager.load_map(self.map_file)

        for player in self.players:
            self.map_manager.add_player(player)
            player.army = self.army_builder.load_army(player.path_to_army, owner=player)

            self.map_manager.load_army(player)
            self.map_manager.place_army(player)

    # ---------------------------
    # Setup
    # ---------------------------
    def setup_map(self, map_file):
        self.map_manager.load_map(map_file)

    def add_player(self, player):
        self.map_manager.add_player(player)

    def load_armies(self):
        for player in self.map_manager.players:
            self.map_manager.load_army(player.path_to_army)

    def load_players(self, player_configs):
        for config in player_configs:
            player = Player(name=config["name"], army_file=config["army"])

            player.army = self.army_builder.load_army(player.army_file, player)
            self.players.append(player)

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