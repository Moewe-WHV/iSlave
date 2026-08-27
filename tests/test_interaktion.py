from src.raeume import Raumsteuerung
from src.aktionen import RoboterAktionen
from src.interaktion import (verfuegbare_raeume_anzeigen, raum_auswaehlen, terminal_raeume_anzeigen, raum_dialog, aktion_auswaehlen) 


def test_terminal_zeigt_verfuegbare_raeume():
    raumsteuerung = Raumsteuerung()
    ergebnis = verfuegbare_raeume_anzeigen(raumsteuerung)
    assert ergebnis == ["Wohnzimmer", "Bad", "Küche", "Schlafzimmer"]

def test_gewaelter_raum_wird_an_raumsteuerung_uebergeben():
    raumsteuerung = Raumsteuerung()
    ergebnis = raum_auswaehlen(raumsteuerung, "Wohnzimmer")
    assert ergebnis == "Wohnzimmer"

def test_terminal_zeigt_raeume_als_text_an():
    raumsteuerung = Raumsteuerung

    ergebnis = terminal_raeume_anzeigen(raumsteuerung)

    assert "Wohnzimmer" in ergebnis
    assert "Bad"in ergebnis
    assert "Küche" in ergebnis
    assert "Schlafzimmer" in ergebnis

def test_benutzereingabe_waehlt_wohnzimmer():
    raumsteuerung = Raumsteuerung()
    ergebnis = raum_auswaehlen(raumsteuerung, "Wohnzimmer")
    assert ergebnis == "Wohnzimmer"
    assert raumsteuerung.aktueller_raum == "Wohnzimmer"

def test_raum_dialog_gibt_gewaehlten_raum_zurueck():
    raumsteuerung = Raumsteuerung()
    ergebnis = raum_dialog(raumsteuerung, "Wohnzimmer")
    assert ergebnis == "Wohnzimmer"

def test_aktion_wird_an_aktionen_uebergeben():
    aktionen = RoboterAktionen()
    ergebnis = aktion_auswaehlen(aktionen, "Spülmittel")
    assert ergebnis == "Spülmittel"

def test_aktion_auswaehlen_mit_roboter_aktionen_klasse():
    aktionen = RoboterAktionen()
    ergebnis = aktion_auswaehlen(aktionen, "Spülmittel")
    assert ergebnis == "Spülmittel"

def test_aktuelle_aktion_wird_gespeichert():

    aktionen = RoboterAktionen()
    aktionen.aktion_ausfuehren("Spülmittel")
    assert aktionen.aktuelle_aktion == "Spülmittel"




        

