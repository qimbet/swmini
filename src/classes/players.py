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
        self.path_to_army = path_to_army
        self.side = side

        # Runtime state
        self.units = []


    def add_unit(self, unit):
        self.units.append(unit)


    def export(self):
        """
        Used for saving player data.
        """
        return {
            "name": self.name,
            "faction": self.faction,
            "path_to_army": self.path_to_army,
            "side": self.side,
            "ranking": self.ranking,
            "winrate_overall": self.winrate_overall,
            "winrate_faction": self.winrate_faction
        }


    def __repr__(self):
        return (
            f"Player("
            f"name={self.name}, "
            f"faction={self.faction}, "
            f"side={self.side}"
            f")"
        )