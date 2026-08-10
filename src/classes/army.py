from dataclasses import dataclass
import json

@dataclass
class ArmyUnit:
    unit: object
    start_position: tuple | None = None

class Army:
    def __init__(self, owner, faction):
        self.owner = owner
        self.faction = faction
        self.units = []

    def add_unit(self, unit, position=None):
        self.units.append(
            ArmyUnit(
                unit=unit, start_position=position
            )
        )


class ArmyBuilder:
    def __init__(self, unit_instantiator):
        self.factory = unit_instantiator

    def load_army(self, path, owner):
        with open(path) as f:
            data = json.load(f)

        army = Army(
            owner=owner,
            faction=data["faction"]
        )

        for entry in data["units"]: #type of unit
            unit_type = entry["type"]
            positionList = entry["position"] #define number of units by placement

            for unit_position in positionList:

                unit = self.factory.create(
                    faction=data["faction"],
                    unit_type=unit_type,
                    owner=owner, 
                )
                army.add_unit(unit, unit_position)

        return army