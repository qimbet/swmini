import json
from pathlib import Path

from src.classes.character_scaffold import Unit


class UnitInstantiator:
    def __init__(self, character_file):
        with open(character_file) as f:
            self.database = json.load(f)


    def create(self, unit_type):
        data = self.database[unit_type]
        return Unit(**data)