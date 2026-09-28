from src.game.grid_coordinates import cell_to_position, position_to_cell


def select_unit(game):
    game_map = game.map_manager

    while True:
        cell = input("Which unit do you want to move? Enter the cell ID (e.g. A1): ")

        try:
            position = cell_to_position(cell)
        except ValueError as error:
            print(error)
            continue

        unit = game_map.get_unit_at(position)

        if unit is None:
            print(f"No unit at {cell}.")
            continue

        if unit.owner is not game.map_manager.active_player:
            print("That unit does not belong to the active player.")
            continue

        return unit


def select_destination(game, unit, movement_manager):
    reachable = movement_manager.get_reachable_tiles(unit)

    print("\nReachable cells:")

    for position in sorted(reachable):
        print(position_to_cell(position), end=" ")

    print()

    while True:
        cell = input("Where do you want to move? ")

        try:
            position = cell_to_position(cell)
        except ValueError as error:
            print(error)
            continue

        if position not in reachable:
            print("That cell is not reachable.")
            continue

        return position