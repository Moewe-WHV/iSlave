from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

STANDARD_DATEI = Path(__file__).with_name("nutzer.json")
ABBRUCH = {"q", "quit", "exit", "abbruch"}


# ======================================================================
# Fehlerklassen
# ======================================================================
class NutzerverwaltungError(Exception):
    """Basisklasse fuer alle Fehler der Nutzerverwaltung."""


class NutzernameVergebenError(NutzerverwaltungError):
    """Der gewuenschte Nutzername existiert bereits."""


class NutzerNichtGefundenError(NutzerverwaltungError):
    """Der gesuchte Nutzer ist nicht in der Liste."""


class UngueltigerNutzernameError(NutzerverwaltungError):
    """Der Nutzername ist leer oder besteht nur aus Leerzeichen."""


class KeinNutzerAngemeldetError(RuntimeError):
    """Die Simulation wurde ohne angemeldeten Nutzer gestartet."""


# ======================================================================
# Datenmodell
# ======================================================================
@dataclass(frozen=True)
class Nutzer:
    """Ein einzelner Nutzerdatensatz."""

    name: str
    erstellt_am: str

    @classmethod
    def neu(cls, name: str) -> "Nutzer":
        zeitpunkt = datetime.now().isoformat(timespec="seconds")
        return cls(name=name, erstellt_am=zeitpunkt)

    @classmethod
    def aus_dict(cls, daten: dict) -> "Nutzer":
        return cls(name=daten["name"], erstellt_am=daten.get("erstellt_am", ""))

    def als_dict(self) -> dict:
        return asdict(self)


# ======================================================================
# Datenhaltung (JSON)
# ======================================================================
class Nutzerverwaltung:
    """Laedt, speichert und verwaltet die Nutzer in einer JSON-Datei."""

    def __init__(self, datei: str | Path = STANDARD_DATEI) -> None:
        self.datei = Path(datei)
        self._nutzer: list[Nutzer] = []
        self.laden()

    # -- Persistenz -----------------------------------------------------
    def laden(self) -> None:
        """Liest die Nutzer aus der JSON-Datei. Fehlt sie, startet die Liste leer."""
        if not self.datei.exists():
            self._nutzer = []
            return

        try:
            rohdaten = json.loads(self.datei.read_text(encoding="utf-8"))
        except json.JSONDecodeError as fehler:
            raise NutzerverwaltungError(
                f"'{self.datei}' ist keine gueltige JSON-Datei: {fehler}"
            ) from fehler

        eintraege = rohdaten.get("nutzer", []) if isinstance(rohdaten, dict) else rohdaten
        self._nutzer = [Nutzer.aus_dict(eintrag) for eintrag in eintraege]

    def speichern(self) -> None:
        """Schreibt die aktuelle Nutzerliste in die JSON-Datei."""
        if self.datei.parent != Path(""):
            self.datei.parent.mkdir(parents=True, exist_ok=True)

        inhalt = {"nutzer": [nutzer.als_dict() for nutzer in self._nutzer]}
        temp_datei = self.datei.with_suffix(self.datei.suffix + ".tmp")
        temp_datei.write_text(
            json.dumps(inhalt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        temp_datei.replace(self.datei)  # atomar: keine halb geschriebene Datei

    # -- Abfragen -------------------------------------------------------
    @staticmethod
    def _schluessel(name: str) -> str:
        """Vergleichsform eines Namens: ohne Rand-Leerzeichen, Gross/Klein egal."""
        return name.strip().casefold()

    def alle(self) -> list[Nutzer]:
        return list(self._nutzer)

    def ist_leer(self) -> bool:
        return not self._nutzer

    def existiert(self, name: str) -> bool:
        schluessel = self._schluessel(name)
        return any(self._schluessel(n.name) == schluessel for n in self._nutzer)

    def finden(self, name: str) -> Nutzer:
        schluessel = self._schluessel(name)
        for nutzer in self._nutzer:
            if self._schluessel(nutzer.name) == schluessel:
                return nutzer
        raise NutzerNichtGefundenError(f"Es gibt keinen Nutzer mit dem Namen '{name}'.")

    # -- Aenderungen ----------------------------------------------------
    def anlegen(self, name: str) -> Nutzer:
        """Legt einen neuen Nutzer an und speichert ihn.

        Raises:
            UngueltigerNutzernameError: bei leerem Namen.
            NutzernameVergebenError: wenn der Name schon vergeben ist.
        """
        name = name.strip()
        if not name:
            raise UngueltigerNutzernameError("Der Nutzername darf nicht leer sein.")
        if self.existiert(name):
            raise NutzernameVergebenError(f"Der Nutzername '{name}' ist bereits vergeben.")

        nutzer = Nutzer.neu(name)
        self._nutzer.append(nutzer)
        self.speichern()
        return nutzer

    def loeschen(self, name: str) -> None:
        nutzer = self.finden(name)
        self._nutzer.remove(nutzer)
        self.speichern()


# ======================================================================
# Ein-/Ausgabe
# ======================================================================
def frage(text: str) -> str:
    """Eingabe lesen; Strg+C / Strg+D werden wie ein Abbruch behandelt."""
    try:
        return input(text).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def liste_anzeigen(verwaltung: Nutzerverwaltung) -> None:
    print("\nVorhandene Nutzer:")
    for nummer, nutzer in enumerate(verwaltung.alle(), start=1):
        print(f"  [{nummer}] {nutzer.name}  (angelegt am {nutzer.erstellt_am})")


# ======================================================================
# Ablauf nach Flussdiagramm
# ======================================================================
def bestehenden_nutzer_waehlen(verwaltung: Nutzerverwaltung) -> Nutzer | None:
    """Zweig 'ja': Nutzer aus der Liste waehlen."""
    if verwaltung.ist_leer():
        print("\nEs ist noch kein Nutzer angelegt.")
        return None

    while True:
        liste_anzeigen(verwaltung)
        eingabe = frage("Nummer oder Nutzername eingeben ('q' = zurueck): ")
        if eingabe.lower() in ABBRUCH:
            return None

        if eingabe.isdigit():
            nutzerliste = verwaltung.alle()
            index = int(eingabe) - 1
            if 0 <= index < len(nutzerliste):
                return nutzerliste[index]
            print("Fehler: Diese Nummer gibt es nicht.")
            continue

        try:
            return verwaltung.finden(eingabe)
        except NutzerNichtGefundenError as fehler:
            print(f"Fehler: {fehler}")


def neuen_nutzer_anlegen(verwaltung: Nutzerverwaltung) -> Nutzer | None:
    """Zweig 'nein': neuen Nutzer anlegen, bei vergebenem Namen zurueck zur Eingabe."""
    while True:
        eingabe = frage("\nGewuenschter Nutzername ('q' = zurueck): ")
        if eingabe.lower() in ABBRUCH:
            return None

        try:
            nutzer = verwaltung.anlegen(eingabe)
        except (NutzernameVergebenError, UngueltigerNutzernameError) as fehler:
            print(f"Fehler: {fehler}")
            continue  # zurueck zur Eingabe, wie im Diagramm

        print(f"Nutzer '{nutzer.name}' wurde angelegt.")
        return nutzer


def nutzer_auswaehlen_oder_anlegen(verwaltung: Nutzerverwaltung) -> Nutzer | None:
    """Gibt den gewaehlten bzw. angelegten Nutzer zurueck oder None bei Abbruch."""
    while True:
        antwort = frage(
            "\nIst der Nutzer bereits angelegt? [j]a / [n]ein / [q]uit: "
        ).lower()

        if antwort in ABBRUCH:
            return None
        if antwort in {"j", "ja", "y", "yes"}:
            nutzer = bestehenden_nutzer_waehlen(verwaltung)
        elif antwort in {"n", "nein", "no"}:
            nutzer = neuen_nutzer_anlegen(verwaltung)
        else:
            print("Bitte 'j', 'n' oder 'q' eingeben.")
            continue

        if nutzer is not None:
            return nutzer  # -> einloggen


def einloggen(nutzer: Nutzer) -> Nutzer:
    print(f"\nEingeloggt als '{nutzer.name}'.")
    return nutzer


# ======================================================================
# Simulation
# ======================================================================
def starte_simulation(nutzer: Nutzer | None) -> None:
    """Startet die Simulation. Ohne Nutzer wird abgebrochen."""
    if nutzer is None:
        raise KeinNutzerAngemeldetError(
            "Ohne ausgewaehlten oder angelegten Nutzer kann die Simulation "
            "nicht gestartet werden."
        )
    print(f"Simulation wird fuer '{nutzer.name}' gestartet ...")
    # ab hier folgt die eigentliche Simulationslogik


def main() -> int:
    verwaltung = Nutzerverwaltung()
    print(f"Nutzerdaten: {verwaltung.datei}")

    nutzer = nutzer_auswaehlen_oder_anlegen(verwaltung)
    if nutzer is None:
        print("\nAbgebrochen - ohne Nutzer wird die Simulation nicht gestartet.")
        return 1

    einloggen(nutzer)
    starte_simulation(nutzer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
