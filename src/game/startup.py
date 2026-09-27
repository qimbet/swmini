import argparse, random, json

from src.game.core import Game
from src.classes.players import Player
from server.api.serializers.game_serializer import serialize_game


def create_debug_game(seed=None):
    players = [
        Player(
            name="Alice",
            faction="rebels",
            path_to_army="data/armies/rebel_default.json",
            side=0
        ),
        Player(
            name="Bob",
            faction="imperials",
            path_to_army="data/armies/imperial_default.json",
            side=2
        )
    ]

    print("Default players created. Creating game object.\n.\n.")
    return Game(
        seed=seed if seed else 0,
        map_file=None,
        unit_files=None,
        players=players
    )


def export_game_state(game, path):
    state = serialize_game(game)

    with open(path, "w") as f:
        json.dump(
            state,
            f,
            indent=2
        )
    print(f"Game state exported to: {path}")

def main(seed, outputPath='debug_game_state.json'):
    print("Beginning test game")
    game = create_debug_game(seed=seed)
    game.start()
    export_game_state(game, outputPath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", type=str, default="debug_game_state.json")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**32 -1)

    main(seed=seed, outputPath=args.output)


