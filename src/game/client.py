from src.game.config import ASSETS, MAPS_DIR


def draw_map(self):
    ts = self.tile_size

    for y in range(self.map.height):
        for x in range(self.map.width):

            tile = self.map.tiles[y][x]

            self.canvas.create_text(
                x * ts + ts // 2,
                y * ts + ts // 2,
                text=tile.symbol(),
            )

            if x < self.map.width - 1:
                if self.map.get_edge((x, y), (x + 1, y)):
                    self.canvas.create_line(
                        (x + 1) * ts,
                        y * ts,
                        (x + 1) * ts,
                        (y + 1) * ts,
                        width=3
                    )

            if y < self.map.height - 1:
                if self.map.get_edge((x, y), (x, y + 1)):
                    self.canvas.create_line(
                        x * ts,
                        (y + 1) * ts,
                        (x + 1) * ts,
                        (y + 1) * ts,
                        width=3
                    )
