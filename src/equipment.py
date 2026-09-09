"""Ausruestung des Roboters.

Setzt die User Stories "Equipment 1" (#26), "Equipment 2" (#27) und
"Equipment 3" (#28) um: Spuelmittel wird automatisch aufgenommen und ist
auf vier Einheiten begrenzt, die beiden Aufsaetze besitzt der Roboter
dauerhaft, Ladekabel und Werkzeuge werden automatisch eingesammelt.
"""

import karte

MAX_SPUELMITTEL = 4

AUFSATZ_FUSSELN = 1
AUFSATZ_STAUB = 2
AUFSAETZE = [AUFSATZ_FUSSELN, AUFSATZ_STAUB]

# Der Roboter erkennt selbstaendig, welcher Aufsatz zu welcher
# Verschmutzungsart gehoert (#27).
AUFSATZ_JE_VERSCHMUTZUNG = {
    karte.FUSSEL: AUFSATZ_FUSSELN,
    karte.STAUB: AUFSATZ_STAUB,
}

BEZEICHNUNGEN = {
    karte.SPUELMITTEL: "Spülmittel",
    karte.LADEKABEL: "Ladekabel",
    karte.WERKZEUG: "Werkzeug",
}


class Ausruestung:
    """Verwaltet Bestand und Aufsaetze des Roboters."""

    def __init__(self, spuelmittel: int = 0):
        self.spuelmittel = spuelmittel
        self.aufsatz = None
        self.ladekabel = 0
        self.werkzeuge = 0

    # -- Spuelmittel (#26) ----------------------------------------------
    def hat_spuelmittel(self) -> bool:
        return self.spuelmittel > 0

    def ist_voll(self) -> bool:
        return self.spuelmittel >= MAX_SPUELMITTEL

    def spuelmittel_aufnehmen(self) -> bool:
        """Nimmt eine Einheit auf. Bei vollem Bestand passiert nichts."""
        if self.ist_voll():
            return False
        self.spuelmittel += 1
        return True

    def spuelmittel_verbrauchen(self) -> bool:
        """Verbraucht genau eine Einheit fuer die Reinigung eines Flecks."""
        if not self.hat_spuelmittel():
            return False
        self.spuelmittel -= 1
        return True

    # -- Aufsaetze (#27) ------------------------------------------------
    def aufsatz_waehlen(self, nummer) -> bool:
        """Waehlt Aufsatz 1 oder 2. Andere Angaben werden abgelehnt."""
        if nummer in AUFSAETZE:
            self.aufsatz = nummer
            return True
        return False

    @staticmethod
    def passender_aufsatz(verschmutzung: str):
        """Gibt den fuer die Verschmutzung vorgesehenen Aufsatz zurueck."""
        return AUFSATZ_JE_VERSCHMUTZUNG.get(verschmutzung)

    def aufsatz_passt(self, verschmutzung: str) -> bool:
        """Prueft, ob der gewaehlte Aufsatz zur Verschmutzung passt."""
        return self.aufsatz == self.passender_aufsatz(verschmutzung)

    # -- Gegenstaende (#28) ---------------------------------------------
    def gegenstand_aufnehmen(self, zeichen: str) -> str:
        """Nimmt einen erkannten Gegenstand auf und meldet das Ergebnis."""
        bezeichnung = BEZEICHNUNGEN.get(zeichen, "Gegenstand")

        if zeichen == karte.SPUELMITTEL:
            if self.spuelmittel_aufnehmen():
                return f"{bezeichnung} aufgenommen ({self.spuelmittel}/4)."
            return f"{bezeichnung} bleibt liegen, Bestand ist voll (4/4)."

        if zeichen == karte.LADEKABEL:
            self.ladekabel += 1
            return f"{bezeichnung} aufgenommen."

        if zeichen == karte.WERKZEUG:
            self.werkzeuge += 1
            return f"{bezeichnung} aufgenommen."

        return ""

    # -- Anzeige --------------------------------------------------------
    def als_text(self) -> str:
        """Kurze Zustandszeile fuer das Terminal."""
        if self.aufsatz is None:
            aufsatz = "keiner"
        else:
            aufsatz = f"Aufsatz {self.aufsatz}"
        return (
            f"Spülmittel: {self.spuelmittel}/{MAX_SPUELMITTEL} | "
            f"Aufsatz: {aufsatz} | "
            f"Ladekabel: {self.ladekabel} | Werkzeuge: {self.werkzeuge}"
        )
