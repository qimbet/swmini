from src.engine.movement.movement_context import MovementContext

class MovementEngine:
    def __init__(self, map_manager):
        self.map_manager = map_manager

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    def create_context(self, unit):
        return MovementContext(unit)

    # --------------------------------------------------
    # Destination validation
    # --------------------------------------------------
#    def get_movement_allowance(self, context):
#        speed = context.unit.movement
#        if context.mobile_attack:
#            return speed
#        if not context.major_action_declared:
#            return speed * 2
#        return speed

    def get_movement_remaining(self, context):
        return max(
            0, 
            self.get_movement_allowance(context)
        )

    def can_move_to(
        self,
        context,
        destination,
    ):
        """
        Determine whether the unit can declare another
        movement segment to the given destination.

        Does not modify authoritative game state.
        """

        if context.movement_segments >= 2:
            return False
        if not self.can_take_movement_segment(context):
            return False

        cost = self.movement_cost(
            context.current_position,
            destination,
            context.unit,
        )

        if cost is None:
            return False

        if cost > self.get_movement_remaining(context):
            return False

        return True

    # --------------------------------------------------
    # Movement cost
    # --------------------------------------------------

    def movement_cost(
        self,
        origin,
        destination,
        unit,
    ):
        """
        Return the number of squares required to move from
        origin to destination.

        Return None if the destination is unreachable.

        This is where your existing pathfinding logic belongs.
        """

        path = self.get_path(
            origin,
            destination,
            unit,
        )

        if path is None:
            return None

        return len(path) - 1

    def can_take_movement_segment(self, context):
        if context.mobile_attack:
            return context.movement_segments < 2
        if context.major_action_declared: 
            return context.movement_segments == 0
        return context.movement_segments < 2

    # --------------------------------------------------
    # Context update
    # --------------------------------------------------

    def record_movement(
        self,
        context,
        destination,
    ):
        """
        Record a movement decision against the temporary
        movement context.

        The real unit is NOT moved.
        """

        cost = self.movement_cost(
            context.current_position,
            destination,
            context.unit,
        )

        if cost is None:
            raise ValueError(
                f"Destination {destination} "
                f"is unreachable."
            )

        if cost > context.movement_remaining:
            raise ValueError(
                f"Destination {destination} "
                f"requires {cost} movement, "
                f"but only "
                f"{context.movement_remaining} remains."
            )

        if context.movement_segments >= 2:
            raise ValueError(
                "Unit cannot declare more than "
                "two movement segments."
            )

        context.record_movement(destination, cost)

    # --------------------------------------------------
    # Pathfinding
    # --------------------------------------------------

    def get_path(
        self,
        origin,
        destination,
        unit,
    ):
        """
        Replace this with your existing pathfinding logic.

        This should account for:
            - map boundaries
            - solid terrain
            - walls
            - unit occupancy
            - unit footprint
            - etc.
        """

        raise NotImplementedError
