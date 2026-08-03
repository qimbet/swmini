import random


class DeploymentManager:
    def __init__(self, map_manager):
        self.rng = map_manager.rng or random.Random()
        self.map_manager=map_manager

    def deploy(self, army, side, positions=None):
        if positions is None:
            positions = [None] * len(army.units)
        for unit, position in zip(army.units, positions):
            if position is None:
                position = self.random_spawn(side=side)
            self.place_unit(unit, position)

    def place_unit(self, unit, position):
        if not self.map_manager.can_place(position):
            return False
        unit.position = position
        return True

    def random_spawn(self, width=5, side=0, clustering=0): #0-left, 1-top, 2-right, 3-bottom
        game_map = self.map_manager.map
        if side == 0:       # left
            x_range = (0, width - 1)
            y_range = (0, game_map.height - 1)
        elif side == 1:     # top
            x_range = (0, game_map.width - 1)
            y_range = (0, width - 1)
        elif side == 2:     # right
            x_range = (game_map.width - width, game_map.width - 1)
            y_range = (0, game_map.height - 1)
        elif side == 3:     # bottom
            x_range = (0, game_map.width - 1)
            y_range = (game_map.height - width, game_map.height - 1)

        else:
            raise ValueError(f"Invalid spawn side: {side}")

        for _ in range(150):
            x = self.rng.randint(*x_range)
            y = self.rng.randint(*y_range)
            if self.map_manager.can_place((x, y)):
                return (x, y)

        raise RuntimeError(
            f"Could not find spawn location on side {side}"
        )