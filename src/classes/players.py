class Player:
    def __init__(
        self,
        name,
        faction,
        path_to_army,
        side,
    ):

        self.name = name
        self.faction = faction
        self.army = None
        self.path_to_army = path_to_army
        self.side = side

        # Runtime state
        self.units = []

    def assign_army(self, army):
        self.army=army


    def export(self): #save player data.
        return {
            "name": self.name,
            "faction": self.faction,
            "path_to_army": self.path_to_army,
            "side": self.side,
            "units": self.units,
        }


    def __repr__(self):
        return (
            f"Player("
            f"name={self.name}, "
            f"faction={self.faction}, "
            f"side={self.side}"
            f")"
        )