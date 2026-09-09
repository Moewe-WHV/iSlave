"""Enthält die Raum-Klasse: beschreibt Größe und Hindernisse eines Raums."""


class Raum:
    def __init__(self, name, breite=10, hoehe=12, hindernisse=None, kachel_farben=None):
        self.name = name
        self.breite = breite
        self.hoehe = hoehe

        if hindernisse is None:
            self.hindernisse = []
        else:
            self.hindernisse = hindernisse

        # Dictionary statt Liste: Schlüssel = (x, y)-Koordinate, Wert = Farbe (hex-String)
        if kachel_farben is None:
            self.kachel_farben = {}
        else:
            self.kachel_farben = kachel_farben