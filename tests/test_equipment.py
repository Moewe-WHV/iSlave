import pytest

import karte
from equipment import AUFSATZ_FUSSELN, AUFSATZ_STAUB, MAX_SPUELMITTEL, Ausruestung


@pytest.fixture
def ausruestung():
    return Ausruestung()


# ==================== Testfälle aus EQUIPMENT1 (#26) ====================


# EQ1-T01: Eine neue Ausrüstung hat kein Spülmittel
def test_EQ1_T01_start_ohne_spuelmittel(ausruestung):
    assert ausruestung.spuelmittel == 0
    assert not ausruestung.hat_spuelmittel()


# EQ1-T02: Spülmittel wird aufgenommen
def test_EQ1_T02_spuelmittel_aufnehmen(ausruestung):
    assert ausruestung.spuelmittel_aufnehmen() is True
    assert ausruestung.spuelmittel == 1
    assert ausruestung.hat_spuelmittel()


# EQ1-T03: Maximal vier Einheiten gleichzeitig
def test_EQ1_T03_maximal_vier_einheiten(ausruestung):
    for _ in range(MAX_SPUELMITTEL):
        assert ausruestung.spuelmittel_aufnehmen() is True

    assert ausruestung.spuelmittel == 4
    assert ausruestung.ist_voll()


# EQ1-T04: Ist der Bestand voll, wird kein weiteres Spülmittel aufgenommen
def test_EQ1_T04_kein_spuelmittel_bei_vollem_bestand():
    ausruestung = Ausruestung(spuelmittel=MAX_SPUELMITTEL)

    assert ausruestung.spuelmittel_aufnehmen() is False
    assert ausruestung.spuelmittel == 4


# EQ1-T05: Für eine Reinigung wird genau eine Einheit verbraucht
def test_EQ1_T05_eine_einheit_pro_reinigung():
    ausruestung = Ausruestung(spuelmittel=2)

    assert ausruestung.spuelmittel_verbrauchen() is True
    assert ausruestung.spuelmittel == 1


# EQ1-T06: Ohne Bestand kann nichts verbraucht werden
def test_EQ1_T06_kein_verbrauch_ohne_bestand(ausruestung):
    assert ausruestung.spuelmittel_verbrauchen() is False
    assert ausruestung.spuelmittel == 0


# EQ1-T07: Volles Spülmittel bleibt liegen und wird gemeldet
def test_EQ1_T07_meldung_bei_vollem_bestand():
    ausruestung = Ausruestung(spuelmittel=MAX_SPUELMITTEL)

    meldung = ausruestung.gegenstand_aufnehmen(karte.SPUELMITTEL)

    assert "bleibt liegen" in meldung


# ==================== Testfälle aus EQUIPMENT2 (#27) ====================


# EQ2-T01: Zu Beginn ist kein Aufsatz gewählt
def test_EQ2_T01_kein_aufsatz_zu_beginn(ausruestung):
    assert ausruestung.aufsatz is None


# EQ2-T02: Aufsatz 1 und 2 können gewählt werden
def test_EQ2_T02_beide_aufsaetze_waehlbar(ausruestung):
    assert ausruestung.aufsatz_waehlen(AUFSATZ_FUSSELN) is True
    assert ausruestung.aufsatz == AUFSATZ_FUSSELN

    assert ausruestung.aufsatz_waehlen(AUFSATZ_STAUB) is True
    assert ausruestung.aufsatz == AUFSATZ_STAUB


# EQ2-T03: Ein nicht vorhandener Aufsatz wird abgelehnt
def test_EQ2_T03_unbekannter_aufsatz_wird_abgelehnt(ausruestung):
    assert ausruestung.aufsatz_waehlen(3) is False
    assert ausruestung.aufsatz is None


# EQ2-T04: Der Roboter erkennt selbstständig den passenden Aufsatz
def test_EQ2_T04_passender_aufsatz_wird_erkannt(ausruestung):
    assert ausruestung.passender_aufsatz(karte.FUSSEL) == AUFSATZ_FUSSELN
    assert ausruestung.passender_aufsatz(karte.STAUB) == AUFSATZ_STAUB


# EQ2-T05: Aufsatz 1 passt zu Fusseln, nicht zu Staub
def test_EQ2_T05_aufsatz_1_passt_nur_zu_fusseln(ausruestung):
    ausruestung.aufsatz_waehlen(AUFSATZ_FUSSELN)

    assert ausruestung.aufsatz_passt(karte.FUSSEL) is True
    assert ausruestung.aufsatz_passt(karte.STAUB) is False


# EQ2-T06: Aufsatz 2 passt zu Staubansammlungen, nicht zu Fusseln
def test_EQ2_T06_aufsatz_2_passt_nur_zu_staub(ausruestung):
    ausruestung.aufsatz_waehlen(AUFSATZ_STAUB)

    assert ausruestung.aufsatz_passt(karte.STAUB) is True
    assert ausruestung.aufsatz_passt(karte.FUSSEL) is False


# ==================== Testfälle aus EQUIPMENT3 (#28) ====================


# EQ3-T01: Ein Ladekabel wird aufgenommen
def test_EQ3_T01_ladekabel_aufnehmen(ausruestung):
    meldung = ausruestung.gegenstand_aufnehmen(karte.LADEKABEL)

    assert ausruestung.ladekabel == 1
    assert "Ladekabel" in meldung


# EQ3-T02: Ein Werkzeug wird aufgenommen
def test_EQ3_T02_werkzeug_aufnehmen(ausruestung):
    meldung = ausruestung.gegenstand_aufnehmen(karte.WERKZEUG)

    assert ausruestung.werkzeuge == 1
    assert "Werkzeug" in meldung


# EQ3-T03: Mehrere Gegenstände werden gezählt
def test_EQ3_T03_mehrere_gegenstaende_werden_gezaehlt(ausruestung):
    ausruestung.gegenstand_aufnehmen(karte.LADEKABEL)
    ausruestung.gegenstand_aufnehmen(karte.LADEKABEL)
    ausruestung.gegenstand_aufnehmen(karte.WERKZEUG)

    assert ausruestung.ladekabel == 2
    assert ausruestung.werkzeuge == 1


# EQ3-T04: Eine Verschmutzung ist kein aufnehmbarer Gegenstand
def test_EQ3_T04_verschmutzung_wird_nicht_aufgenommen(ausruestung):
    assert ausruestung.gegenstand_aufnehmen(karte.FLECK) == ""
    assert ausruestung.ladekabel == 0
    assert ausruestung.werkzeuge == 0


# EQ3-T05: Die Zustandszeile nennt Bestand und Aufsatz
def test_EQ3_T05_zustandszeile_zeigt_bestand(ausruestung):
    ausruestung.aufsatz_waehlen(AUFSATZ_STAUB)
    ausruestung.spuelmittel_aufnehmen()

    zeile = ausruestung.als_text()

    assert "1/4" in zeile
    assert "Aufsatz 2" in zeile
