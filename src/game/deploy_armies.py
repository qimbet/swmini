import random


class DeploymentManager:
    def __init__(self, game_map, map_manager, rng=None):
        self.rng = rng or random.Random()
        self.map = game_map
        self.map_manager=map_manager

    def deploy(self, army, positions=None):
        for unit, position in zip(army.units, positions):
            if position is None:
                position = self.random_spawn()
            self.place_unit(unit, position)

    def place_unit(self, unit, position):
        x, y = position
        if not self.map_manager.can_place(x, y):
            return False

        unit.position = (x,y)
        self.units.append(unit)
        return True

    def random_spawn(self, width=5, side=0, clustering=0): #0-left, 1-top, 2-right, 3-bottom
        if side == 0:       # left
            x_range = (0, width - 1)
            y_range = (0, self.map.height - 1)
        elif side == 1:     # top
            x_range = (0, self.map.width - 1)
            y_range = (0, width - 1)
        elif side == 2:     # right
            x_range = (self.map.width - width, self.map.width - 1)
            y_range = (0, self.map.height - 1)
        elif side == 3:     # bottom
            x_range = (0, self.map.width - 1)
            y_range = (self.map.height - width, self.map.height - 1)

        else:
            raise ValueError(f"Invalid spawn side: {side}")

        for _ in range(150):
            x = self.rng.randint(*x_range)
            y = self.rng.randint(*y_range)
            if self.can_place(x, y):
                return (x, y)

        raise RuntimeError(
            f"Could not find spawn location on side {side}"
        )