"""Tests des Einstiegspunkts und des Menuedurchlaufs.

Nutzer- und Punktedateien liegen in einem temporaeren Ordner, damit
weder src/nutzer.json noch highscores.json angefasst wird.
"""

import os
import shutil
import tempfile
from datetime import date

import pytest

import main
import nutzerverwaltung
from interaktion import terminal_menu
from nutzerverwaltung import Nutzer, Nutzerverwaltung
from spiel import Spiel

HEUTE = date(2026, 9, 9)


@pytest.fixture
def ordner():
    """Temporaerer Ordner fuer Nutzer- und Punktedatei."""
    pfad = tempfile.mkdtemp()
    yield pfad
    shutil.rmtree(pfad, ignore_errors=True)


@pytest.fixture
def verwaltung(ordner):
    return Nutzerverwaltung(os.path.join(ordner, "nutzer.json"))


@pytest.fixture
def spiel(ordner):
    return Spiel(
        "Tester",
        akkustand=100,
        letzte_wartung=HEUTE,
        heute=HEUTE,
        highscore_datei=os.path.join(ordner, "highscores.json"),
    )


# ==================== Profil lesen (#20, #21, #31) ====================


# MAIN-T01: Ohne gespeichertes Datum gilt heute als letzte Wartung
def test_MAIN_T01_ohne_wartungsdatum_gilt_heute():
    nutzer = Nutzer.neu("Tester")

    assert main.letzte_wartung_lesen(nutzer) == date.today()


# MAIN-T02: Ein gespeichertes Datum wird gelesen
def test_MAIN_T02_gespeichertes_wartungsdatum_wird_gelesen():
    nutzer = Nutzer(name="Tester", erstellt_am="", letzte_wartung="2026-01-01")

    assert main.letzte_wartung_lesen(nutzer) == date(2026, 1, 1)


# MAIN-T03: Ein unlesbares Datum führt nicht zum Abbruch
def test_MAIN_T03_unlesbares_datum_wird_abgefangen(capsys):
    nutzer = Nutzer(name="Tester", erstellt_am="", letzte_wartung="kein Datum")

    assert main.letzte_wartung_lesen(nutzer) == date.today()
    assert "unlesbar" in capsys.readouterr().out


# MAIN-T04: Der Spielzustand wird aus dem Profil aufgebaut
def test_MAIN_T04_spiel_aus_profil():
    nutzer = Nutzer(
        name="Tester",
        erstellt_am="",
        akkustand=55,
        zyklen_zaehler=9,
        verbrauchte_kapazitaet=40,
        letzte_wartung="2026-01-01",
        punkte=6,
        spuelmittel=2,
    )

    spiel = main.spiel_aus_nutzer(nutzer)

    assert spiel.nutzername == "Tester"
    assert spiel.akku.akkustand == 55
    assert spiel.akku.zyklen_zaehler == 9
    assert spiel.akku.verbrauchte_kapazitaet == 40
    assert spiel.letzte_wartung == date(2026, 1, 1)
    assert spiel.highscore.punkte == 6
    assert spiel.roboter.ausruestung.spuelmittel == 2


# ==================== Profil speichern (#20, #32) ====================


# MAIN-T05: Der Roboterzustand landet im Nutzerprofil
def test_MAIN_T05_profil_wird_gesichert(verwaltung, spiel):
    nutzer = verwaltung.anlegen("Tester")
    spiel.aktion_ausfuehren("Wischen")  # verbraucht Akku, bringt 2 SP

    main.profil_sichern(verwaltung, nutzer, spiel)

    gespeichert = verwaltung.finden("Tester")
    assert gespeichert.punkte == 2
    assert gespeichert.akkustand == spiel.akku.akkustand
    assert gespeichert.letzte_wartung == "2026-09-09"


# MAIN-T06: Ein unbekannter Nutzer beendet das Programm nicht
def test_MAIN_T06_unbekannter_nutzer_wird_gemeldet(verwaltung, spiel, capsys):
    fremder = Nutzer.neu("Niemand")

    main.profil_sichern(verwaltung, fremder, spiel)

    assert "konnte nicht gespeichert werden" in capsys.readouterr().out


# ==================== Startmeldung (#21) ====================


# MAIN-T07: Beim Start werden Zustand und Wartungstermin gezeigt
def test_MAIN_T07_startmeldung(spiel, capsys):
    main.startmeldung_ausgeben(spiel)
    ausgabe = capsys.readouterr().out

    assert "Akku: 100%" in ausgabe
    assert "Nächste Wartung" in ausgabe


# MAIN-T08: Eine fällige Wartung wird beim Start deutlich gemeldet
def test_MAIN_T08_startmeldung_bei_faelliger_wartung(ordner, capsys):
    spiel = Spiel(
        "Tester",
        letzte_wartung=date(2020, 1, 1),
        heute=HEUTE,
        highscore_datei=os.path.join(ordner, "highscores.json"),
    )

    main.startmeldung_ausgeben(spiel)

    assert "gesperrt" in capsys.readouterr().out


# ==================== Menuedurchlauf (#24) ====================


# MAIN-T09: Eine falsche Eingabe beendet die Simulation nicht
def test_MAIN_T09_falsche_eingabe_beendet_nicht(spiel, monkeypatch, capsys):
    eingaben = iter(["9", "5", "0"])  # falsch, Karte, beenden
    monkeypatch.setattr("builtins.input", lambda *args: next(eingaben))

    terminal_menu(spiel)
    ausgabe = capsys.readouterr().out

    assert "Falsche Eingabe!" in ausgabe
    assert "R" in ausgabe  # die Karte wurde danach noch angezeigt


# MAIN-T10: Ein vollständiger Auftrag läuft über das Menü
def test_MAIN_T10_auftrag_ueber_das_menue(spiel, monkeypatch, capsys):
    eingaben = iter(
        [
            "2",  # Aufsatz wählen
            "1",  # Aufsatz 1
            "1",  # Auftrag starten
            "Wohnzimmer",  # Raum
            "Saugen",  # erste Aktion
            "n",  # keine weitere Aktion
            "0",  # beenden
        ]
    )
    monkeypatch.setattr("builtins.input", lambda *args: next(eingaben))

    terminal_menu(spiel)
    ausgabe = capsys.readouterr().out

    assert "Aufsatz 1 ausgewählt." in ausgabe
    assert "Fusseln beseitigt." in ausgabe
    assert "Saugen beendet" in ausgabe
    assert "gespeichert!" in ausgabe


# MAIN-T11: Akku laden und Wartung sind über das Menü erreichbar
def test_MAIN_T11_laden_und_wartung_ueber_das_menue(ordner, monkeypatch, capsys):
    spiel = Spiel(
        "Tester",
        akkustand=40,
        letzte_wartung=date(2020, 1, 1),
        heute=HEUTE,
        highscore_datei=os.path.join(ordner, "highscores.json"),
    )
    eingaben = iter(["3", "4", "0"])  # laden, Wartung, beenden
    monkeypatch.setattr("builtins.input", lambda *args: next(eingaben))

    terminal_menu(spiel)
    ausgabe = capsys.readouterr().out

    assert "60 % geladen" in ausgabe
    assert "Wartung durchgeführt." in ausgabe
    assert spiel.akku.akkustand == 100
    assert not spiel.wartung_ist_faellig()


# MAIN-T12: Ohne Nutzer wird die Simulation nicht gestartet
def test_MAIN_T12_ohne_nutzer_kein_start():
    with pytest.raises(nutzerverwaltung.KeinNutzerAngemeldetError):
        nutzerverwaltung.starte_simulation(None)
