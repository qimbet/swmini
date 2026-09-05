
class Tile:
    def __init__(self):
        self.features = []
        self.no_stop = False

    def add(self, feature):
        self.features.append(feature)

    def symbol(self):
        if not self.features:
            return " "
        return self.features[-1].symbol()

    def blocks_movement(self):
        return any(
            feature.blocks_movement()
            for feature in self.features
        )

    def movement_cost(self):
        if self.blocks_movement():
            return float("inf")

        return sum(
            feature.movement_cost()
            for feature in self.features
        )

class TileFeature:
    def symbol(self):
        return "c"

    def blocks_movement(self): return False
    def movement_cost(self): return 1
    def cover_value(self): return 0
    def height(self): return 0

class SolidObstacle(TileFeature):
    tags = {"solid", "opaque", "impassable", "enclosed"}
    def symbol(self):
        return "#"
    def blocks_movement(self):

        return True

    def movement_cost(self):
        return float("inf")

    def blocks_vision(self):
        return True


class LightCover(TileFeature):
    tags = {"cover"}
    def symbol(self):
        return "-"

    def cover_value(self):
        return 1

class DenseCover(TileFeature):
    tags = {"cover", "obstruction"}
    def symbol(self):
        return "="
    def cover_value(self):
        return 2

class ShallowPit(TileFeature):
    tags = {}
    def symbol(self):
        return "u"
    def blocks_movement(self): 
        return False

    def movement_cost(self):
        return 1.5


class Pit(TileFeature):
    tags = {}
    def symbol(self):
        return "U"
    def blocks_movement(self): 
        return True

