from src.game.grid_coordinates import cell_to_position, position_to_cell

def select_unit(snapshot, player):
    player_id = player.id

    player_units = [
        unit
        for unit in snapshot.get("units", [])
        if unit.get("owner_id") == player_id
        and unit.get("position") is not None
    ]

    if not player_units:
        raise RuntimeError(
            f"Player {player.name} has no units available to select."
        )

    while True:
        cell = input(
            "Which unit do you want to move? "
            "Enter the cell ID (e.g. A1): "
        ).strip()
        if not cell:
            print("Please enter a cell")
            continue

        try:
            position = cell_to_position(cell)
        except ValueError as error:
            print(error)
            continue

        matching_units = [
            unit
            for unit in player_units
            if tuple(unit["position"]) == position
        ]

        if not matching_units:
            print(
                f"No unit belonging to {player.name} "
                f"at {cell}."
            )
            continue

        if len(matching_units) > 1:
            raise RuntimeError(
                f"Multiple units occupy {cell}; "
                "unit selection by cell is ambiguous."
            )

        unit = matching_units[0]
        print(
            f"Selected unit {unit['name']} "
            f"unit {unit['unit_id']}."
            )
        return unit


def select_destination(snapshot, unit, movement_engine, movement_context):
    valid_destinations = movement_engine.get_valid_destinations(movement_context)

    print("\nReachable cells:")

    if not valid_destinations:
        print(f"{unit.name} has no legal movement destinations")
        return None

    for position in sorted(valid_destinations):
        print(position_to_cell(position), end=" ")

    while True:
        cell = input("Where do you want to move? ")

        if not cell.strip():
            return None

        try:
            position = cell_to_position(cell)
        except ValueError as error:
            print(error)
            continue

        if position not in valid_destinations:
            print("That cell is not reachable.")
            continue

        return position