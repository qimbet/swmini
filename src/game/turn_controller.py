from src.game.grid_coordinates import position_to_cell
from src.game.unit_movement import MovementManager
from src.game.cli import select_unit, select_destination


class TurnController:

    def __init__(self, game):
        self.game = game

    def run(self):
        active_player = self.game.map_manager.active_player

        print(
            f"\nTurn {self.game.map_manager.turn_number}"
            f" — {active_player.name}"
        )

        self.game.display()

        unit = select_unit(self.game)

        movement_manager = MovementManager(
            self.game.map_manager
        )

        destination = select_destination(
            self.game,
            unit,
            movement_manager
        )

        print(
            f"{unit.name} moving to "
            f"{position_to_cell(destination)}"
        )

        unit.position = destination