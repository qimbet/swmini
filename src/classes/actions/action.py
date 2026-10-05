from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self, unit_id):
        self.unit_id = unit_id

    @property
    @abstractmethod
    def action_type(self):
        """Human-readable/action-dispatch identifier."""
        pass

    @property
    @abstractmethod
    def action_class(self):
        """Either 'major' or 'minor'."""
        pass

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"unit_id={self.unit_id}"
            f")"
        )
