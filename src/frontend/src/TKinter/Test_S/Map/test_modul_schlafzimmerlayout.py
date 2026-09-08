from test_modul_konfiguration import Konfiguration, Farben


class SchlafzimmerLayout:
    """Berechnet NUR, welche Kachel welches Möbelstück im Schlafzimmer ist.

    Baut daraus ein Dict {(gx, gy): (farbe, label)}, genau wie KuechenLayout.
    Der Boden ist die Standardfarbe (siehe kachel_bei) und braucht deshalb
    keine eigene Schleife - nur eine einzelne Kachel wird mit "3" beschriftet,
    damit die Legendenziffer auch im Raum sichtbar ist.
    """

    def __init__(self, breite, hoehe, farben=Farben):
        self.breite = breite
        self.hoehe = hoehe
        self.farben = farben
        self.kacheln = self._berechnen()

    def _berechnen(self):
        layout = {}
        layout.update(self._boden_markierung())
        layout.update(self._bett())
        layout.update(self._nachttische())
        layout.update(self._kleiderschrank())
        return layout

    def _boden_markierung(self):
        """Eine einzelne Bodenkachel mit der Ziffer 3 beschriften."""
        gx, gy = 1, max(2, round(self.hoehe * 0.45))
        return {(gx, gy): (self.farben.BODEN_SCHLAFZIMMER, "3")}

    def _bett(self):
        """Bett mittig oben, reicht von der Kopfseite bis knapp vor die
        Zimmermitte (Kachel 4)."""
        teil = {}
        x0 = max(1, round(self.breite * 0.22))
        x1 = min(self.breite - 2, round(self.breite * 0.78))
        y0 = 0
        y1 = max(y0, round(self.hoehe * 0.65)) - 1
        for gx in range(x0, x1 + 1):
            for gy in range(y0, y1 + 1):
                teil[(gx, gy)] = (self.farben.BETT, None)
        teil[(x0 + (x1 - x0) // 2, y0 + (y1 - y0) // 2)] = (self.farben.BETT, "4")
        self._bett_grenzen = (x0, x1, y0, y1)  # für die Nachttische merken
        return teil

    def _nachttische(self):
        """Nachttisch(e) links und rechts neben dem Bettkopfende (Kachel 1)."""
        teil = {}
        x0, x1, y0, y1 = self._bett_grenzen
        hoehe_tisch = max(1, round(self.hoehe * 0.25))

        if x0 > 0:
            for gy in range(0, hoehe_tisch):
                teil[(x0 - 1, gy)] = (self.farben.NACHTTISCH, None)
            teil[(x0 - 1, hoehe_tisch // 2)] = (self.farben.NACHTTISCH, "1")

        if x1 < self.breite - 1:
            for gy in range(0, hoehe_tisch):
                teil[(x1 + 1, gy)] = (self.farben.NACHTTISCH, None)
            teil[(x1 + 1, hoehe_tisch // 2)] = (self.farben.NACHTTISCH, "1")
        return teil

    def _kleiderschrank(self):
        """Kleiderschrank als breites Band am unteren Zimmerrand (Kachel 2)."""
        teil = {}
        hoehe_schrank = max(1, round(self.hoehe * 0.22))
        y0 = self.hoehe - hoehe_schrank
        for gx in range(0, self.breite):
            for gy in range(y0, self.hoehe):
                teil[(gx, gy)] = (self.farben.KLEIDERSCHRANK, None)
        teil[(self.breite // 2, y0 + hoehe_schrank // 2)] = (self.farben.KLEIDERSCHRANK, "2")
        return teil

    def kachel_bei(self, gx, gy):
        """Liefert (farbe, label) für eine Kachel, oder Boden-Farbe + kein Label,
        falls dort kein Möbelstück liegt."""
        return self.kacheln.get((gx, gy), (self.farben.BODEN_SCHLAFZIMMER, None))
