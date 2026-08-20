from akku_1_b import Akku  # Importiere deine Akku-Klasse aus akku.py


def test_tf01_anzeige_in_prozent():
    akku = Akku(100)
    ergebnis = akku.akkustand_anzeigen()
    assert ergebnis == 100


def test_tf02_aktualisierung_nach_aktion():
    akku = Akku(100)
    akku.aufgabe()
    assert akku.akkustand == 85
    assert akku.akkustand != 100


def test_tf03_fester_verbrauch_pro_aufgabe():
    akku = Akku(100)
    akku.aufgabe()
    assert akku.akkustand == 100 - 15  # exakt 15% Verbrauch


def test_tf04_sperre_unter_20_prozent(capsys):
    akku = Akku(15)
    akku.aufgabe()
    ausgabe = capsys.readouterr().out
    assert akku.akkustand == 15  # Akkustand unverändert
    assert "Akku zu niedrig, Aufgabe kann nicht ausgeführt werden." in ausgabe


def test_tf05_warnmeldung_unter_20_prozent(capsys):
    akku = Akku(30)
    akku.aufgabe()
    ausgabe = capsys.readouterr().out
    assert akku.akkustand == 15
    assert "Warnung: Akku unter 20%! Roboter muss geladen werden." in ausgabe


def test_tf06_grenzfall_exakt_20_prozent(capsys):
    akku = Akku(20)
    akku.aufgabe()
    ausgabe = capsys.readouterr().out
    assert akku.akkustand == 5  # Aufgabe wurde ausgeführt (>=20 erlaubt)
    assert "Warnung: Akku unter 20%! Roboter muss geladen werden." in ausgabe