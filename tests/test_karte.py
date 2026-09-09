import pytest

import karte
from karte import Karte


@pytest.fixture
def wohnung():
    return Karte()


# ==================== Testfälle aus UMGEBUNG1 (#29) ====================


# UMG1-T01: Die Karte ist rasterbasiert und hat eine feste Größe
def test_UMG1_T01_karte_ist_rasterbasiert(wohnung):
    assert len(wohnung.raster) == karte.HOEHE
    assert all(len(zeile) == karte.BREITE for zeile in wohnung.raster)


# UMG1-T02: Alle vier Räume sind vorhanden
def test_UMG1_T02_alle_vier_raeume_vorhanden():
    assert sorted(karte.RAEUME) == sorted(
        ["Bad", "Küche", "Schlafzimmer", "Wohnzimmer"]
    )


# UMG1-T03: Jeder Raum hat ein begehbares Startfeld
def test_UMG1_T03_startfeld_ist_begehbar(wohnung):
    for raum in karte.RAEUME:
        x, y = wohnung.startfeld(raum)
        assert wohnung.ist_begehbar(x, y)
        assert wohnung.raum_von(x, y) == raum


# UMG1-T04: Die Räume sind räumlich getrennt
def test_UMG1_T04_raeume_sind_durch_waende_getrennt(wohnung):
    # Zwischen Wohnzimmer (x <= 11) und Bad (x >= 13) liegt eine Wand
    assert wohnung.zeichen(12, 1) == karte.WAND
    # Zwischen Wohnzimmer (y <= 8) und Küche (y >= 10) liegt eine Wand
    assert wohnung.zeichen(1, 9) == karte.WAND


# UMG1-T05: Trotz Trennung ist jeder Raum durch Türen erreichbar
def test_UMG1_T05_alle_raeume_sind_erreichbar(wohnung):
    start = wohnung.startfeld("Wohnzimmer")
    for raum in karte.RAEUME:
        if raum == "Wohnzimmer":
            continue
        assert wohnung.weg_suchen(start, wohnung.startfeld(raum)) != []


# UMG1-T06: Die Textansicht zeigt den Roboter als R
def test_UMG1_T06_textansicht_zeigt_roboter(wohnung):
    ansicht = wohnung.als_text((1, 1))
    assert "R" in ansicht
    assert len(ansicht.splitlines()) == karte.HOEHE


# ==================== Testfälle aus UMGEBUNG2 (#30) ====================


# UMG2-T01: Möbel sind Hindernisse
def test_UMG2_T01_moebel_sind_hindernisse(wohnung):
    # Sofa im Wohnzimmer
    assert wohnung.zeichen(2, 2) == karte.MOEBEL
    assert wohnung.ist_hindernis(2, 2)
    assert not wohnung.ist_begehbar(2, 2)


# UMG2-T02: Wände sind Hindernisse, auch außerhalb der Karte
def test_UMG2_T02_waende_sind_hindernisse(wohnung):
    assert wohnung.ist_hindernis(0, 0)
    assert wohnung.zeichen(-1, -1) == karte.WAND


# UMG2-T03: Der Weg führt um Hindernisse herum
def test_UMG2_T03_weg_fuehrt_um_hindernisse(wohnung):
    weg = wohnung.weg_suchen((1, 1), (5, 1))
    assert weg != []
    assert all(wohnung.ist_begehbar(x, y) for x, y in weg)
    assert (2, 2) not in weg  # das Sofa wird nicht überfahren


# UMG2-T04: Ein Hindernis selbst ist kein gültiges Ziel
def test_UMG2_T04_hindernis_ist_kein_ziel(wohnung):
    assert wohnung.weg_suchen((1, 1), (2, 2)) == []


# UMG2-T05: Der Weg endet auf dem Zielfeld
def test_UMG2_T05_weg_endet_am_ziel(wohnung):
    ziel = (9, 7)
    weg = wohnung.weg_suchen((1, 1), ziel)
    assert weg[-1] == ziel


# UMG2-T06: Jeder Raum enthält Verschmutzungen
def test_UMG2_T06_jeder_raum_hat_verschmutzungen(wohnung):
    for raum in karte.RAEUME:
        assert wohnung.verschmutzungen_im_raum(raum) != []
        assert not wohnung.ist_sauber(raum)


# UMG2-T07: Beseitigte Verschmutzungen verschwinden von der Karte
def test_UMG2_T07_verschmutzung_wird_entfernt(wohnung):
    x, y = wohnung.verschmutzungen_im_raum("Wohnzimmer")[0]
    inhalt = wohnung.feld_leeren(x, y)

    assert inhalt in karte.VERSCHMUTZUNGEN
    assert wohnung.zeichen(x, y) == karte.LEER


# UMG2-T08: Ein Raum kann vollständig gereinigt werden
def test_UMG2_T08_raum_wird_sauber(wohnung):
    for x, y in wohnung.verschmutzungen_im_raum("Bad"):
        wohnung.feld_leeren(x, y)

    assert wohnung.ist_sauber("Bad")


# UMG2-T09: Spülmittel liegt in der Wohnung und ist auffindbar
def test_UMG2_T09_spuelmittel_ist_auffindbar(wohnung):
    vorraete = wohnung.suchen(karte.SPUELMITTEL)
    assert len(vorraete) >= 1
    assert all(wohnung.ist_begehbar(x, y) for x, y in vorraete)


# UMG2-T10: Möbelfelder werden nicht mit Inhalten überschrieben
def test_UMG2_T10_moebel_bleiben_frei_von_inhalten(wohnung):
    for x, y in wohnung.verschmutzungen_im_raum("Küche"):
        assert wohnung.zeichen(x, y) != karte.MOEBEL


# UMG2-T11: Nachbarfelder enthalten nur begehbare Felder
def test_UMG2_T11_nachbarfelder_sind_begehbar(wohnung):
    for x, y in wohnung.nachbarfelder(1, 1):
        assert wohnung.ist_begehbar(x, y)


# UMG2-T12: Ein unbekannter Raum liefert keine Felder
def test_UMG2_T12_unbekannter_raum_hat_keine_felder(wohnung):
    assert wohnung.felder_im_raum("Garage") == []
    assert wohnung.startfeld("Garage") is None
