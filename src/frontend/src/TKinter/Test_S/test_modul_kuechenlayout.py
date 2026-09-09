from test_modul_konfiguration import Konfiguration, Farben
import tkinter as tk

class KuechenLayout:
    """Berechnet NUR, welche Kachel welches Möbelstück ist.

    Baut daraus ein Dict {(gx, gy): (farbe, label)}. label ist nur bei der
    jeweils mittleren Kachel eines Möbelstücks gesetzt (fürs Beschriften).
    Diese Klasse zeichnet nichts selbst und kennt kein tkinter-Widget -
    sie liefert nur Daten, die die RaumCanvas-Klasse später zeichnet.
    """

    def __init__(self, breite, hoehe, farben=Farben):
        self.breite = breite
        self.hoehe = hoehe
        self.farben = farben
        self.kacheln = self._berechnen()

    def _berechnen(self):
        layout = {}
        layout.update(self._schrankzeile())
        layout.update(self._tisch())
        layout.update(self._stuehle())
        return layout

    def _schrankzeile(self):
        """Kochfeld / Arbeitsfläche / Kühlschrank als Zeile links."""
        teil = {}
        schrank_breite = max(2, round(self.breite * 0.25))
        kochfeld_ende = max(1, round(self.hoehe * 0.27))
        arbeitsflaeche_ende = max(kochfeld_ende + 1, round(self.hoehe * 0.71))

        for gx in range(0, schrank_breite):
            for gy in range(0, self.hoehe):
                if gy < kochfeld_ende:
                    teil[(gx, gy)] = (self.farben.KOCHFELD, None)
                elif gy < arbeitsflaeche_ende:
                    teil[(gx, gy)] = (self.farben.ARBEITSFLAECHE, None)
                else:
                    teil[(gx, gy)] = (self.farben.KUEHLSCHRANK, None)

        # Labels mittig in jedes der drei Segmente setzen
        mitte_x = schrank_breite // 2
        if kochfeld_ende > 0:
            teil[(mitte_x, kochfeld_ende // 2)] = (self.farben.KOCHFELD, "3")
        teil[(mitte_x, (kochfeld_ende + arbeitsflaeche_ende) // 2)] = (self.farben.ARBEITSFLAECHE, "1")
        teil[(mitte_x, (arbeitsflaeche_ende + self.hoehe) // 2)] = (self.farben.KUEHLSCHRANK, "2")
        return teil

    def _tisch(self):
        """Tisch rechts oben."""
        teil = {}
        x0 = round(self.breite * 0.55)
        x1 = max(x0 + 1, round(self.breite * 0.85) - 1)
        y0 = round(self.hoehe * 0.15)
        y1 = max(y0 + 1, round(self.hoehe * 0.45) - 1)

        for gx in range(x0, x1 + 1):
            for gy in range(y0, y1 + 1):
                teil[(gx, gy)] = (self.farben.TISCH, None)
        teil[((x0 + x1) // 2, (y0 + y1) // 2)] = (self.farben.TISCH, "4")

        # Für _stuehle() merken wir uns die Eckpunkte des Tischs
        self._tisch_x0, self._tisch_x1 = x0, x1
        self._tisch_y0, self._tisch_y1 = y0, y1
        return teil

    def _stuehle(self):
        """Stühle rund um den Tisch (nur optisch, blockieren nichts)."""
        teil = {}
        stuehle = {
            "6": (self._tisch_x0, self._tisch_y0 - 1),  # oben links
            "8": (self._tisch_x1, self._tisch_y0 - 1),  # oben rechts
            "7": (self._tisch_x0, self._tisch_y1 + 1),  # unten links
            "5": (self._tisch_x1, self._tisch_y1 + 1),  # unten rechts
        }
        for label, (sx, sy) in stuehle.items():
            if 0 <= sx < self.breite and 0 <= sy < self.hoehe:
                teil[(sx, sy)] = (self.farben.STUHL, label)
        return teil

    def kachel_bei(self, gx, gy):
        """Liefert (farbe, label) für eine Kachel, oder Boden-Farbe + kein Label,
        falls dort kein Möbelstück liegt."""
        return self.kacheln.get((gx, gy), (self.farben.BODEN, None))

