from src.aktionen import RoboterAktionen


def test_staubsauger_aktion_ausfuehren():
    roboteraktion = RoboterAktionen()
    ergebnis = roboteraktion.aktion_ausfuehren("Staubsaugeraufsätze")
    assert ergebnis == "Staubsaugeraufsätze"


def test_spuellmittel_aktion_ausfuehren():
    roboteraktion = RoboterAktionen()
    ergebnis = roboteraktion.aktion_ausfuehren("Spülmittel")
    assert ergebnis == "Spülmittel"


def test_unbekante_aktion_wird_abgelehnt():
    roboteraktion = RoboterAktionen()

    ergebnis = roboteraktion.aktion_ausfuehren("Springen")
    assert ergebnis == "Aktion nicht möglich!"
