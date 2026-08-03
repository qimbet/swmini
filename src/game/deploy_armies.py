import random


class DeploymentManager:
    def __init__(self, game_map, rng=None):
        self.rng = rng or random.Random()
        self.map = game_map

    def deploy(self, army, positions=None):
        for unit, position in zip(army.units, positions):
            if position is None:
                position = self.random_spawn()

            self.place_unit(unit, position)


    def place_unit(self, unit, position):
        x, y = position
        if not self.can_place(x, y):
            return False

        unit.position = (x,y)
        self.units.append(unit)
        return True



    def can_place(self, x, y, obstacleTypes=["solid"], phasing=False): #return True if ALL OF 'obstacleTypes' tags are present in space
        # outside map
        if not (
            0 <= x < self.map.width and
            0 <= y < self.map.height
        ):
            print(f"Cannot place unit outside map!")
            return False


        tile = self.map.tiles[y][x]

        # specified obstacle
        if any(
            any(tag in feature.tags for tag in obstacleTypes)
            for feature in tile.features):

            print(f"Cannot place unit inside an obstacle!")
            return False

        # occupied
        if not phasing:
            for unit in self.units:
                if unit.position == (x,y):
                    print(f"Space already occupied!")
                    return False

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