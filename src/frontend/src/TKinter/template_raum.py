"""Enthält die Raum-Klasse: beschreibt Größe und Hindernisse eines Raums."""


class Raum:
    def __init__(self, name, breite=10, hoehe=12, hindernisse=None):
        self.name = name
        self.breite = breite
        self.hoehe = hoehe
        # Vorsicht-Regel: NIE eine leere Liste [] direkt als Default in der
        # Funktionssignatur nehmen (def ...(hindernisse=[])). Das würde
        # dazu führen, dass sich ALLE Raum-Objekte diese eine Liste teilen.
        # Deswegen: Default ist "None", und wir erzeugen die echte leere
        # Liste hier erst innerhalb von __init__.
        if hindernisse is None:
            self.hindernisse = []
        else:
            self.hindernisse = hindernisse