from test_modul_konfiguration import Konfiguration, Farben


class WohnzimmerLayout:
    """Berechnet NUR, welche Kachel welches Möbelstück im Wohnzimmer ist.

    Baut daraus ein Dict {(gx, gy): (farbe, label)}, genau wie KuechenLayout.
    Das Sofa ist L-förmig (ein senkrechter Teil rechts + ein waagerechter
    Teil unten quer durchs Zimmer), deshalb braucht es zwei Teil-Rechtecke.
    """

    def __init__(self, breite, hoehe, farben=Farben):
        self.breite = breite
        self.hoehe = hoehe
        self.farben = farben
        self.kacheln = self._berechnen()

    def _berechnen(self):
        layout = {}
        layout.update(self._boden_markierung())
        layout.update(self._ladestation())
        layout.update(self._fernsehtisch())
        layout.update(self._sofa())
        return layout

    def _boden_markierung(self):
        """Eine einzelne Bodenkachel mit der Ziffer 4 beschriften."""
        gx, gy = round(self.breite * 0.5), max(1, round(self.hoehe * 0.35))
        return {(gx, gy): (self.farben.BODEN_WOHNZIMMER, "4")}

    def _ladestation(self):
        """Ladestation oben links (Kachel 1)."""
        teil = {}
        x1 = max(1, round(self.breite * 0.22))
        y1 = max(1, round(self.hoehe * 0.33)) - 1
        for gx in range(0, x1):
            for gy in range(0, y1 + 1):
                teil[(gx, gy)] = (self.farben.LADESTATION, None)
        teil[((x1 - 1) // 2, y1 // 2)] = (self.farben.LADESTATION, "1")
        self._lade_breite = x1  # merken, wo der Fernsehtisch anfangen darf
        return teil

    def _fernsehtisch(self):
        """Fernsehtisch + Fernseher oben, schmales Band (Kachel 2)."""
        teil = {}
        x0 = self._lade_breite
        x1 = max(x0, round(self.breite * 0.80)) - 1
        for gx in range(x0, x1 + 1):
            teil[(gx, 0)] = (self.farben.FERNSEHTISCH, None)
        teil[(x0 + (x1 - x0) // 2, 0)] = (self.farben.FERNSEHTISCH, "2")
        return teil

    def _sofa(self):
        """L-förmiges Sofa: senkrechter Teil rechts + waagerechter Teil
        unten quer durchs Zimmer (Kachel 3)."""
        teil = {}
        x0_r = max(1, round(self.breite * 0.75))
        y0_r = max(1, round(self.hoehe * 0.45))
        y1_r = min(self.hoehe - 2, y0_r + 1)
        for gx in range(x0_r, self.breite):
            for gy in range(y0_r, y1_r + 1):
                teil[(gx, gy)] = (self.farben.SOFA, None)

        x0_u = max(1, round(self.breite * 0.22))
        y0_u = y1_r + 1
        for gx in range(x0_u, self.breite):
            for gy in range(y0_u, self.hoehe):
                teil[(gx, gy)] = (self.farben.SOFA, None)

        teil[(x0_u + (self.breite - x0_u) // 2, self.hoehe - 1)] = (self.farben.SOFA, "3")
        return teil

    def kachel_bei(self, gx, gy):
        """Liefert (farbe, label) für eine Kachel, oder Boden-Farbe + kein Label,
        falls dort kein Möbelstück liegt."""
        return self.kacheln.get((gx, gy), (self.farben.BODEN_WOHNZIMMER, None))
