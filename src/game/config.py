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
#PROJECT_ROOT = SRC_ROOT.parent
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

print(f"project root: {PROJECT_ROOT}")

ASSETS = os.path.join(PROJECT_ROOT, "assets")
MAPS_DIR = os.path.join(ASSETS, "maps")
MAP_OBJECTS = os.path.join(ASSETS, "map_assets", "objects")
MAP_BACKGROUNDS = os.path.join(ASSETS, "map_assets", "backgrounds")

ABILITIES    = os.path.join(SRC_ROOT, "abilities")
CLASSES    = os.path.join(SRC_ROOT, "classes")
DATA   = os.path.join(SRC_ROOT, "data")
ENGINE    = os.path.join(SRC_ROOT, "engine")
GAME    = os.path.join(SRC_ROOT, "game")
MAP    = os.path.join(SRC_ROOT, "map")
UNITS    = os.path.join(SRC_ROOT, "units")

