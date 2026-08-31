import os
import sys
import unittest
from unittest.mock import patch
from src.highscore import Highscore

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


class TestHighscore(unittest.TestCase):

    def setUp(self):
        """Wird vor jedem einzelnen Test ausgeführt."""
        self.test_datei = "test_highscores.json"
        # Saubere Instanz für jeden Test mit temporärer Testdatei
        self.hs = Highscore(dateiname=self.test_datei)

    def tearDown(self):
        """Wird nach jedem Test ausgeführt, um Testdateien zu bereinigen."""
        if os.path.exists(self.test_datei):
            os.remove(self.test_datei)

    def test_high_t01_neuen_nutzer_erstellen(self):
        """HIGH-T01: Neuen Nutzer erstellen -> Highscore startet bei 0 SP."""
        self.assertEqual(self.hs.punkte, 0)

    def test_high_t02_einen_fleck_reinigen(self):
        """HIGH-T02: Einen Fleck reinigen -> Highscore steigt um 2 SP."""
        start_punkte = self.hs.punkte
        self.hs.fleck_reinigen()
        self.assertEqual(self.hs.punkte, start_punkte + 2)

    def test_high_t03_eine_wolllaus_besiegen(self):
        """HIGH-T03: Eine Wolllaus besiegen -> Highscore steigt um 1 SP."""
        start_punkte = self.hs.punkte
        self.hs.wolllaus_besiegen()
        self.assertEqual(self.hs.punkte, start_punkte + 1)

    def test_high_t04_ein_staubmonster_besiegen(self):
        """HIGH-T04: Ein Staubmonster besiegen -> Highscore steigt um 2 SP."""
        start_punkte = self.hs.punkte
        self.hs.staubmonster_besiegen()
        self.assertEqual(self.hs.punkte, start_punkte + 2)

    def test_high_t05_nutzerwechsel_getrennte_highscores(self):
        """
        HIGH-T05: Zu Nutzer A wechseln und anschließend zu Nutzer B wechseln
        -> Jeder Nutzer sieht seinen eigenen Highscore.
        """
        # Nutzer A spielt
        spieler_a = Highscore(dateiname=self.test_datei)
        spieler_a.fleck_reinigen()  # +2 SP
        with patch("builtins.input", return_value="Nutzer A"):
            spieler_a.spiel_beenden_und_speichern()

        # Nutzer B spielt separat
        spieler_b = Highscore(dateiname=self.test_datei)
        spieler_b.wolllaus_besiegen()  # +1 SP
        spieler_b.staubmonster_besiegen()  # +2 SP (Gesamt: 3 SP)
        with patch("builtins.input", return_value="Nutzer B"):
            spieler_b.spiel_beenden_und_speichern()

        # Überprüfung der gespeicherten Punktestände der beiden Nutzer
        scores = self.hs.alle_highscores_laden()
        scores_dict = {eintrag["name"]: eintrag["punkte"] for eintrag in scores}

        self.assertEqual(scores_dict.get("Nutzer A"), 2)
        self.assertEqual(scores_dict.get("Nutzer B"), 3)


if __name__ == "__main__":
    unittest.main()
