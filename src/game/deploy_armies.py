import random



#class DeploymentZone:
#    def __init__(self, x_range, y_range):
#        self.x_range = x_range
#        self.y_range = y_range
#
#    def contains(self, position):
#        x, y = position
#        return (
#            self.x_range[0] <= x <= self.x_range[1]
#            and
#            self.y_range[0] <= y <= self.y_range[1]
#        )
#
#    def positions(self):
#        for x in range(self.x_range[0], self.x_range[1] + 1):
#            for y in range(self.y_range[0], self.y_range[1] + 1):
#                yield (x, y)
#
#def get_deployment_zone(self, side):
#    game_map = self.map_manager.map
#    width = game_map.width
#    height = game_map.height
#    spawn = game_map.spawn_parameters
#
#    side_names = {
#        0: "left",
#        1: "top",
#        2: "right",
#        3: "bottom",
#    }
#
#    if side not in side_names:
#        raise ValueError(f"Invalid spawn side given! {side}")
#
#    config = spawn[side_names[side]]
#
#    band_width = config["band_width"]
#    window = config["window"]
#
#    if window is None:
#        perpendicular_range = (
#            0,
#            height - 1
#        ) if side in (0, 2) else (0, width - 1)
#    else:
#        center = window["center"]
#        spread = window["spread"]
#
#        max_perpendicular = (
#            height - 1
#            if side in (0, 2)
#            else width - 1
#        )
#
#        perpendicular_range = (
#            max(0, center - spread),
#            min(max_perpendicular, center + spread)
#        )
#
#    if side == 0:       # LEFT
#        x_range = (0, band_width - 1)
#        y_range = perpendicular_range
#
#    elif side == 1:     # TOP
#        x_range = perpendicular_range
#        y_range = (0, band_width - 1)
#
#    elif side == 2:     # RIGHT
#        x_range = (width - band_width, width - 1)
#        y_range = perpendicular_range
#
#    else:               # BOTTOM
#        x_range = perpendicular_range
#        y_range = (height - band_width, height - 1)
#
#    return DeploymentZone(x_range, y_range)

class DeploymentManager:
    def __init__(self, map_manager):
        self.rng = map_manager.rng or random.Random()
        self.map_manager=map_manager

    def deploy(self, army, side):
        #army comes as a list of: [(unit, position)]
        #where position is the dict defined in the .json army file
        print(f"deploymentManager/deploy: army: {army}")

        for army_unit in army.units:
            unit = army_unit.unit
            print(f"\n.\nDeploymentManager/deploy: unit: {unit}")

            position = self.spawn_unit(side=side, army_unit=army_unit)

            unit.position = position



    def spawn_unit(self, side, army_unit): #assigns a random location if not specified
        #0-left, 1-top, 2-right, 3-bottom
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

        
        unit = army_unit.unit
        startPosition = army_unit.start_position
        print(f"startPosition: {startPosition}")
        x_default = startPosition['x']
        y_default = startPosition['y']

        print(f"x_default: {x_default}")
        print(f"y_default: {y_default}")

        valid_positions = []
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                position = (x,y)

                if self.map_manager.can_place(position, unitToPlace=unit):
                    valid_positions.append(position)
        if not valid_positions:
            raise RuntimeError(f"Could not find spawn location on side {side}")

        if x_default is None and y_default is None:
            position = self.rng.choice(valid_positions)
        else:
            random_position = self.rng.choice(valid_positions)

            x = x_default if x_default is not None else random_position[0]
            y = y_default if y_default is not None else random_position[1]

            position = (x,y)
        
        print(f"Position: {position}")
        if self.map_manager.can_place(position, unitToPlace=unit):
            return position

        raise RuntimeError(f"Could not find spawn location on side {side}")