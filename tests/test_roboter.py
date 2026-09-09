import pytest

from equipment import Ausruestung
from roboter import NORDEN, OSTEN, SUEDEN, WESTEN, Roboter


@pytest.fixture
def roboter():
    return Roboter((5, 5))


# ROB-T01: Der Roboter kennt seine Startposition
def test_ROB_T01_startposition(roboter):
    assert roboter.position == (5, 5)
    assert roboter.x == 5
    assert roboter.y == 5


# ROB-T02: Ohne eigene Ausrüstung bekommt der Roboter eine leere
def test_ROB_T02_hat_immer_eine_ausruestung(roboter):
    assert isinstance(roboter.ausruestung, Ausruestung)
    assert roboter.ausruestung.spuelmittel == 0


# ROB-T03: Eine vorhandene Ausrüstung wird übernommen
def test_ROB_T03_ausruestung_wird_uebernommen():
    ausruestung = Ausruestung(spuelmittel=3)
    roboter = Roboter((1, 1), ausruestung)

    assert roboter.ausruestung is ausruestung
    assert roboter.ausruestung.spuelmittel == 3


# ROB-T04: Bewegung setzt Position und Blickrichtung
def test_ROB_T04_bewegung_setzt_blickrichtung(roboter):
    roboter.bewegen_nach((5, 4))

    assert roboter.position == (5, 4)
    assert roboter.blickrichtung == NORDEN


# ROB-T05: Alle vier Richtungen werden erkannt
def test_ROB_T05_alle_richtungen(roboter):
    roboter.bewegen_nach((6, 5))
    assert roboter.blickrichtung == OSTEN

    roboter.bewegen_nach((6, 6))
    assert roboter.blickrichtung == SUEDEN

    roboter.bewegen_nach((5, 6))
    assert roboter.blickrichtung == WESTEN

    roboter.bewegen_nach((5, 5))
    assert roboter.blickrichtung == NORDEN


# ROB-T06: Ein Sprung über mehrere Felder ändert die Blickrichtung nicht
def test_ROB_T06_sprung_behaelt_blickrichtung(roboter):
    vorher = roboter.blickrichtung
    roboter.bewegen_nach((9, 9))

    assert roboter.position == (9, 9)
    assert roboter.blickrichtung == vorher


# ROB-T07: Beim Raumwechsel wird der Roboter versetzt
def test_ROB_T07_versetzen_beim_raumwechsel(roboter):
    roboter.versetzen_nach((13, 1))

    assert roboter.position == (13, 1)


# ROB-T08: Die Zustandszeile nennt Position und Blickrichtung
def test_ROB_T08_zustandszeile(roboter):
    zeile = roboter.als_text()

    assert "(5, 5)" in zeile
    assert roboter.blickrichtung in zeile
