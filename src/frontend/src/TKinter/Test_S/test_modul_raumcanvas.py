from test_modul_konfiguration import Konfiguration, Farben
import tkinter as tk

class RaumCanvas:
    """Baut NUR die Zeichenfläche (Canvas) und zeichnet dort die Karte:
    Kacheln aus dem KuechenLayout + den Roboter als Kreis."""

    def __init__(self, parent, zimmer, layout, roboter,
                 konfiguration=Konfiguration, farben=Farben):
        self.zimmer = zimmer
        self.layout = layout
        self.roboter = roboter
        self.konfiguration = konfiguration
        self.farben = farben

        self.widget = tk.Canvas(
            parent,
            width=zimmer.breite * konfiguration.TILE_SIZE,
            height=zimmer.hoehe * konfiguration.TILE_SIZE,
            bg=farben.BODEN,
            highlightthickness=0,
        )
        self.widget.pack(side="top")

    def neu_zeichnen(self):
        """Löscht die Zeichenfläche und zeichnet Küche + Raster + Roboter neu."""
        self.widget.delete("all")  # alles Vorherige wird entfernt, sonst stapeln sich die Zeichnungen
        self._zeichne_kacheln()
        self._zeichne_roboter()

    def _zeichne_kacheln(self):
        tile = self.konfiguration.TILE_SIZE
        for gx in range(self.zimmer.breite):
            for gy in range(self.zimmer.hoehe):
                x0, y0 = gx * tile, gy * tile
                x1, y1 = x0 + tile, y0 + tile

                fill, label = self.layout.kachel_bei(gx, gy)
                self.widget.create_rectangle(x0, y0, x1, y1, fill=fill, outline=self.farben.RASTER)

                if label is not None:
                    textfarbe = self.farben.TEXT_HELL if fill != self.farben.STUHL else "black"
                    self.widget.create_text(x0 + tile / 2, y0 + tile / 2,
                                             text=label, fill=textfarbe,
                                             font=("Segoe UI", 11, "bold"))

    def _zeichne_roboter(self):
        """Platzhalter: grüner Kreis an der Roboter-Position."""
        tile = self.konfiguration.TILE_SIZE
        rx0 = self.roboter.x * tile + 6
        ry0 = self.roboter.y * tile + 6
        rx1 = rx0 + tile - 12
        ry1 = ry0 + tile - 12
        self.widget.create_oval(rx0, ry0, rx1, ry1, fill=self.farben.ROBOTER, outline="black", width=2)
