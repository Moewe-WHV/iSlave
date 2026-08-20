import io
import unittest
from contextlib import redirect_stdout
from Akku2 import Akku


class TestAkku(unittest.TestCase):

    def setUp(self):
        self.akku = Akku()

    # AKKU2-T01: Ladezyklus vollständig durchführen (0% auf 100%)
    def test_AKKU2_T01_ladezyklus_vollstaendig(self):
        akkustand = 0
        geladen, zyklen_zaehler, neuer_akkustand = self.akku.laden(akkustand)

        self.assertEqual(geladen, 100)
        self.assertEqual(neuer_akkustand, 100)
        self.assertIsNotNone(zyklen_zaehler)

    # AKKU2-T02: Unvollständiges Laden (z. B. bei 50% ohne Force-Laden)
    def test_AKKU2_T02_unvollstaendiges_laden(self):
        akkustand = 50
        ergebnis = self.akku.laden(akkustand, batterie_laden=False)

        # Da akkustand >= min_akkustand (20), wird kein Ladevorgang ausgeführt
        self.assertIsNone(ergebnis)

    # AKKU2-T03: Ladezyklen im Terminal anzeigen
    def test_AKKU2_T03_ladezyklen_anzeigen(self):
        zyklen = 5
        output = io.StringIO()

        with redirect_stdout(output):
            self.akku.zyklen_anzeigen(zyklen)

        self.assertIn("5/500", output.getvalue())

    # AKKU2-T04: Verschleißgrenze bei >= 495 Zyklen
    def test_AKKU2_T04_verschleissgrenze(self):
        output = io.StringIO()

        # Beim Laden von z.B. 5% ergibt sich 500 - (100 - 5) = 405 (keine Warnung)
        # Ab 500 - (100 - akkustand) >= 495 (d.h. akkustand <= 5) wird die Warnung ausgegeben:
        akkustand = 0  # 500 - 100 = 400; oder erzwungen mit batterie_laden=True und akkustand=95 -> zyklen=495
        with redirect_stdout(output):
            geladen, zyklen_zaehler, _ = self.akku.laden(
                akkustand=95, batterie_laden=True
            )

        self.assertEqual(zyklen_zaehler, 495)
        self.assertIn(
            "Achtung: Die Batterie ist fast am Ende ihrer Lebensdauer!",
            output.getvalue(),
        )


if __name__ == "__main__":
    unittest.main()