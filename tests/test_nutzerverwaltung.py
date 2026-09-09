from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.nutzerverwaltung import (
    KeinNutzerAngemeldetError,
    NutzernameVergebenError,
    NutzerNichtGefundenError,
    Nutzerverwaltung,
    UngueltigerNutzernameError,
    starte_simulation,
)


class TestNutzerverwaltung(unittest.TestCase):
    def setUp(self) -> None:
        self._verzeichnis = tempfile.TemporaryDirectory()
        self.datei = Path(self._verzeichnis.name) / "nutzer.json"
        self.verwaltung = Nutzerverwaltung(self.datei)

    def tearDown(self) -> None:
        self._verzeichnis.cleanup()

    # -- Nutzer anlegen -------------------------------------------------
    def test_neuer_nutzer_wird_angelegt(self):
        nutzer = self.verwaltung.anlegen("Anna")
        self.assertEqual(nutzer.name, "Anna")
        self.assertTrue(self.verwaltung.existiert("Anna"))

    def test_vergebener_name_erzeugt_fehler(self):
        self.verwaltung.anlegen("Anna")
        with self.assertRaises(NutzernameVergebenError):
            self.verwaltung.anlegen("Anna")
        self.assertEqual(len(self.verwaltung.alle()), 1)

    def test_name_ist_unabhaengig_von_gross_klein_und_leerzeichen_eindeutig(self):
        self.verwaltung.anlegen("Anna")
        with self.assertRaises(NutzernameVergebenError):
            self.verwaltung.anlegen("  aNNa  ")

    def test_leerer_name_wird_abgelehnt(self):
        with self.assertRaises(UngueltigerNutzernameError):
            self.verwaltung.anlegen("   ")

    # -- Persistenz -----------------------------------------------------
    def test_nutzer_landen_in_der_json_datei(self):
        self.verwaltung.anlegen("Anna")
        inhalt = json.loads(self.datei.read_text(encoding="utf-8"))
        self.assertEqual([e["name"] for e in inhalt["nutzer"]], ["Anna"])

    def test_nutzer_bleiben_nach_neustart_erhalten(self):
        self.verwaltung.anlegen("Anna")
        self.verwaltung.anlegen("Bernd")

        neue_verwaltung = Nutzerverwaltung(self.datei)
        self.assertEqual([n.name for n in neue_verwaltung.alle()], ["Anna", "Bernd"])

    def test_fehlende_datei_ergibt_leere_liste(self):
        self.assertTrue(self.verwaltung.ist_leer())
        self.assertFalse(self.datei.exists())

    # -- Nutzer finden --------------------------------------------------
    def test_bestehenden_nutzer_finden(self):
        self.verwaltung.anlegen("Anna")
        self.assertEqual(self.verwaltung.finden("anna").name, "Anna")

    def test_unbekannter_nutzer_erzeugt_fehler(self):
        with self.assertRaises(NutzerNichtGefundenError):
            self.verwaltung.finden("Niemand")

    def test_loeschen_entfernt_nutzer(self):
        self.verwaltung.anlegen("Anna")
        self.verwaltung.loeschen("Anna")
        self.assertTrue(Nutzerverwaltung(self.datei).ist_leer())


class TestSimulationsstart(unittest.TestCase):
    def test_ohne_nutzer_kein_start(self):
        with self.assertRaises(KeinNutzerAngemeldetError):
            starte_simulation(None)

    def test_mit_nutzer_startet_die_simulation(self):
        with tempfile.TemporaryDirectory() as verzeichnis:
            verwaltung = Nutzerverwaltung(Path(verzeichnis) / "nutzer.json")
            nutzer = verwaltung.anlegen("Anna")
            starte_simulation(nutzer)  # darf keine Exception werfen


if __name__ == "__main__":
    unittest.main(verbosity=2)
