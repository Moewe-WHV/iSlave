"""Gemeinsamer Spielzustand.

Dieses Modul verbindet die einzelnen Bausteine zu einer Simulation:
Nutzer, Akku, Wartung, Karte, Roboter, Ausruestung, Aktionen und
Highscore.

Die Methoden von Spiel geben ihre Meldungen als Liste zurueck, statt sie
selbst auszugeben. So kann dieselbe Logik vom Terminal (interaktion.py)
und von der Anzeige (gui.py) genutzt werden. Der Akku gibt seinen Stand
weiterhin selbst aus, weil die Testfaelle AKKU1-T01 bis T05 genau diese
Terminalausgabe pruefen.
"""

from datetime import date

import karte
import wartung
from akku import Akku
from aktionen import RoboterAktionen
from equipment import Ausruestung
from highscore import Highscore
from raeume import Raumsteuerung
from roboter import Roboter

STARTRAUM = "Wohnzimmer"

# Punkte je beseitigter Verschmutzung (#31).
# Staub und Fusseln bringen laut User Story keine SP.
PUNKTE_JE_VERSCHMUTZUNG = {
    karte.FLECK: 2,
}


class Spiel:
    """Haelt den gesamten Zustand einer Spielrunde zusammen."""

    def __init__(
        self,
        nutzername: str,
        akkustand: int = 90,
        zyklen_zaehler: int = 2,
        verbrauchte_kapazitaet: int = 0,
        letzte_wartung: date = None,
        punkte: int = 0,
        spuelmittel: int = 0,
        heute: date = None,
        highscore_datei: str = "highscores.json",
    ):
        self.nutzername = nutzername
        self.heute = heute if heute is not None else date.today()
        if letzte_wartung is None:
            letzte_wartung = self.heute
        self.letzte_wartung = letzte_wartung

        self.karte = karte.Karte()
        self.roboter = Roboter(
            self.karte.startfeld(STARTRAUM), Ausruestung(spuelmittel)
        )
        self.akku = Akku(akkustand, zyklen_zaehler, verbrauchte_kapazitaet)
        self.aktionen = RoboterAktionen()
        self.raumsteuerung = Raumsteuerung()
        self.raumsteuerung.raum_wechseln(STARTRAUM)

        self.highscore = Highscore(dateiname=highscore_datei)
        self.highscore.punkte_setzen(punkte)

    # -- Zustand --------------------------------------------------------
    @property
    def aktueller_raum(self) -> str:
        return self.raumsteuerung.aktueller_raum

    def statuszeile(self) -> str:
        """SP werden neben dem Akkustand angezeigt (#31)."""
        return (
            f"Nutzer: {self.nutzername} | "
            f"Akku: {self.akku.akkustand}% | "
            f"SP: {self.highscore.punkte} | "
            f"Zyklen: {self.akku.zyklen_zaehler}/{self.akku.max_zyklen} | "
            f"Raum: {self.aktueller_raum}"
        )

    def ausruestungszeile(self) -> str:
        return self.roboter.ausruestung.als_text()

    def profil_daten(self) -> dict:
        """Zustand, der im Nutzerprofil gespeichert wird."""
        return {
            "akkustand": self.akku.akkustand,
            "zyklen_zaehler": self.akku.zyklen_zaehler,
            "verbrauchte_kapazitaet": self.akku.verbrauchte_kapazitaet,
            "letzte_wartung": self.letzte_wartung.isoformat(),
            "punkte": self.highscore.punkte,
            "spuelmittel": self.roboter.ausruestung.spuelmittel,
        }

    # -- Wartung (#21) --------------------------------------------------
    @property
    def wartungstermin(self) -> date:
        return wartung.berechne_naechste_wartung(self.letzte_wartung)

    def wartung_ist_faellig(self) -> bool:
        return wartung.ist_wartung_faellig(self.wartungstermin, self.heute)

    def wartungsmeldung(self) -> str:
        return wartung.erstelle_wartungsmeldung(self.wartungstermin, self.heute)

    def wartung_ausfuehren(self) -> list:
        """Setzt die letzte Wartung auf heute und nennt den neuen Termin."""
        self.letzte_wartung = wartung.wartung_durchfuehren(self.heute)
        return ["Wartung durchgeführt.", self.wartungsmeldung()]

    # -- Akku (#19, #20) ------------------------------------------------
    def akku_laden(self) -> list:
        """Lädt den Akku auf 100 %."""
        geladen, zyklen, stand = self.akku.laden(batterie_laden=True)
        meldungen = [f"Akku um {geladen} % geladen. Neuer Stand: {stand} %."]
        if zyklen >= self.akku.warngrenze_zyklen:
            meldungen.append(
                "Achtung: Die Batterie ist fast am Ende ihrer Lebensdauer!"
            )
        return meldungen

    def einsatzbereit(self) -> list:
        """Prüft Wartung und Akku. Leere Liste bedeutet einsatzbereit."""
        if self.wartung_ist_faellig():
            return [self.wartungsmeldung()]
        if not self.akku.kann_aufgabe_ausfuehren():
            return [
                "Akku unter 20 %. Der Roboter kann keine Aufgaben ausführen.",
                "Bitte zuerst laden.",
            ]
        return []

    # -- Raumwechsel (#25) ----------------------------------------------
    def raum_wechseln(self, zielraum: str) -> list:
        """Schickt den Roboter in einen anderen Raum."""
        ergebnis = self.raumsteuerung.raum_wechseln(zielraum)
        if ergebnis == "Raum nicht vorhanden!":
            return [ergebnis]

        meldungen = [f"Roboter fährt ins {zielraum}."]
        meldungen += self._fahren_nach(self.karte.startfeld(zielraum))
        return meldungen

    def verfuegbare_raeume(self) -> list:
        return self.raumsteuerung.gueltige_raeume

    # -- Aufsatzwahl (#27) ----------------------------------------------
    def aufsatz_waehlen(self, nummer) -> list:
        if self.roboter.ausruestung.aufsatz_waehlen(nummer):
            return [f"Aufsatz {nummer} ausgewählt."]
        return ["Aufsatz nicht vorhanden! Wähle Aufsatz 1 oder 2."]

    # -- Auftrag (#24) --------------------------------------------------
    def auftrag_ausfuehren(self, gewaehlte_aktionen: list) -> list:
        """Führt einen Auftrag aus mehreren Aktionen aus.

        Sind Saugen und Wischen gewählt, wird zuerst gesaugt (#24).
        """
        hindernis = self.einsatzbereit()
        if hindernis:
            return hindernis

        meldungen = []
        for aktion in self.aktionen.reihenfolge_festlegen(gewaehlte_aktionen):
            meldungen += self.aktion_ausfuehren(aktion)
            if not self.akku.kann_aufgabe_ausfuehren():
                meldungen.append("Akku unter 20 %. Auftrag wird abgebrochen.")
                break
        return meldungen

    def aktion_ausfuehren(self, aktion: str) -> list:
        """Führt eine einzelne Aktion im aktuellen Raum aus."""
        if self.aktionen.aktion_ausfuehren(aktion) == "Aktion nicht möglich!":
            return ["Aktion nicht möglich!"]

        hindernis = self.einsatzbereit()
        if hindernis:
            return hindernis

        if aktion == "Spülen":
            meldungen = self._spuelen()
        else:
            meldungen = self._reinigen(aktion)

        self.akku.verbrauchen(self.aktionen.akku_verbrauch(aktion))
        meldungen.append(f"{aktion} beendet. Akkustand: {self.akku.akkustand} %.")
        return meldungen

    def _spuelen(self) -> list:
        """Stationäre Aufgabe mit einer Einheit Spülmittel (#25)."""
        meldungen = []

        if not self.roboter.ausruestung.hat_spuelmittel():
            meldungen.append("Kein Spülmittel vorhanden.")
            meldungen += self._spuelmittel_suchen()
            if not self.roboter.ausruestung.hat_spuelmittel():
                return meldungen + ["Spülen nicht möglich!"]

        self.roboter.ausruestung.spuelmittel_verbrauchen()
        meldungen.append("Spülen mit Spülmittel ausgeführt.")
        return meldungen

    def _reinigen(self, aktion: str) -> list:
        """Beseitigt alle passenden Verschmutzungen im Raum (#30)."""
        if self.aktionen.braucht_aufsatz(aktion):
            if self.roboter.ausruestung.aufsatz is None:
                return ["Kein Aufsatz gewählt. Bitte Aufsatz 1 oder 2 wählen."]

        ziele = self.aktionen.ziel_verschmutzungen(aktion)
        offen = [
            feld
            for feld in self.karte.verschmutzungen_im_raum(self.aktueller_raum)
            if self.karte.zeichen(*feld) in ziele
        ]

        if not offen:
            return [f"Im {self.aktueller_raum} gibt es nichts zu {aktion.lower()}."]

        meldungen = []
        for feld in offen:
            verschmutzung = self.karte.zeichen(*feld)
            meldungen += self._fahren_nach(feld)
            meldungen += self._verschmutzung_bearbeiten(feld, aktion, verschmutzung)
        return meldungen

    def _verschmutzung_bearbeiten(
        self, feld: tuple, aktion: str, verschmutzung: str
    ) -> list:
        """Prüft Aufsatz und Material und beseitigt die Verschmutzung."""
        if self.roboter.position != feld:
            return []

        if self.aktionen.braucht_aufsatz(aktion):
            if not self.roboter.ausruestung.aufsatz_passt(verschmutzung):
                passend = self.roboter.ausruestung.passender_aufsatz(verschmutzung)
                return [
                    f"Falscher Aufsatz für {self._bezeichnung(verschmutzung)}. "
                    f"Benötigt wird Aufsatz {passend}."
                ]

        meldungen = []
        if self.aktionen.braucht_spuelmittel(aktion):
            if not self.roboter.ausruestung.hat_spuelmittel():
                meldungen += self._spuelmittel_suchen()
                if not self.roboter.ausruestung.hat_spuelmittel():
                    return meldungen + ["Kein Spülmittel gefunden."]
                meldungen += self._fahren_nach(feld)
            self.roboter.ausruestung.spuelmittel_verbrauchen()

        self.karte.feld_leeren(*feld)
        meldungen.append(f"{self._bezeichnung(verschmutzung)} beseitigt.")

        punkte = PUNKTE_JE_VERSCHMUTZUNG.get(verschmutzung, 0)
        if punkte:
            self.highscore.punkte += punkte
            meldungen.append(f"+{punkte} SP! Aktuelle SP: {self.highscore.punkte}")

        return meldungen

    # -- Bewegung und Aufnahme (#26, #28, #30) --------------------------
    def _fahren_nach(self, ziel: tuple) -> list:
        """Fährt den kürzesten Weg um Hindernisse herum zum Ziel."""
        weg = self.karte.weg_suchen(self.roboter.position, ziel)

        if not weg and self.roboter.position != ziel:
            return ["Ziel ist nicht erreichbar, der Weg ist blockiert."]

        meldungen = []
        for feld in weg:
            self.roboter.bewegen_nach(feld)
            aufnahme = self._gegenstand_pruefen(feld)
            if aufnahme:
                meldungen.append(aufnahme)
        return meldungen

    def _gegenstand_pruefen(self, feld: tuple) -> str:
        """Nimmt einen erkannten Gegenstand automatisch auf (#26, #28)."""
        inhalt = self.karte.zeichen(*feld)
        if inhalt not in karte.GEGENSTAENDE:
            return ""

        if inhalt == karte.SPUELMITTEL and self.roboter.ausruestung.ist_voll():
            return "Spülmittel bleibt liegen, Bestand ist voll (4/4)."

        self.karte.feld_leeren(*feld)
        return self.roboter.ausruestung.gegenstand_aufnehmen(inhalt)

    def _spuelmittel_suchen(self) -> list:
        """Sucht so lange nach Spülmittel, bis welches gefunden wurde (#30)."""
        vorraete = self.karte.suchen(karte.SPUELMITTEL)
        if not vorraete:
            return ["Es ist kein Spülmittel mehr in der Wohnung."]

        erreichbar = []
        for feld in vorraete:
            weg = self.karte.weg_suchen(self.roboter.position, feld)
            if weg:
                erreichbar.append((len(weg), feld))

        if not erreichbar:
            return ["Kein Spülmittel erreichbar."]

        erreichbar.sort()
        meldungen = ["Roboter sucht Spülmittel."]
        meldungen += self._fahren_nach(erreichbar[0][1])
        return meldungen

    @staticmethod
    def _bezeichnung(verschmutzung: str) -> str:
        namen = {
            karte.FLECK: "Fleck",
            karte.STAUB: "Staubansammlung",
            karte.FUSSEL: "Fusseln",
        }
        return namen.get(verschmutzung, "Verschmutzung")

    # -- Anzeige und Abschluss ------------------------------------------
    def karte_als_text(self) -> str:
        return self.karte.als_text(self.roboter.position)

    def beenden(self) -> list:
        """Speichert den Punktestand des Nutzers (#31)."""
        self.highscore.speichern(self.nutzername)
        punkte = self.highscore.punkte
        return [f"Punkte für {self.nutzername} ({punkte} SP) gespeichert!"]
