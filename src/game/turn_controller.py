from src.game.cli import select_unit, select_destination
from src.engine.movement.movement_context import MovementContext
from src.engine.movement.movement_engine import MovementEngine
from src.classes.decision_wave import DecisionWave
from src.classes.actions.move import MoveAction
from server.api.serializers.game_serializer import serialize_player_snapshot


class TurnController:
    def __init__(self, game):
        self.game = game

    # --------------------------------------------------
    # Decision phase
    # --------------------------------------------------

    def collect_unit_actions(self, unit, wave, snapshot):
        """
        Collect the ordered actions for one unit.

        DEBUG VERSION:
            - Allows the player to select movement.
            - If the unit has mobile_attack, movement may later be split around a major attack.
            - For now, we collect movement only.

        The MovementContext tracks the unit's movement budget and action history during decision collection.

        No authoritative game state is modified.
        """

        movement_engine = MovementEngine(
            self.game.map_manager
        )

        context = MovementContext(unit)

        # --------------------------------------------------
        # First movement
        # --------------------------------------------------

        destination = select_destination(
            snapshot,
            unit,
            movement_engine,
            context,
        )

        if destination is None:
            return

        move_action = MoveAction(
            unit_id=unit["unit_id"],
            destination=destination,
        )

        wave.add_action(move_action)

        movement_engine.record_movement(
            context,
            destination,
        )

        # --------------------------------------------------
        # Mobile attack
        # --------------------------------------------------

        if context.mobile_attack:

            # DEBUG:
            # We are not collecting attacks yet.
            #
            # This is where the major action will eventually
            # be collected:
            #
            # attack = select_major_action(...)
            # wave.add_action(attack)
            # context.record_major_action()
            #
            # The important thing is that the attack is added
            # AFTER the first movement.

            pass

        # --------------------------------------------------
        # Second movement
        # --------------------------------------------------

        if context.mobile_attack > 0:
            return
        if context.movement_remaining > 0:
            answer = input(
                "Forego major action and move again? [y/N]:"
            ).strip.lower()
            if answer != "y":
                return
            context.record_major_action()

            # DEBUG:
            # For now, allow another movement only if the unit
            # still has movement remaining.
            #
            # For standard units this represents the second
            # minor movement available when the unit gives up
            # its major action.
            #
            # For mobile_attack units this will eventually be
            # reached after an attack if the attack was declared.

            destination = select_destination(
                snapshot,
                unit,
                movement_engine,
                context,
            )

            if destination is None:
                return

            move_action = MoveAction(
                unit_id=unit["unit_id"],
                destination=destination,
            )

            wave.add_action(move_action)

            movement_engine.record_movement(
                context,
                destination,
            )


#    def collect_unit_actions(self, unit, wave, snapshot):
#        context = MovementContext(unit)
#
#        movement_engine = MovementEngine(
#            self.game.map_manager
#        )
#
#        movement_context = MovementContext(unit)
#
#        destination = select_destination(
#            snapshot,
#            unit,
#            movement_engine,
#            movement_context,
#        )
#
#        if destination:
#            wave.add_action(MoveAction(
#                unit_id=unit["unit_id"],
#                destination=destination,
#            ))
#            context.record_movement(movement_context, destination)
#        action = MoveAction(
#                    )
#
#        wave.add_action(action)


    def collect_decision_waves(self, players):
        """
        Collect a DecisionWave from each player.

        DEBUG:
            Only collect decisions from the first player.

        No authoritative game state should be modified here.
        """

        waves = []

        if not players:
            return waves

        # DEBUG: only process one player for now.
        player = players[0]

        print(
            f"\n--- Decision phase: {player.name} ---"
        )

        snapshot = serialize_player_snapshot(self.game, player)

        wave = self.collect_player_wave(
            player,
            snapshot
        )

        waves.append(wave)

        return waves

    def collect_player_wave(self, player, snapshot, debug=False):
        wave = DecisionWave(player)
        movement_engine = MovementEngine(
            self.game.map_manager
        )

        #debug: select only one unit for now
        unit = select_unit(snapshot, player)

        self.collect_unit_actions(
            unit, 
            wave, 
            snapshot
        )

#        movement_context = MovementContext(unit)
#        destination = select_destination(
#            snapshot,
#            unit,
#            movement_engine, 
#            movement_context
#        )
#
#        if destination is None:
#            wave.lock()
#            return wave
#
#        action = MoveAction(
#            unit_id=unit["unit_id"],
#            destination=destination
#        )
#        wave.add_action(action)
#
#        movement_engine.record_movement(
#            movement_context,
#            destination,
#        )
        wave.lock()

        return wave

    # --------------------------------------------------
    # Resolution phase
    # --------------------------------------------------

    def resolve_waves(self, waves):
        "DEBUG: Resolution is intentionally disabled."

        print("\n--- Resolution phase ---")
        for wave in waves:
            print(f"{wave.player.name} locked their decisions.")
            for action in wave.get_actions():
                print(
                    f" {action}"
                )
            print("debug state ON: action resolution currently disabled")


    # --------------------------------------------------
    # Victory conditions
    # --------------------------------------------------

    def check_victory(self):
        """
        DEBUG victory condition:

        A player wins if every opposing player has no units
        remaining.

        Returns:
            winning Player
            None if the game should continue
        """

        alive_players = []

        for player in self.game.players:

            if not player.army:
                continue

            # Adjust this depending on your Army API.
            units = player.army.units

            living_units = [
                unit
                for unit in units
                if unit.position is not None
            ]

            if living_units:
                alive_players.append(player)

        # No winner if more than one player still has pieces.
        if len(alive_players) > 1:
            return None

        # If exactly one player remains, they win.
        if len(alive_players) == 1:
            return alive_players[0]

        # Nobody has pieces.
        return None
