# src/game/config.py
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SRC_ROOT.parent

ASSETS = PROJECT_ROOT / "assets"

ABILITIES    = SRC_ROOT / "abilities"
CLASSES    = SRC_ROOT / "classes"
DATA   = SRC_ROOT / "data"
ENGINE    = SRC_ROOT / "engine"
GAME    = SRC_ROOT / "game"
MAP    = SRC_ROOT / "map"
UNITS    = SRC_ROOT / "units"
