
import os

from random import Random
from src.classes.unit_instantiator import UnitInstantiator
from src.game.deploy_armies import DeploymentManager
from src.map.mapBuilder import GameMap, load_layout
from src.game.config import *


rng = Random()
factory = UnitInstantiator("src/data/rebel/characters.json")

mapPath = os.path.join(MAPS_DIR, "mapLayout.json")

layout = load_layout(mapPath=mapPath)
game_map = GameMap(layout)
#game_map.display()

deployment = DeploymentManager(
    game_map,
    factory,
    rng=rng
)


deployment.load_army(
    "assets/armies/rebel_default.json"
)