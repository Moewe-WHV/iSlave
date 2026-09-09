"""Tests der Kartenansicht (#22).

Geprueft werden nur die reinen Hilfsfunktionen. Sie brauchen kein
Fenster, damit die Tests auch auf einem Rechner ohne Bildschirm laufen.

Ist Tkinter gar nicht installiert - wie auf dem CI-Runner -, wird die
ganze Datei uebersprungen. gui.py braucht Tkinter zwingend, main.py
faengt das Fehlen ab und laeuft dann nur im Terminal weiter.
"""

import pytest

pytest.importorskip("tkinter", reason="Tkinter ist nicht installiert")

import karte  # noqa: E402
from gui import (  # noqa: E402
    FARBEN,
    FELDGROESSE,
    RANDBREITE,
    ROBOTERFARBE,
    feld_farbe,
    feld_rechteck,
    leinwandgroesse,
    raumbeschriftungen,
)


# GUI-T01: Jedes Kartenzeichen hat eine eigene Farbe
def test_GUI_T01_jedes_zeichen_hat_eine_farbe():
    zeichen = [karte.WAND, karte.LEER, karte.MOEBEL]
    zeichen += karte.VERSCHMUTZUNGEN
    zeichen += karte.GEGENSTAENDE

    for eintrag in zeichen:
        assert eintrag in FARBEN
        assert feld_farbe(eintrag).startswith("#")


# GUI-T02: Unbekannte Zeichen bekommen die Farbe eines leeren Feldes
def test_GUI_T02_unbekanntes_zeichen_faellt_zurueck():
    assert feld_farbe("?") == FARBEN[karte.LEER]


# GUI-T03: Der Roboter hebt sich farblich von allen Feldern ab
def test_GUI_T03_roboterfarbe_ist_eigenstaendig():
    assert ROBOTERFARBE not in FARBEN.values()


# GUI-T04: Das erste Feld liegt am Rand
def test_GUI_T04_erstes_feld_liegt_am_rand():
    assert feld_rechteck(0, 0) == (
        RANDBREITE,
        RANDBREITE,
        RANDBREITE + FELDGROESSE,
        RANDBREITE + FELDGROESSE,
    )


# GUI-T05: Felder sind quadratisch und liegen nebeneinander
def test_GUI_T05_felder_liegen_nebeneinander():
    links, oben, rechts, unten = feld_rechteck(3, 2)

    assert rechts - links == FELDGROESSE
    assert unten - oben == FELDGROESSE
    assert links == feld_rechteck(2, 2)[2]


# GUI-T06: Die Zeichenfläche fasst die ganze Karte
def test_GUI_T06_leinwand_fasst_die_karte():
    breite, hoehe = leinwandgroesse()

    assert breite == 2 * RANDBREITE + karte.BREITE * FELDGROESSE
    assert hoehe == 2 * RANDBREITE + karte.HOEHE * FELDGROESSE


# GUI-T07: Alle vier Räume werden beschriftet
def test_GUI_T07_alle_raeume_werden_beschriftet():
    namen = [name for name, _, _ in raumbeschriftungen()]

    assert sorted(namen) == sorted(["Bad", "Küche", "Schlafzimmer", "Wohnzimmer"])


# GUI-T08: Die Beschriftung liegt innerhalb der Zeichenfläche
def test_GUI_T08_beschriftung_liegt_in_der_leinwand():
    breite, hoehe = leinwandgroesse()

    for _, x, y in raumbeschriftungen():
        assert 0 <= x <= breite
        assert 0 <= y <= hoehe
