from src.aktionen import RoboterAktionen


def test_saugen_aktion_ausfuehren():
    roboteraktion = RoboterAktionen()
    ergebnis = roboteraktion.aktion_ausfuehren("Saugen")
    assert ergebnis == "Saugen"


def test_spuelen_aktion_ausfuehren():
    roboteraktion = RoboterAktionen()
    ergebnis = roboteraktion.aktion_ausfuehren("Spülen")
    assert ergebnis == "Spülen"


def test_unbekante_aktion_wird_abgelehnt():
    roboteraktion = RoboterAktionen()

    ergebnis = roboteraktion.aktion_ausfuehren("Springen")
    assert ergebnis == "Aktion nicht möglich!"


def test_wischen_ist_gueltige_aktion():
    aktionen = RoboterAktionen()

    assert "Wischen" in aktionen.gueltige_aktionen


def test_gleiche_aktion_nicht_zweimal_erlaubt():
    aktionen = RoboterAktionen()
    ausgewaehlte_aktionen = ["Wischen"]

    ergebnis = aktionen.aktionen_bereits_gewaehlt(ausgewaehlte_aktionen, "Wischen")

    assert ergebnis is True


def test_andere_aktion_ist_noch_nicht_gewaehlt():
    aktionen = RoboterAktionen()
    ausgewaehlte_aktionen = ["Wischen"]

    ergebnis = aktionen.aktionen_bereits_gewaehlt(ausgewaehlte_aktionen, "Spülen")

    assert ergebnis is False


def test_saugen_wird_vor_wischen_ausgefuehrt():
    aktionen = RoboterAktionen()
    ausgewaehlte_aktionen = ["Wischen", "Saugen"]

    ergebnis = aktionen.reihenfolge_festlegen(ausgewaehlte_aktionen)

    assert ergebnis == ["Saugen", "Wischen"]
