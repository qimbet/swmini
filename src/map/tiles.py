
class Tile:
    def __init__(self):
        self.features = []
        self.no_stop = False

    def add(self, feature):
        self.features.append(feature)

class TileFeature:
    def blocks_movement(self): return False
    def movement_cost(self): return 1
    def cover_value(self): return 0
    def height(self): return 0


class LightCover(TileFeature):
    tags = {"cover"}
    def cover_value(self):
        return 1

class DenseCover(TileFeature):
    tags = {"cover", "obstruction"}
    def cover_value(self):
        return 2

class ShallowPit(TileFeature):
    tags = {"obstruction"}
    def blocks_movement(self): 
        return False

    def movement_cost(self):
        return 1.5


