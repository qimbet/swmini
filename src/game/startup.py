from src.game.core import Game
from src.classes.players import Player


def create_debug_game():
    players = [
        Player(
            name="Alice",
            faction="rebels",
            path_to_army="data/armies/rebel_default.json",
            side=0
        ),
        Player(
            name="Bob",
            faction="rebels",
            path_to_army="data/armies/rebel_default.json",
            side=2
        )
    ]

    return Game(
        seed=1234,
        map_file="src/data/maps/mapLayout.json",
        unit_files={
            "rebels": "src/data/units/rebels.json",
            "imperials": "src/data/units/imperials.json",
        },
        players=players
    )


def main():
    game = create_debug_game()
    game.start()


if __name__ == "__main__":
    main()


