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

    print("Default players created. Creating game object.")
    return Game(
        seed=12334,
        map_file=None,
        unit_files=None,
        players=players
    )


def main():
    print("Beginning test game")
    game = create_debug_game()
    game.start()


if __name__ == "__main__":
    main()


