from datetime import date
from src.wartung import (
    berechne_naechste_wartung,
    ist_wartung_faellig,
    berechne_verbleibende_tage,
    erstelle_wartungsmeldung,
)


def test_berechne_naechste_wartung_nach_zwei_jahren():
    letzte_wartung = date(2024, 8, 18)

    ergebnis = berechne_naechste_wartung(letzte_wartung)

    assert ergebnis == date(2026, 8, 18)


def test_wartung_ist_am_wartungstermin_faellig():
    wartungstermin = date(2026, 8, 18)
    aktuelles_datum = date(2026, 8, 18)

    ergebnis = ist_wartung_faellig(wartungstermin, aktuelles_datum)

    assert ergebnis is True


def test_wartung_ist_vor_dem_wartungstermin_nicht_faellig():
    wartungstermin = date(2026, 8, 18)
    aktuelles_datum = date(2026, 8, 17)

    ergebnis = ist_wartung_faellig(wartungstermin, aktuelles_datum)

    assert ergebnis is False


def test_verbleibende_tage_bis_zur_wartung():
    wartungstermin = date(2026, 8, 18)
    aktuelles_datum = date(2026, 8, 10)

    ergebnis = berechne_verbleibende_tage(wartungstermin, aktuelles_datum)

    assert ergebnis == 8


def test_verbleibende_tage_sind_nach_faelligkeit_null():
    wartungstermin = date(2026, 8, 18)
    aktuelles_datum = date(2026, 8, 20)

    ergebnis = berechne_verbleibende_tage(wartungstermin, aktuelles_datum)

    assert ergebnis == 0


def test_meldung_wenn_wartung_faellig_ist():
    wartungstermin = date(2026, 8, 18)
    aktuelles_datum = date(2026, 8, 18)

    ergebnis = erstelle_wartungsmeldung(wartungstermin, aktuelles_datum)

    assert ergebnis == ("Wartung fällig. Der Roboter kann nicht mehr genutzt werden.")


def test_meldung_wenn_wartung_noch_nicht_faellig_ist():
    wartungstermin = date(2026, 8, 18)
    aktuelles_datum = date(2026, 8, 10)

    ergebnis = erstelle_wartungsmeldung(wartungstermin, aktuelles_datum)

    assert ergebnis == ("Nächste Wartung: 18.08.2026. " "Verbleibende Tage: 8.")
