import json
from src.classes.character_scaffold import Unit, Footprint


class UnitInstantiator:
    def __init__(self, character_files):
        self.database = {}
        self._next_unit_id = 0

        for faction, path in character_files.items(): #upload all faction entities
            with open(path) as f:
                self.database[faction] = json.load(f) #lookup by [faction][name]

    def _get_next_unit_id(self):
        unit_id = self._next_unit_id
        self._next_unit_id += 1
        return unit_id

    def create(self, faction, unit_type, owner):
        raw_data = self.database[faction][unit_type]

        footprintData = raw_data['footprint']
        footprint = Footprint(
            width=footprintData['width'],
            length=footprintData['length']
        )

        unitData = raw_data.copy()
        unitData['footprint'] = footprint

        unitData.pop("unit_id", None)
        unitData.pop("owner", None)

        unit_id = self._get_next_unit_id()


        return Unit(**unitData, owner=owner, unit_id=unit_id)