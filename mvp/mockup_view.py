"""Display the actual drawings embedded in the project's mockup PDFs."""

import math
from pathlib import Path
import tkinter as tk

from .core import HEIGHT, WIDTH

# Pixel bounds of the room drawings in the extracted, unmodified PDF images.
MOCKUPS = {
    "Wohnzimmer": (
        "wohnzimmer.png",
        (276, 260, 1668, 1168),
        "1 Ladestation · 2 Fernsehtisch / TV · 3 Sofa · 4 Boden",
    ),
    "Küche": (
        "kueche.png",
        (300, 107, 1709, 1131),
        "1 Arbeitsfläche · 2 Kühlschrank · 3 Kochfeld · 4 Tisch · 5–8 Stühle",
    ),
    "Bad": (
        "bad.png",
        (248, 131, 975, 592),
        "1 Dusche · 2 Badewanne · 3 Toilette · 4 Waschbecken\n"
        "5 Waschmaschine · 6 Wäschetrockner",
    ),
    "Schlafzimmer": (
        "schlafzimmer.png",
        (284, 134, 1509, 1118),
        "1 Nachttische · 2 Kleiderschrank · 3 Boden · 4 Bett",
    ),
}


class MockupView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.sources = {}
        self.scaled = {}
        for name, (filename, bounds, _) in MOCKUPS.items():
            source = tk.PhotoImage(
                master=canvas,
                data=(
                    Path(__file__).parent / "assets" / "mockups" / filename
                ).read_bytes(),
                format="PNG",
            )
            cropped = tk.PhotoImage(master=canvas)
            canvas.tk.call(str(cropped), "copy", str(source), "-from", *bounds)
            self.sources[name] = cropped

    def draw(self, sim):
        c = self.canvas
        c.delete("all")
        cell_w, cell_h = max(100, c.winfo_width() / 2), max(100, c.winfo_height() / 2)
        for index, (name, (_, _, legend)) in enumerate(MOCKUPS.items()):
            source = self.sources[name]
            ratio = max(
                source.width() / max(20, cell_w - 24),
                source.height() / max(20, cell_h - 70),
            )
            factor = max(1, math.ceil(ratio))
            key = (name, factor)
            if key not in self.scaled:
                self.scaled[key] = source.subsample(factor, factor)
            image = self.scaled[key]
            left = (index % 2) * cell_w
            top = (index // 2) * cell_h
            x0 = left + (cell_w - image.width()) / 2
            y0 = top + 25
            tag = "room:" + name
            c.create_text(
                left + cell_w / 2,
                top + 12,
                text=name,
                font=("Segoe UI", 10, "bold"),
                fill="#172b3a",
                tags=("room-label", tag),
            )
            c.create_image(x0, y0, image=image, anchor="nw", tags=("mockup", tag))
            c.create_text(
                left + cell_w / 2,
                y0 + image.height() + 6,
                text=legend,
                anchor="n",
                width=cell_w - 16,
                font=("Segoe UI", 8),
                fill="#37434b",
                tags=(tag,),
            )
            if name == sim.state.room:
                x, y = sim.position
                cx = x0 + (x + 0.5) / WIDTH * image.width()
                cy = y0 + (y + 0.5) / HEIGHT * image.height()
                c.create_oval(
                    cx - 5,
                    cy - 5,
                    cx + 5,
                    cy + 5,
                    fill="#087f78",
                    outline="white",
                    width=2,
                    tags=("robot", tag),
                )
