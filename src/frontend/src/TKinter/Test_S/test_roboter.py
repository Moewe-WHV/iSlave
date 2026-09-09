"""Enthält die Roboter-Klasse: Position und Bewegungslogik."""


class Roboter:
    def __init__(self, x=2, y=3):
        self.x = x
        self.y = y

    def bewege(self, dx, dy, raum):
        """Versucht den Roboter um (dx, dy) zu verschieben. Gibt True/False zurück."""
        neues_x = self.x + dx
        neues_y = self.y + dy

        innerhalb_der_grenzen = 0 <= neues_x < raum.breite and 0 <= neues_y < raum.hoehe
        if not innerhalb_der_grenzen:
            return False

        if (neues_x, neues_y) in raum.hindernisse:
            return False

        self.x = neues_x
        self.y = neues_y
        return True