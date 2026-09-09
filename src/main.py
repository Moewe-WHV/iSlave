"""Haupteinstiegspunkt der Terminalanwendung.

Ablauf: Nutzer auswaehlen oder anlegen (#32), Wartung pruefen (#21),
danach das Menue zur Steuerung des Roboters (#24). Beim Beenden werden
Punktestand und Roboterzustand im Nutzerprofil gespeichert (#20, #31).

Start:
    python src/main.py              mit Tkinter-Kartenansicht (#22)
    python src/main.py --ohne-gui   nur Terminal
"""

import sys
from datetime import date

import nutzerverwaltung
from interaktion import terminal_menu
from spiel import Spiel


def letzte_wartung_lesen(nutzer) -> date:
    """Liest das gespeicherte Wartungsdatum, sonst gilt heute."""
    if not nutzer.letzte_wartung:
        return date.today()
    try:
        return date.fromisoformat(nutzer.letzte_wartung)
    except ValueError:
        print("Wartungsdatum im Profil ist unlesbar, es wird heute angenommen.")
        return date.today()


def spiel_aus_nutzer(nutzer) -> Spiel:
    """Baut den Spielzustand aus dem gespeicherten Nutzerprofil."""
    return Spiel(
        nutzername=nutzer.name,
        akkustand=nutzer.akkustand,
        zyklen_zaehler=nutzer.zyklen_zaehler,
        verbrauchte_kapazitaet=nutzer.verbrauchte_kapazitaet,
        letzte_wartung=letzte_wartung_lesen(nutzer),
        punkte=nutzer.punkte,
        spuelmittel=nutzer.spuelmittel,
    )


def profil_sichern(verwaltung, nutzer, spiel) -> None:
    """Speichert den Roboterzustand zurueck ins Nutzerprofil."""
    try:
        verwaltung.profil_speichern(nutzer, spiel.profil_daten())
    except nutzerverwaltung.NutzerverwaltungError as fehler:
        print(f"Profil konnte nicht gespeichert werden: {fehler}")


def startmeldung_ausgeben(spiel) -> None:
    """Zeigt Zustand und Wartungstermin beim Start an."""
    print("\n===== iSlave =====")
    print(spiel.statuszeile())
    print(spiel.wartungsmeldung())

    if spiel.wartung_ist_faellig():
        print("Der Roboter ist gesperrt. Bitte im Menü die Wartung durchführen.")


def anzeige_starten(spiel):
    """Öffnet die Kartenansicht, wenn Tkinter verfügbar ist (#22)."""
    try:
        import gui
    except ImportError as fehler:
        print(f"Kartenansicht nicht verfügbar ({fehler}), es läuft nur das Terminal.")
        return None
    return gui.anzeige_starten(spiel)


def main(mit_gui: bool = True) -> int:
    verwaltung = nutzerverwaltung.Nutzerverwaltung()
    print(f"Nutzerdaten: {verwaltung.datei}")

    nutzer = nutzerverwaltung.nutzer_auswaehlen_oder_anlegen(verwaltung)
    if nutzer is None:
        print("\nAbgebrochen - ohne Nutzer wird die Simulation nicht gestartet.")
        return 1

    nutzerverwaltung.einloggen(nutzer)

    spiel = spiel_aus_nutzer(nutzer)
    startmeldung_ausgeben(spiel)

    anzeige = anzeige_starten(spiel) if mit_gui else None

    try:
        terminal_menu(spiel)
    finally:
        if anzeige is not None:
            anzeige.schliessen()
        profil_sichern(verwaltung, nutzer, spiel)

    return 0


if __name__ == "__main__":
    sys.exit(main(mit_gui="--ohne-gui" not in sys.argv))
