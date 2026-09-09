from test_modul_konfiguration import Konfiguration, Farben


class BadLayout:
    """Berechnet NUR, welche Kachel welches Möbelstück im Bad ist.

    Baut daraus ein Dict {(gx, gy): (farbe, label)}. label ist nur bei der
    jeweils mittleren Kachel eines Möbelstücks gesetzt (fürs Beschriften).
    Diese Klasse zeichnet nichts selbst und kennt kein tkinter-Widget -
    sie liefert nur Daten, die die RaumCanvas-Klasse später zeichnet.
    (Genau wie KuechenLayout, nur mit dem Grundriss vom Bad.)
    """

    def __init__(self, breite, hoehe, farben=Farben):
        self.breite = breite
        self.hoehe = hoehe
        self.farben = farben
        self.kacheln = self._berechnen()

    def _berechnen(self):
        layout = {}
        layout.update(self._dusche())
        layout.update(self._badewanne())
        layout.update(self._toilette())
        layout.update(self._waschbecken())
        layout.update(self._waschmaschine_und_trockner())
        return layout

    def _dusche(self):
        """Dusche oben links (Kachel 1)."""
        teil = {}
        x1 = max(1, round(self.breite * 0.18))
        y1 = max(1, round(self.hoehe * 0.40)) - 1
        for gx in range(0, x1):
            for gy in range(0, y1 + 1):
                teil[(gx, gy)] = (self.farben.DUSCHE, None)
        teil[((x1 - 1) // 2, y1 // 2)] = (self.farben.DUSCHE, "1")
        self._dusche_breite = x1  # merken für die Badewanne (gleiche Spaltenbreite)
        return teil

    def _badewanne(self):
        """Badewanne unten links, gleiche Spalten wie die Dusche (Kachel 2)."""
        teil = {}
        x1 = self._dusche_breite
        hoehe_wanne = max(1, round(self.hoehe * 0.40))
        y0 = self.hoehe - hoehe_wanne
        for gx in range(0, x1):
            for gy in range(y0, self.hoehe):
                teil[(gx, gy)] = (self.farben.BADEWANNE, None)
        teil[((x1 - 1) // 2, y0 + hoehe_wanne // 2)] = (self.farben.BADEWANNE, "2")
        return teil

    def _toilette(self):
        """Toilette oben, schmales Feld (Kachel 3)."""
        teil = {}
        x0 = max(2, round(self.breite * 0.27))
        x1 = max(x0, round(self.breite * 0.40))
        for gx in range(x0, x1 + 1):
            teil[(gx, 0)] = (self.farben.TOILETTE, None)
        teil[(x0 + (x1 - x0) // 2, 0)] = (self.farben.TOILETTE, "3")
        return teil

    def _waschbecken(self):
        """Waschbecken oben, längliches Feld (Kachel 4)."""
        teil = {}
        x0 = round(self.breite * 0.50)
        x1 = round(self.breite * 0.66)
        for gx in range(x0, x1 + 1):
            teil[(gx, 0)] = (self.farben.WASCHBECKEN, None)
        teil[(x0 + (x1 - x0) // 2, 0)] = (self.farben.WASCHBECKEN, "4")
        return teil

    def _waschmaschine_und_trockner(self):
        """Waschmaschine (5) und Wäschetrockner (6) oben rechts, nebeneinander."""
        teil = {}
        x0 = round(self.breite * 0.80)
        mitte = x0 + max(1, (self.breite - x0) // 2)
        hoehe_geraete = max(1, round(self.hoehe * 0.28))

        for gx in range(x0, mitte):
            for gy in range(0, hoehe_geraete):
                teil[(gx, gy)] = (self.farben.WASCHMASCHINE, None)
        teil[(x0 + max(0, (mitte - x0 - 1) // 2), hoehe_geraete // 2)] = \
            (self.farben.WASCHMASCHINE, "5")

        for gx in range(mitte, self.breite):
            for gy in range(0, hoehe_geraete):
                teil[(gx, gy)] = (self.farben.WAESCHETROCKNER, None)
        teil[(mitte + max(0, (self.breite - mitte - 1) // 2), hoehe_geraete // 2)] = \
            (self.farben.WAESCHETROCKNER, "6")
        return teil

    def kachel_bei(self, gx, gy):
        """Liefert (farbe, label) für eine Kachel, oder Boden-Farbe + kein Label,
        falls dort kein Möbelstück liegt."""
        return self.kacheln.get((gx, gy), (self.farben.BODEN_BAD, None))
