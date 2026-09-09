"""Aktionen des Roboters.

Neben der Auswahl legt dieses Modul fest, wie viel Akku eine Aktion
verbraucht (#19), welche Verschmutzungsart sie bearbeitet (#27, #30) und
ob sie Spülmittel oder einen Aufsatz benötigt (#25, #26).
"""

import karte

# Jede Aufgabe verbraucht ihren eigenen festgelegten Wert (#19)
AKKU_VERBRAUCH = {
    "Saugen": 15,
    "Wischen": 20,
    "Spülen": 10,
}

# Welche Verschmutzung bearbeitet welche Aktion (#27, #30)
ZIEL_VERSCHMUTZUNGEN = {
    "Saugen": [karte.STAUB, karte.FUSSEL],
    "Wischen": [karte.FLECK],
    "Spülen": [],
}

# Aktionen, die eine Einheit Spülmittel verbrauchen (#25, #26)
BRAUCHT_SPUELMITTEL = ["Wischen", "Spülen"]

# Aktionen, die einen Staubsaugeraufsatz benötigen (#25, #27)
BRAUCHT_AUFSATZ = ["Saugen"]


class RoboterAktionen:

    gueltige_aktionen = ["Spülen", "Saugen", "Wischen"]

    def __init__(self):
        self.aktuelle_aktion = None

    def aktion_ausfuehren(self, aktion):
        if aktion in self.gueltige_aktionen:
            self.aktuelle_aktion = aktion
            return aktion
        else:
            return "Aktion nicht möglich!"

    def aktionen_bereits_gewaehlt(self, ausgewaehlte_aktionen, aktion):
        return aktion in ausgewaehlte_aktionen

    def reihenfolge_festlegen(self, ausgewaehlte_aktionen):
        if "Saugen" in ausgewaehlte_aktionen and "Wischen" in ausgewaehlte_aktionen:
            return ["Saugen", "Wischen"]
        return ausgewaehlte_aktionen

    def akku_verbrauch(self, aktion) -> int:
        """Festgelegter Akkuverbrauch der Aktion in Prozent (#19)."""
        return AKKU_VERBRAUCH.get(aktion, 0)

    def ziel_verschmutzungen(self, aktion) -> list:
        """Verschmutzungsarten, die diese Aktion bearbeitet."""
        return ZIEL_VERSCHMUTZUNGEN.get(aktion, [])

    def braucht_spuelmittel(self, aktion) -> bool:
        return aktion in BRAUCHT_SPUELMITTEL

    def braucht_aufsatz(self, aktion) -> bool:
        return aktion in BRAUCHT_AUFSATZ

    def passt_zu_verschmutzung(self, aktion, verschmutzung) -> bool:
        """Prüft, ob die Aktion die Verschmutzung bearbeiten kann (#24)."""
        return verschmutzung in self.ziel_verschmutzungen(aktion)
