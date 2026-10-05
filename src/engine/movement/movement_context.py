class MovementContext:
    def __init__(self, unit_snapshot):
        self.unit_id = unit_snapshot["unit_id"]
        self.unit = unit_snapshot

        self.start_position = tuple(unit_snapshot["position"])
        self.current_position = self.start_position

        self.movement_used = 0
        self.movement_segments = 0
        self.actions = []
        self.major_action_declared = False
        self.major_action_forfeited = False

    @property
    def mobile_attack(self):
        return "mobile_attack" in self.unit.get("abilities, []")

    @property
    def movement(self):
        return self.unit["movement"]

    @property
    def movement_allowance(self):  #how far
        if self.major_action_forfeited:
            return self.movement * 2
        return self.unit.movement 

    @property
    def movement_remaining(self):
        return max(
            0,
            self.movement_allowance - self.movement_used,
        )

    def record_action(self, action):
        self.actions.append(action)

    def record_movement(self, destination, cost):
        self.current_position = destination
        self.movement_used += cost
        self.movement_segments += 1

    def record_major_action(self, action):
        self.major_action_declared = True
        self.record_action(action)

    def forfeit_major_action(self):
        self.major_action_forfeited = True