import random


class DeploymentManager:
    def __init__(self, map_manager):
        self.rng = map_manager.rng or random.Random()
        self.map_manager=map_manager

    def deploy(self, army, side):
        """
        Two passes:
        Units with fixed positions are deployed first.
        Units without fixed positions are randomly placed around them.
        """

        print(f"deploymentManager/deploy: army: {army}")

        # Fixed-position units
        for army_unit in army.units:
            unit = army_unit.unit
            start_position = army_unit.start_position

            x = start_position["x"]
            y = start_position["y"]

            if x is None or y is None:
                continue

            position = (x, y)
            can_place, reason = self.map_manager.can_place(
                position,
                unitToPlace=unit,
                return_reason=True,
            )

            if not can_place:
                unit_name = getattr(
                    unit,
                    "name",
                    unit.__class__.__name__,
                )

                raise RuntimeError(
                    f"Could not place fixed unit '{unit_name}' "
                    f"at {position}: {reason}"
                )

            unit.position = position
            self.map_manager.units.append(unit)


        # Random-position units
        for army_unit in army.units:
            unit = army_unit.unit
            start_position = army_unit.start_position

            x = start_position["x"]
            y = start_position["y"]

            if x is not None and y is not None:
                continue

            position = self.spawn_unit(
                side=side,
                army_unit=army_unit,
            )

            unit.position = position
            self.map_manager.units.append(unit)

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

        x_default = startPosition['x']
        y_default = startPosition['y']

        valid_positions = []
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                if x_default is not None and x != x_default:
                    continue
                if y_default is not None and y != y_default:
                    continue

                position = (x,y)

                if self.map_manager.can_place(position, unitToPlace=unit):
                    valid_positions.append(position)
        if not valid_positions:
            raise RuntimeError(f"Could not find spawn location on the {side_names[side]} side ")

#        if x_default is None and y_default is None:
#            position = self.rng.choice(valid_positions)
#        else:
#            random_position = self.rng.choice(valid_positions)
#
#            x = x_default if x_default is not None else random_position[0]
#            y = y_default if y_default is not None else random_position[1]
#
#            position = (x,y)
#        
#        print(f"Position: {position}")
#        if self.map_manager.can_place(position, unitToPlace=unit):
#            return position
        return self.rng.choice(valid_positions)

#       raise RuntimeError(f"Could not find spawn location for {army_unit} on the {side_names[side]} side")