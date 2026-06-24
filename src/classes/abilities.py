class Ability:
    def on_attack(self, context):
        pass

    def on_move(self, context):
        pass

    def on_turn_start(self, context):
        pass


class DoubleAttack(Ability):
    def on_attack(self, context):

        if not context.extra_attack:

            context.queue_attack(
                context.attacker,
                context.target,
                extra_attack=True
            )


class SteadyShot(Ability):
    def modify_damage(self, context):

        if context.attacker.did_not_move:

            context.damage += 5