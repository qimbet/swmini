from src.classes.actions.action import Action

class MoveAction(Action):
    action_type = "move"
    action_class = "minor"

    def __init__(self, unit_id, destination):
        super().__init__(unit_id)

        self.destination = destination

    def __repr__(self):
        return (
            f"MoveAction("
            f"unit_id={self.unit_id}, "
            f"destination={self.destination}"
            f")"
        )

