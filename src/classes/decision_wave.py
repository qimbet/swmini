
class DecisionWave:
    def __init__(self, player):
        self.player = player
        self._actions = []
        self.locked = False

    # --------------------------------------------------
    # Adding actions
    # --------------------------------------------------

    def add_action(self, action):
        """
        Add an action to the end of the decision wave.

        The order in which actions are added is the order
        in which they will be resolved.
        """

        self._ensure_unlocked()
        self._validate_action(action)
        self._actions.append(action)

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def _validate_action(self, action):
        unit_id = action.unit_id

        if action.action_class == "major":
            if self.has_major_action(unit_id):
                raise ValueError(
                    f"Unit {unit_id} already has "
                    f"a major action."
                )

        elif action.action_class == "minor":
            #we intentionally don't restrict movements here. 
            #movement may be split around major actions
            pass

        else:
            raise ValueError(
                f"Unknown action class: "
                f"{action.action_class}"
            )

    # --------------------------------------------------
    # Queries
    # --------------------------------------------------

    @property
    def actions(self):
        return tuple(self._actions)

    def has_major_action(self, unit_id):
        return any(
            action.unit_id == unit_id
            and action.action_class == "major"
            for action in self.actions
        )

    def get_actions(self):
        return list(self.actions)

    # --------------------------------------------------
    # Locking
    # --------------------------------------------------

    def lock(self):
        if self.locked:
            raise RuntimeError(
                "Decision wave is already locked."
            )

        self.locked = True

    def is_locked(self):
        return self.locked

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _ensure_unlocked(self):
        if self.locked:
            raise RuntimeError(
                "Cannot modify a locked decision wave."
            )

    def __repr__(self):
        return (
            f"DecisionWave("
            f"player={self.player.name!r}, "
            f"actions={len(self.actions)}, "
            f"locked={self.locked}"
            f")"
        )

