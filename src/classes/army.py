import json

class Army:
    def __init__(self, owner, faction):
        self.owner = owner
        self.faction = faction
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)


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

        for entry in data["units"]:
            unit_type = entry["type"]

            count = len(entry["position"])
            for _ in range(count):
                unit = self.factory.create(
                    faction=data["faction"],
                    unit_type=unit_type,
                    owner=owner
                )
                army.add_unit(unit)

        return army