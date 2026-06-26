from src.game.config import ASSETS, MAPS_DIR
from tkinter import Tk, Canvas
from PIL import Image, ImageTk


class GamePopup:
    def __init__(self, map_obj, background_path, tile_size=48):
        self.map = map_obj
        self.tile_size = tile_size

        self.root = Tk()
        self.root.title("Map Viewer")

        width = map_obj.width * tile_size
        height = map_obj.height * tile_size

        self.canvas = Canvas(
            self.root,
            width=width,
            height=height
        )
        self.canvas.pack()

        img = Image.open(background_path)
        img = img.resize((width, height))
        self.bg = ImageTk.PhotoImage(img)

        self.canvas.create_image(
            0, 0,
            image=self.bg,
            anchor="nw"
        )

        self.draw_map()

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

    def run(self):
        self.root.mainloop()