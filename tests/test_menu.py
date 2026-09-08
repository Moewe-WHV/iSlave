from src.interaktion import menu_auswahl
from src.interaktion import weitere_aktion_auswaehlen


def test_menu_auftrag_straten():
    ergebnis = menu_auswahl("1")
    assert ergebnis == "auftrag"


def test_menu_beenden():
    ergebnis = menu_auswahl("0")
    assert ergebnis == "beenden"


def test_menu_laeuft_nach_falscher_eingabe_weiter():
    ergebnis = menu_auswahl("9")
    assert ergebnis == "Falsche Eingabe!"


def test_weitere_aktion_ja():
    ergebnis = weitere_aktion_auswaehlen("j")
    assert ergebnis is True


def test_weitere_aktion_nein():
    ergebnis = weitere_aktion_auswaehlen("n")
    assert ergebnis is False
