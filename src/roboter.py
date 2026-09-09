"""Zustand des Roboters auf der Karte.

Haelt Position, Blickrichtung und Ausruestung zusammen. Ob ein Feld
befahren werden darf, prueft die Karte, damit Hindernisse nicht
ueberfahren werden (#30).
"""

from equipment import Ausruestung

NORDEN = "Norden"
OSTEN = "Osten"
SUEDEN = "Süden"
WESTEN = "Westen"

# Bewegungsdifferenz -> Blickrichtung
RICHTUNGEN = {
    (0, -1): NORDEN,
    (1, 0): OSTEN,
    (0, 1): SUEDEN,
    (-1, 0): WESTEN,
}


class Roboter:
    """Der Haushaltsroboter mit Position, Blickrichtung und Ausruestung."""

    def __init__(self, position: tuple = (1, 1), ausruestung: Ausruestung = None):
        self.position = position
        self.blickrichtung = SUEDEN
        if ausruestung is None:
            ausruestung = Ausruestung()
        self.ausruestung = ausruestung

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]

    def blickrichtung_setzen(self, ziel: tuple) -> str:
        """Dreht den Roboter in Richtung des Nachbarfeldes."""
        differenz = (ziel[0] - self.x, ziel[1] - self.y)
        if differenz in RICHTUNGEN:
            self.blickrichtung = RICHTUNGEN[differenz]
        return self.blickrichtung

    def bewegen_nach(self, ziel: tuple) -> tuple:
        """Setzt den Roboter auf ein Nachbarfeld und dreht ihn dorthin."""
        self.blickrichtung_setzen(ziel)
        self.position = ziel
        return self.position

    def versetzen_nach(self, ziel: tuple) -> tuple:
        """Setzt den Roboter ohne Wegstrecke auf ein Feld (Raumwechsel)."""
        self.position = ziel
        return self.position

    def als_text(self) -> str:
        """Kurze Zustandszeile fuer das Terminal."""
        return f"Position: {self.position} | Blickrichtung: {self.blickrichtung}"
