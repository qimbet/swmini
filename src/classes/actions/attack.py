from src.classes.actions.action import Action


class AttackAction(Action):

    action_type = "attack"
    action_class = "major"

    def __init__(self, unit_id, target_id):
        super().__init__(unit_id)

        self.target_id = target_id

    def __repr__(self):
        return (
            f"AttackAction("
            f"unit_id={self.unit_id}, "
            f"target_id={self.target_id}"
            f")"
        )
