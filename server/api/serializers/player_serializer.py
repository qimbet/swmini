def serialize_player(player):
    """
    Serialize a Player into an API-safe dictionary.

    Player identity is represented by player_id.
    Army composition is represented by unit IDs and their
    original deployment positions.

    This function does not serialize the live Unit objects;
    those are handled by unit_serializer.
    """

    army_data = None

    if player.army is not None:
        army_data = {
            "faction": player.army.faction,
            "units": [
                {
                    "unit_id": army_unit.unit.id,
                    "start_position": (
                        list(army_unit.start_position)
                        if army_unit.start_position is not None
                        else None
                    ),
                }
                for army_unit in player.army.units
            ],
        }

    return {
        "player_id": player.id,
        "name": player.name,
        "faction": player.faction,
        "side": player.side,
        "army": army_data,
    }


def serialize_players(players):
    """
    Serialize a collection of players.

    Returns a list suitable for inclusion in the game-state payload.
    """

    return [
        serialize_player(player)
        for player in players
    ]
