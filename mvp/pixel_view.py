"""Original pixel artwork for the existing simulation; no gameplay rules."""

import tkinter as tk

from .core import HEIGHT, ROOMS, WIDTH

TILE = 16
MAP_WIDTH, MAP_HEIGHT = 448, 384
ORIGINS = ((16, 32), (240, 32), (16, 224), (240, 224))


class Pixels:
    def __init__(self, width, height, color):
        self.width, self.height = width, height
        self.rows = [bytearray(bytes.fromhex(color) * width) for _ in range(height)]

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, int(x)), max(0, int(y))
        x1, y1 = min(self.width, int(x + w)), min(self.height, int(y + h))
        if x1 <= x0 or y1 <= y0:
            return
        stripe = bytes.fromhex(color) * (x1 - x0)
        for row in self.rows[y0:y1]:
            row[x0 * 3 : x1 * 3] = stripe

    def ppm(self, scale=1):
        width, height = int(self.width * scale), int(self.height * scale)
        # Nearest-neighbor scaling keeps hard pixel edges at every window size.
        columns = [min(self.width - 1, int(x / scale)) * 3 for x in range(width)]
        cached = {}
        rows = []
        for y in range(height):
            source = min(self.height - 1, int(y / scale))
            if source not in cached:
                row = self.rows[source]
                cached[source] = b"".join(row[x : x + 3] for x in columns)
            rows.append(cached[source])
        return f"P6\n{width} {height}\n255\n".encode() + b"".join(rows)


def furniture(p, name, x, y, w, h):
    """Draw within the furniture's existing collision footprint."""
    p.rect(x + 2, y + 3, w - 2, h - 3, "756c64")
    p.rect(x, y, w - 2, h - 3, "454453")
    p.rect(x + 2, y + 2, w - 6, h - 7, "aa7351")
    if name in ("Tisch", "Esstisch", "Nachttisch"):
        p.rect(x + 3, y + 3, w - 8, h - 9, "daa366")
        p.rect(x + 4, y + 5, w - 10, 2, "ecc887")
        if w >= 30:
            p.rect(x + w // 2 - 4, y + h // 2 - 4, 8, 8, "f7e8c9")
            p.rect(x + w // 2 - 2, y + h // 2 - 2, 4, 4, "77a47c")
    elif name == "Sofa":
        p.rect(x + 2, y + 2, w - 6, h - 7, "69669a")
        p.rect(x + 5, y + 4, w - 12, 8, "aaa1ca")
        for yy in range(y + 15, y + h - 8, 12):
            p.rect(x + 7, yy, w - 15, 10, "8985b6")
            p.rect(x + 8, yy, w - 17, 2, "b8afd4")
        p.rect(x + 2, y + 7, 4, h - 15, "bab0d4")
        p.rect(x + w - 9, y + 7, 4, h - 15, "55577f")
    elif name == "Bett":
        p.rect(x + 3, y + 4, w - 8, h - 10, "f3e8cf")
        p.rect(x + 5, y + 5, w - 12, 13, "ffffee")
        p.rect(x + w // 2 - 1, y + 5, 2, 13, "c8cbbb")
        p.rect(x + 4, y + 21, w - 10, h - 28, "7694b5")
        p.rect(x + 4, y + 21, w - 10, 5, "b9d5d6")
        for xx in range(x + 9, x + w - 10, 12):
            p.rect(xx, y + 30, 2, h - 39, "8fb0c7")
    elif name in ("Regal", "Schrank"):
        for yy in range(y + 5, y + h - 8, 16):
            p.rect(x + 3, yy, w - 8, 9, "6f534d")
            for i, color in enumerate(("72998a", "d19c73", "aaa2ba")):
                p.rect(x + 3 + i * 3, yy + 1, 2, 7, color)
            p.rect(x + 2, yy + 10, w - 6, 2, "dfb880")
    elif name == "TV":
        p.rect(x + 7, y, w - 18, h - 6, "31394c")
        p.rect(x + 10, y + 2, w - 24, h - 11, "80b7c4")
        p.rect(x + 12, y + 2, 10, 2, "c2ece1")
        p.rect(x + w - 8, y + h - 7, 2, 2, "92c895")
    elif name == "Arbeitsfläche":
        p.rect(x + 2, y + 2, w - 6, h - 7, "e7dfcb")
        for xx in range(x + 4, x + w - 7, 16):
            p.rect(xx, y + h - 12, 13, 5, "bc9270")
            p.rect(xx + 5, y + h - 11, 4, 1, "645d59")
        p.rect(x + 4, y + 4, 20, 12, "808e99")
        p.rect(x + 6, y + 6, 16, 8, "b4d5d5")
        p.rect(x + w - 27, y + 4, 20, 12, "4d5363")
        for dx in (0, 9):
            for dy in (0, 6):
                p.rect(x + w - 25 + dx, y + 5 + dy, 5, 4, "a0a7ad")
    elif name in ("Kühlschrank", "Waschmaschine"):
        p.rect(x + 2, y + 2, w - 6, h - 7, "d7e3dd")
        p.rect(x + 3, y + 3, w - 8, 3, "f7f4dc")
        if name == "Kühlschrank":
            p.rect(x + 2, y + 12, w - 6, 2, "8eaaa9")
            p.rect(x + w - 8, y + 17, 2, 8, "657c83")
        else:
            p.rect(x + w // 2 - 8, y + 10, 16, 15, "738f9c")
            p.rect(x + w // 2 - 5, y + 12, 10, 11, "accdd1")
            p.rect(x + 5, y + 6, 2, 2, "749c89")
    elif name in ("Wanne", "Dusche", "Waschbecken"):
        p.rect(x + 2, y + 2, w - 6, h - 7, "f1f0db")
        p.rect(x + 5, y + 5, w - 12, h - 13, "83b6c0")
        p.rect(x + 7, y + 7, w - 16, h - 17, "b1d9d6")
        p.rect(x + w // 2 - 2, y + 2, 4, 6, "6c8794")
        if h > 20:
            p.rect(x + 9, y + h - 14, w - 22, 2, "d8f1df")


def room_art(p, room, ox, oy):
    tiled = room.name in ("Küche", "Bad")
    for x in range(WIDTH):
        for y in range(HEIGHT):
            xx, yy = ox + x * TILE, oy + y * TILE
            if tiled:
                a, b = (
                    ("b3d1c9", "c6dfd0") if room.name == "Bad" else ("e2d5ac", "eee2bc")
                )
                p.rect(xx, yy, 16, 16, a if (x + y) % 2 else b)
                p.rect(xx, yy, 16, 1, "f5efcf")
                p.rect(xx, yy, 1, 16, "91a9a0")
                p.rect(xx + 12, yy + 12, 2, 2, "c5c2a6")
            else:
                p.rect(xx, yy, 16, 16, "cfaa78" if y % 2 else "d8b785")
                p.rect(xx, yy + 15, 16, 1, "b28a68")
                p.rect(xx + (7 if y % 2 else 0), yy, 1, 15, "be986e")
                p.rect(xx + 3, yy + 5, 7, 1, "e4c695")
    # Cutaway walls are outside the original walkable raster.
    w, h = WIDTH * TILE, HEIGHT * TILE
    for x, y, ww, hh in (
        (ox - 8, oy - 16, w + 16, 16),
        (ox - 8, oy, 8, h + 8),
        (ox + w, oy, 8, h + 8),
        (ox, oy + h, w, 8),
    ):
        p.rect(x, y, ww, hh, "515c66")
        p.rect(x + 2, y + 2, ww - 4, hh - 4, "93aaa9")
    p.rect(ox, oy - 12, w, 7, "d5dfc8")
    p.rect(ox, oy - 4, w, 4, "738b87")
    # Windows set into the wall.
    for wx in (ox + 24, ox + 136):
        p.rect(wx, oy - 15, 24, 13, "586e7a")
        p.rect(wx + 2, oy - 13, 20, 9, "91c5d0")
        p.rect(wx + 4, oy - 12, 7, 2, "e3f1d8")
        p.rect(wx + 11, oy - 13, 2, 9, "edf0d5")
    for name, x, y, fw, fh in room.furniture:
        furniture(p, name, ox + x * TILE, oy + y * TILE, fw * TILE, fh * TILE)


def apartment():
    p = Pixels(MAP_WIDTH, MAP_HEIGHT, "354954")
    # One continuous hallway connects the four rooms visually.
    p.rect(8, 184, 432, 24, "9caa96")
    p.rect(216, 16, 16, 360, "9caa96")
    for y in range(184, 208, 8):
        for x in range(8, 440, 8):
            p.rect(x, y, 7, 7, "aebba3")
    for room, (ox, oy) in zip(ROOMS.values(), ORIGINS):
        room_art(p, room, ox, oy)
        # Open door at the free side of each room, facing the central hallway.
        door_x = ox + WIDTH * TILE if ox == 16 else ox - 8
        door_y = oy + 7 * TILE
        p.rect(door_x, door_y, 8, 16, "dac396")
        p.rect(door_x, door_y, 8, 2, "eee0b9")
    return p


ROBOT = (
    "......oo......",
    ".....oyyo.....",
    "...oooooooo...",
    "..owwwwwwwwo..",
    "..owccccccwo..",
    "..owcKccKcwo..",
    "..owccccccwo..",
    "...owwwwwo....",
    "..ooottoooo...",
    ".owowttwowwo..",
    ".owoowwooowo..",
    "..o.owwwo.o...",
    "....ooooo.....",
    "...oss.osso...",
    "...ooo.ooo....",
)
PALETTE = {
    "o": "344654",
    "w": "e6e6c9",
    "c": "68a6a6",
    "K": "263c50",
    "t": "d99f69",
    "s": "7799a1",
    "y": "edcb73",
}


class PixelView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.art = apartment()
        self.cached_scale = None
        self.image = None
        self.robot_image = None

    def draw(self, sim):
        c = self.canvas
        scale = max(
            0.25,
            min(
                (c.winfo_width() - 12) / MAP_WIDTH, (c.winfo_height() - 12) / MAP_HEIGHT
            ),
        )
        scale = round(scale, 3)
        if scale != self.cached_scale:
            self.image = tk.PhotoImage(master=c, data=self.art.ppm(scale), format="PPM")
            # Transparent robot sprite, built from original palette pixels.
            sprite = tk.PhotoImage(master=c, width=14, height=15)
            for y, row in enumerate(ROBOT):
                for x, value in enumerate(row):
                    if value != ".":
                        sprite.put("#" + PALETTE[value], (x, y))
            factor = max(1, round(scale))
            self.robot_image = sprite.zoom(factor, factor)
            self.cached_scale = scale
        c.delete("all")
        left = (c.winfo_width() - self.image.width()) / 2
        top = (c.winfo_height() - self.image.height()) / 2
        c.create_image(left, top, image=self.image, anchor="nw", tags=("apartment",))
        for room, (ox, oy) in zip(ROOMS.values(), ORIGINS):
            tag = "room:" + room.name
            active = room.name == sim.state.room
            x0, y0 = left + ox * scale, top + oy * scale
            completed = any(
                a in sim.state.completed[room.name] for a in ("Saugen", "Wischen")
            )
            for x, y in room.floor:
                if completed or (active and (x, y) in sim.visited):
                    xx, yy = x0 + x * TILE * scale, y0 + y * TILE * scale
                    c.create_rectangle(
                        xx + 2,
                        yy + 2,
                        xx + 4,
                        yy + 4,
                        fill="#d8f8db",
                        outline="",
                        tags=(tag,),
                    )
            c.create_text(
                x0 + 5,
                y0 + HEIGHT * TILE * scale - 8,
                text=room.name,
                anchor="sw",
                fill="#263e4b",
                font=("Consolas", 10, "bold"),
                tags=("room-label", tag),
            )
            if active:
                x, y = sim.position
                c.create_image(
                    x0 + (x + 0.5) * TILE * scale,
                    y0 + (y + 0.5) * TILE * scale,
                    image=self.robot_image,
                    tags=("robot", tag),
                )
