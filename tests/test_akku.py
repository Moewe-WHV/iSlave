import io
import unittest
from contextlib import redirect_stdout

from src.akku1 import Akku


class TestAkku(unittest.TestCase):

    # ==================== Testfälle aus AKKU1 ====================

    # AKKU1-T01: Akkustand bei 100 % anzeigen
    def test_AKKU1_T01_akkustand_100_anzeigen(self):
        akku = Akku(100)
        output = io.StringIO()
        with redirect_stdout(output):
            stand = akku.akkustand_anzeigen()

        self.assertEqual(stand, 100)
        self.assertIn("Akkustand: 100%", output.getvalue())

    # AKKU1-T02: Akkustand bei 50 % anzeigen
    def test_AKKU1_T02_akkustand_50_anzeigen(self):
        akku = Akku(50)
        output = io.StringIO()
        with redirect_stdout(output):
            stand = akku.akkustand_anzeigen()

        self.assertEqual(stand, 50)
        self.assertIn("Akkustand: 50%", output.getvalue())

    # AKKU1-T03: Akkuverbrauch durch Aufgabe (Verbrauch 10 %)
    def test_AKKU1_T03_akkuverbrauch_durch_aufgabe(self):
        akku = Akku(100)
        output = io.StringIO()
        with redirect_stdout(output):
            akku.verbrauchen(10)

        self.assertEqual(akku.akkustand, 90)
        self.assertIn("Akkustand: 90%", output.getvalue())

    # AKKU1-T04: Mehrere Aufgaben nacheinander ausführen
    def test_AKKU1_T04_mehrere_aufgaben_ausfuehren(self):
        akku = Akku(100)

        # Erste Aufgabe ausführen (15 % Standardverbrauch)
        akku.aufgabe()
        self.assertEqual(akku.akkustand, 85)

        # Zweite Aufgabe ausführen (15 % Standardverbrauch)
        akku.aufgabe()
        self.assertEqual(akku.akkustand, 70)

    # AKKU1-T05: Akkustand nach Neustart (gespeicherter Stand z. B. 60 %)
    def test_AKKU1_T05_akkustand_nach_neustart(self):
        gespeicherter_akkustand = 60
        akku_neustart = Akku(gespeicherter_akkustand)
        output = io.StringIO()

        with redirect_stdout(output):
            stand = akku_neustart.akkustand_anzeigen()

        self.assertEqual(stand, 60)
        self.assertEqual(akku_neustart.akkustand, 60)
        self.assertIn("Akkustand: 60%", output.getvalue())

    # ==================== Testfälle aus AKKU2 ====================

    # AKKU2-T01: Ladezyklus vollständig durchführen (0 % auf 100 %)
    def test_AKKU2_T01_ladezyklus_vollstaendig(self):
        akku = Akku(0)
        geladen, zyklen_zaehler, neuer_akkustand = akku.laden(akku.akkustand)

        self.assertEqual(geladen, 100)
        self.assertEqual(neuer_akkustand, 100)
        self.assertIsNotNone(zyklen_zaehler)

    # AKKU2-T02: Unvollständiges Laden (50 % ohne Force-Laden -> kein Ladevorgang)
    def test_AKKU2_T02_unvollstaendiges_laden(self):
        akku = Akku(50)
        ergebnis = akku.laden(akku.akkustand, batterie_laden=False)

        self.assertIsNone(ergebnis)

    # AKKU2-T03: Ladezyklen im Terminal anzeigen (z. B. 5 Zyklen)
    def test_AKKU2_T03_ladezyklen_anzeigen(self):
        akku = Akku(100)
        zyklen = 5
        output = io.StringIO()

        with redirect_stdout(output):
            akku.zyklen_anzeigen(zyklen)

        self.assertIn("5/500", output.getvalue())

    # AKKU2-T04: Verschleißgrenze bei >= 495 Zyklen
    def test_AKKU2_T04_verschleissgrenze(self):
        akku = Akku(95)
        output = io.StringIO()

        # Laden von 95 % auf 100 % -> zyklen_zaehler = 500 - (100 - 95) = 495
        with redirect_stdout(output):
            geladen, zyklen_zaehler, _ = akku.laden(
                akku.akkustand, batterie_laden=True
            )

        self.assertEqual(zyklen_zaehler, 495)
        self.assertIn(
            "Achtung: Die Batterie ist fast am Ende ihrer Lebensdauer!",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()