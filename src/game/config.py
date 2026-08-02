# src/game/config.py
import os
from pathlib import Path

ROOT_MARKER = ".gameroot"
def find_site_root(start: Path, rootMarker=".gameroot") -> Path:
    current = start.resolve()

    if current.is_file():
        current = current.parent

    while True:
        if (current / rootMarker).exists():
            return current
        if current.parent == current:
            raise FileNotFoundError(f"Could not locate '{rootMarker}'.")
        current = current.parent


PROJECT_ROOT =  find_site_root(Path(os.getcwd()), rootMarker=".gameroot")
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

print(f"project root: {PROJECT_ROOT}")

ASSETS_DIR= os.path.join(PROJECT_ROOT, "assets")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

MAP_OBJECTS = os.path.join('assets', "map_assets", "objects")
MAP_BACKGROUNDS = os.path.join('assets', "map_assets", "backgrounds")

ABILITIES    = os.path.join(DATA_DIR, "abilities")
ARMIES    = os.path.join(DATA_DIR, "armies")
MAPS_DIR = os.path.join(DATA_DIR, "maps")
UNITS    = os.path.join(DATA_DIR, "units")


CLASSES    = os.path.join(SRC_ROOT, "classes")
ENGINE    = os.path.join(SRC_ROOT, "engine")
GAME    = os.path.join(SRC_ROOT, "game")