
#implements movement on board-state pieces
#user inputs are parsed at turn_controller.py

class MovementEngine:
    def __init__(self, map_manager):
        self.map_manager = map_manager

    def validate_movement_sequence(
        self,
        unit,
        movement_actions,
        state,
    ):
        """
        Validate all movement segments belonging to one unit.

        movement_actions must already be in the order in which
        they occur in the DecisionWave.
        """

        current_position = unit.position
        movement_used = 0

        for action in movement_actions:

            cost = self._movement_cost(
                current_position,
                action.destination,
                state,
            )

            if cost is None:
                return False

            movement_used += cost

            if movement_used > unit.movement:
                return False

            current_position = action.destination

        return True

    def _movement_cost(
        self,
        origin,
        destination,
        state,
    ):
        """
        Calculate movement cost between two positions.

        Return None if the destination cannot be reached.
        """

        # For now, plug your existing movement/pathfinding
        # implementation in here.

        path = self.get_path(
            origin,
            destination,
            state,
        )

        if path is None:
            return None

        return len(path) - 1

    def get_path(
        self,
        origin,
        destination,
        state,
    ):
        """
        Existing pathfinding logic goes here.
        """

        ...
