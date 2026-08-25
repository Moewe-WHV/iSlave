from src.raeume import Raumsteuerung


def test_roboter_kann_ins_wohnzimmer_wechseln():
    raumsteuerung = Raumsteuerung()
    ergebnis = raumsteuerung.raum_wechseln("Wohnzimmer")
    assert ergebnis == "Wohnzimmer"


def test_roboter_kann_in_die_kueche_wechseln():
    raumsteuerung = Raumsteuerung()
    ergebnis = raumsteuerung.raum_wechseln("Küche")
    assert ergebnis == "Küche"


def test_roboter_kann_in_die_schlafzimmer_wechseln():
    raumsteuerung = Raumsteuerung()
    ergebnis = raumsteuerung.raum_wechseln("Schlafzimmer")
    assert ergebnis == "Schlafzimmer"


def test_roboter_kann_in_die_bad_wechseln():
    raumsteuerung = Raumsteuerung()
    ergebnis = raumsteuerung.raum_wechseln("Bad")
    assert ergebnis == "Bad"


def test_nicht_existierender_raum_wird_abgelehnt():
    raumsteuerung = Raumsteuerung()
    ergebnis = raumsteuerung.raum_wechseln("Garage")
    assert ergebnis == "Raum nicht vorhanden!"


def test_verfuegbare_raeume_werden_angezeigt():
    raumsteuerung = Raumsteuerung()
    ergebnis = raumsteuerung.gueltige_raeume
    assert ergebnis == ["Wohnzimmer", "Bad", "Küche", "Schlafzimmer"]


def test_nach_raum_wechsel_ist_zielraum_aktueller_raum():
    raumsteuerung = Raumsteuerung()
    raumsteuerung.raum_wechseln("Wohnzimmer")
    ergebnis = raumsteuerung.aktueller_raum
    assert ergebnis == "Wohnzimmer"


def test_ungueltiger_raum_aendert_aktuellen_raum_nicht():
    raumsteuerung = Raumsteuerung()
    raumsteuerung.raum_wechseln("Küche")
    raumsteuerung.raum_wechseln("Garage")
    ergebnis = raumsteuerung.aktueller_raum
    assert ergebnis == "Küche"
