import json
import os
import shutil
import tempfile
from datetime import date

import pytest

import karte
from equipment import AUFSATZ_FUSSELN, AUFSATZ_STAUB
from spiel import Spiel

HEUTE = date(2026, 9, 9)


@pytest.fixture
def punktedatei():
    """Eigene Highscore-Datei je Test, damit nichts im Repo landet."""
    ordner = tempfile.mkdtemp()
    yield os.path.join(ordner, "highscores.json")
    shutil.rmtree(ordner, ignore_errors=True)


@pytest.fixture
def spiel(punktedatei):
    return Spiel(
        "Tester",
        akkustand=100,
        letzte_wartung=HEUTE,
        heute=HEUTE,
        highscore_datei=punktedatei,
    )


def neues_spiel(punktedatei, **werte):
    """Spiel mit festem Datum und eigener Punktedatei."""
    werte.setdefault("letzte_wartung", HEUTE)
    return Spiel("Tester", heute=HEUTE, highscore_datei=punktedatei, **werte)


def meldungstext(meldungen):
    return "\n".join(meldungen)


# ==================== Zustand und Anzeige (#31) ====================


# SPIEL-T01: Der Punktestand steht neben dem Akkustand
def test_SPIEL_T01_statuszeile_zeigt_akku_und_sp(spiel):
    zeile = spiel.statuszeile()

    assert "Akku: 100%" in zeile
    assert "SP: 0" in zeile
    assert "Tester" in zeile


# SPIEL-T02: Das Spiel startet im Wohnzimmer
def test_SPIEL_T02_start_im_wohnzimmer(spiel):
    assert spiel.aktueller_raum == "Wohnzimmer"
    assert spiel.karte.raum_von(*spiel.roboter.position) == "Wohnzimmer"


# SPIEL-T03: Die Textansicht zeigt den Roboter
def test_SPIEL_T03_kartenansicht_zeigt_roboter(spiel):
    assert "R" in spiel.karte_als_text()


# ==================== Akku (#19, #20) ====================


# SPIEL-T04: Unter 20 % führt der Roboter keine Aufgaben aus
def test_SPIEL_T04_kein_auftrag_unter_20_prozent(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=15)

    meldungen = spiel.auftrag_ausfuehren(["Wischen"])

    assert "Akku unter 20 %" in meldungstext(meldungen)
    assert spiel.akku.akkustand == 15  # nichts verbraucht


# SPIEL-T05: Jede Aktion verbraucht ihren festgelegten Wert
def test_SPIEL_T05_verbrauch_je_aktion(spiel):
    spiel.roboter.ausruestung.spuelmittel_aufnehmen()

    spiel.aktion_ausfuehren("Spülen")

    assert spiel.akku.akkustand == 90  # Spülen kostet 10 %


# SPIEL-T06: Saugen und Wischen kosten unterschiedlich viel
def test_SPIEL_T06_saugen_und_wischen_unterschiedlich(spiel):
    spiel.aufsatz_waehlen(AUFSATZ_FUSSELN)

    spiel.aktion_ausfuehren("Saugen")
    assert spiel.akku.akkustand == 85  # Saugen kostet 15 %

    spiel.aktion_ausfuehren("Wischen")
    assert spiel.akku.akkustand == 65  # Wischen kostet 20 %


# SPIEL-T07: Ein Auftrag bricht ab, wenn der Akku unter 20 % fällt
def test_SPIEL_T07_auftrag_bricht_bei_leerem_akku_ab(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=25)
    spiel.aufsatz_waehlen(AUFSATZ_FUSSELN)

    meldungen = spiel.auftrag_ausfuehren(["Saugen", "Wischen"])

    assert "Auftrag wird abgebrochen" in meldungstext(meldungen)


# SPIEL-T08: Laden setzt den Akku auf 100 %
def test_SPIEL_T08_laden_fuellt_akku(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=30)

    meldungen = spiel.akku_laden()

    assert spiel.akku.akkustand == 100
    assert "70 % geladen" in meldungstext(meldungen)


# ==================== Wartung (#21) ====================


# SPIEL-T09: Eine fällige Wartung sperrt den Roboter
def test_SPIEL_T09_faellige_wartung_sperrt(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=100, letzte_wartung=date(2020, 1, 1))

    assert spiel.wartung_ist_faellig()
    assert "Wartung fällig" in meldungstext(spiel.auftrag_ausfuehren(["Wischen"]))


# SPIEL-T10: Nach der Wartung ist der Roboter wieder nutzbar
def test_SPIEL_T10_wartung_gibt_roboter_frei(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=100, letzte_wartung=date(2020, 1, 1))

    spiel.wartung_ausfuehren()

    assert not spiel.wartung_ist_faellig()
    assert spiel.letzte_wartung == HEUTE
    assert spiel.wartungstermin == date(2028, 9, 9)


# SPIEL-T11: Der nächste Wartungstermin wird genannt
def test_SPIEL_T11_wartungsmeldung_nennt_termin(spiel):
    assert "Nächste Wartung: 09.09.2028" in spiel.wartungsmeldung()


# ==================== Raumwechsel (#25) ====================


# SPIEL-T12: Der Roboter fährt in einen gültigen Raum
def test_SPIEL_T12_raumwechsel_in_die_kueche(spiel):
    meldungen = spiel.raum_wechseln("Küche")

    assert "Küche" in meldungstext(meldungen)
    assert spiel.aktueller_raum == "Küche"
    assert spiel.karte.raum_von(*spiel.roboter.position) == "Küche"


# SPIEL-T13: Ein nicht vorhandener Raum wird abgelehnt
def test_SPIEL_T13_unbekannter_raum_wird_abgelehnt(spiel):
    meldungen = spiel.raum_wechseln("Garage")

    assert meldungen == ["Raum nicht vorhanden!"]
    assert spiel.aktueller_raum == "Wohnzimmer"


# SPIEL-T14: Alle vier Räume werden angeboten
def test_SPIEL_T14_verfuegbare_raeume(spiel):
    assert sorted(spiel.verfuegbare_raeume()) == sorted(
        ["Bad", "Küche", "Schlafzimmer", "Wohnzimmer"]
    )


# ==================== Aufsätze (#27) ====================


# SPIEL-T15: Ohne Aufsatz wird nicht gesaugt
def test_SPIEL_T15_saugen_ohne_aufsatz(spiel):
    meldungen = spiel.aktion_ausfuehren("Saugen")

    assert "Kein Aufsatz gewählt" in meldungstext(meldungen)


# SPIEL-T16: Ein nicht vorhandener Aufsatz wird abgelehnt
def test_SPIEL_T16_unbekannter_aufsatz(spiel):
    assert "Aufsatz nicht vorhanden!" in meldungstext(spiel.aufsatz_waehlen(3))


# SPIEL-T17: Aufsatz 1 entfernt Fusseln, meldet aber Staub als falsch
def test_SPIEL_T17_falscher_aufsatz_wird_gemeldet(spiel):
    spiel.aufsatz_waehlen(AUFSATZ_FUSSELN)

    text = meldungstext(spiel.aktion_ausfuehren("Saugen"))

    assert "Fusseln beseitigt" in text
    assert "Falscher Aufsatz für Staubansammlung" in text
    assert "Benötigt wird Aufsatz 2" in text


# SPIEL-T18: Mit Aufsatz 2 wird die Staubansammlung beseitigt
def test_SPIEL_T18_richtiger_aufsatz_beseitigt_staub(spiel):
    spiel.aufsatz_waehlen(AUFSATZ_STAUB)

    assert "Staubansammlung beseitigt" in meldungstext(
        spiel.aktion_ausfuehren("Saugen")
    )


# ============ Reinigen und Punkte (#26, #30, #31) ============


# SPIEL-T19: Ein gereinigter Fleck bringt 2 SP
def test_SPIEL_T19_fleck_bringt_zwei_sp(spiel):
    text = meldungstext(spiel.aktion_ausfuehren("Wischen"))

    assert "Fleck beseitigt" in text
    assert "+2 SP" in text
    assert spiel.highscore.punkte == 2


# SPIEL-T20: Staub und Fusseln bringen keine SP
def test_SPIEL_T20_staub_bringt_keine_sp(spiel):
    spiel.aufsatz_waehlen(AUFSATZ_STAUB)

    spiel.aktion_ausfuehren("Saugen")

    assert spiel.highscore.punkte == 0


# SPIEL-T21: Für einen Fleck wird eine Einheit Spülmittel verbraucht
def test_SPIEL_T21_fleck_verbraucht_spuelmittel(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=100, spuelmittel=2)

    spiel.aktion_ausfuehren("Wischen")

    assert spiel.roboter.ausruestung.spuelmittel == 1


# SPIEL-T30: Spülmittel wird auf vier Einheiten aufgefüllt
def test_SPIEL_T30_spuelmittel_auffuellen(spiel):
    text = meldungstext(spiel.spuelmittel_auffuellen())

    assert "4 Einheiten Spülmittel nachgefüllt" in text
    assert spiel.roboter.ausruestung.spuelmittel == 4


# SPIEL-T31: Ein teilweise gefüllter Bestand wird nur ergänzt
def test_SPIEL_T31_auffuellen_ergaenzt_nur(punktedatei):
    spiel = neues_spiel(punktedatei, spuelmittel=3)

    text = meldungstext(spiel.spuelmittel_auffuellen())

    assert "1 Einheiten Spülmittel nachgefüllt" in text
    assert spiel.roboter.ausruestung.spuelmittel == 4


# SPIEL-T32: Ein voller Bestand wird nicht überschritten
def test_SPIEL_T32_auffuellen_bei_vollem_bestand(punktedatei):
    spiel = neues_spiel(punktedatei, spuelmittel=4)

    text = meldungstext(spiel.spuelmittel_auffuellen())

    assert "bereits voll" in text
    assert spiel.roboter.ausruestung.spuelmittel == 4


# SPIEL-T22: Ohne Spülmittel sucht der Roboter danach
def test_SPIEL_T22_roboter_sucht_spuelmittel(spiel):
    assert spiel.roboter.ausruestung.spuelmittel == 0

    text = meldungstext(spiel.aktion_ausfuehren("Wischen"))

    assert "sucht Spülmittel" in text
    assert "Fleck beseitigt" in text


# SPIEL-T23: Ist nichts zu tun, wird das gemeldet
def test_SPIEL_T23_meldung_wenn_nichts_zu_tun(spiel):
    spiel.aktion_ausfuehren("Wischen")  # der Fleck ist danach weg

    assert "nichts zu wischen" in meldungstext(spiel.aktion_ausfuehren("Wischen"))


# SPIEL-T33: Eine Aktion ohne Arbeit kostet keinen Akku
def test_SPIEL_T33_aktion_ohne_arbeit_kostet_nichts(spiel):
    spiel.aktion_ausfuehren("Wischen")  # der Fleck ist danach weg
    vorher = spiel.akku.akkustand

    text = meldungstext(spiel.aktion_ausfuehren("Wischen"))

    assert spiel.akku.akkustand == vorher
    assert "Kein Akku verbraucht." in text
    assert "Wischen beendet" not in text


# SPIEL-T34: Saugen ohne Aufsatz kostet keinen Akku
def test_SPIEL_T34_saugen_ohne_aufsatz_kostet_nichts(spiel):
    vorher = spiel.akku.akkustand

    text = meldungstext(spiel.aktion_ausfuehren("Saugen"))

    assert spiel.akku.akkustand == vorher
    assert "Kein Aufsatz gewählt" in text
    assert "Kein Akku verbraucht." in text


# SPIEL-T35: Passt kein Aufsatz zu den Verschmutzungen, bleibt der Akku voll
def test_SPIEL_T35_nur_falscher_aufsatz_kostet_nichts(punktedatei):
    spiel = neues_spiel(punktedatei, akkustand=100)
    spiel.raum_wechseln("Bad")  # im Bad liegt nur eine Staubansammlung
    spiel.aufsatz_waehlen(1)  # Aufsatz fuer Fusseln, passt nicht
    vorher = spiel.akku.akkustand

    text = meldungstext(spiel.aktion_ausfuehren("Saugen"))

    assert "Falscher Aufsatz" in text
    assert spiel.akku.akkustand == vorher
    assert "Kein Akku verbraucht." in text


# SPIEL-T36: Spülen ohne erreichbares Spülmittel kostet keinen Akku
def test_SPIEL_T36_spuelen_ohne_spuelmittel_kostet_nichts(spiel):
    for x, y in spiel.karte.suchen(karte.SPUELMITTEL):
        spiel.karte.feld_leeren(x, y)  # kein Vorrat mehr in der Wohnung
    vorher = spiel.akku.akkustand

    text = meldungstext(spiel.aktion_ausfuehren("Spülen"))

    assert "Spülen nicht möglich!" in text
    assert spiel.akku.akkustand == vorher
    assert "Kein Akku verbraucht." in text


# SPIEL-T24: Gegenstände auf dem Weg werden automatisch aufgenommen
def test_SPIEL_T24_gegenstaende_werden_aufgenommen(spiel):
    ladekabel = spiel.karte.suchen(karte.LADEKABEL)[0]

    text = meldungstext(spiel._fahren_nach(ladekabel))

    assert "Ladekabel aufgenommen" in text
    assert spiel.roboter.ausruestung.ladekabel == 1


# SPIEL-T25: Eine unbekannte Aktion wird abgelehnt
def test_SPIEL_T25_unbekannte_aktion(spiel):
    assert spiel.aktion_ausfuehren("Springen") == ["Aktion nicht möglich!"]


# ==================== Auftragsreihenfolge (#24) ====================


# SPIEL-T26: Bei Saugen und Wischen wird zuerst gesaugt
def test_SPIEL_T26_zuerst_saugen_dann_wischen(spiel):
    spiel.aufsatz_waehlen(AUFSATZ_FUSSELN)

    text = meldungstext(spiel.auftrag_ausfuehren(["Wischen", "Saugen"]))

    assert text.index("Saugen beendet") < text.index("Wischen beendet")


# ==================== Speichern (#20, #31, #32) ====================


# SPIEL-T27: Beim Beenden werden die Punkte des Nutzers gespeichert
def test_SPIEL_T27_beenden_speichert_punkte(spiel, punktedatei):
    spiel.aktion_ausfuehren("Wischen")  # +2 SP
    spiel.beenden()

    with open(punktedatei, encoding="utf-8") as datei:
        gespeichert = json.load(datei)

    assert gespeichert == [{"name": "Tester", "punkte": 2}]


# SPIEL-T28: Ein gespeicherter Punktestand wird übernommen
def test_SPIEL_T28_gespeicherte_punkte_werden_geladen(punktedatei):
    spiel = neues_spiel(punktedatei, punkte=7)

    assert spiel.highscore.punkte == 7
    assert "SP: 7" in spiel.statuszeile()


# SPIEL-T29: Das Profil enthält den vollständigen Roboterzustand
def test_SPIEL_T29_profil_daten(spiel):
    daten = spiel.profil_daten()

    assert daten["akkustand"] == 100
    assert daten["letzte_wartung"] == "2026-09-09"
    assert daten["punkte"] == 0
    assert daten["spuelmittel"] == 0
    assert "zyklen_zaehler" in daten
    assert "verbrauchte_kapazitaet" in daten
