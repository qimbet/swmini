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

    def random_spawn(self, side): #0-left, 1-top, 2-right, 3-bottom
        game_map = self.map_manager.map
        width = game_map.width
        height = game_map.height

        spawn = game_map.spawn_parameters
        side_names = {
            0: "left",
            1: "top",
            2: "right",
            3: "bottom"
        }

        if side not in side_names:
            raise ValueError(f"Invalid spawn side given! {side}")

        config = spawn[side_names[side]]
        band_width = config['band_width']
        window = config['window']

        if window is None: 
            if side in (0, 2): #left, right -- maximum vertical spawn range
                perpendicular_range = (0, height-1)
            else: 
                perpendicular_range = (0, width-1)
        else:
            center = window['center']
            spread = window['spread']
            
            min_value = max(0, center - spread)
            max_value = min(
                   (height - 1) if side in (0,2) else (width -1),
                    center + spread
                )
            perpendicular_range = (min_value, max_value)

        if side == 0:  # LEFT
            x_range = (0, band_width - 1)
            y_range = perpendicular_range

        elif side == 1:  # TOP
            x_range = perpendicular_range
            y_range = (0, band_width - 1)

        elif side == 2:  # RIGHT
            x_range = (width - band_width, width - 1)
            y_range = perpendicular_range

        elif side == 3:  # BOTTOM
            x_range = perpendicular_range
            y_range = (height - band_width, height - 1)

        
        tryCount = 0
        while tryCount < 15:
            x = self.rng.randint(x_range[0], x_range[1])
            y = self.rng.randint(y_range[0], y_range[1])

            if self.map_manager.can_place((x, y)):
                return (x, y)
            tryCount += 1

        raise RuntimeError(
            f"Could not find spawn location on side {side}"
        )