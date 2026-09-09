import json
import os


class Highscore:

    def __init__(self, dateiname: str = "highscores.json"):
        self.punkte: int = 0  # Sauberkeitspunkte (SP) starten bei 0
        self.dateiname: str = dateiname

    def punkte_hinzufuegen(self, wert: int, aktion: str = ""):
        """Erhöht die Sauberkeitspunkte (SP) um den angegebenen Wert."""
        self.punkte += wert
        if aktion:
            print(f"+{wert} SP für {aktion}! Aktuelle SP: {self.punkte}")
        else:
            print(f"+{wert} SP! Aktuelle SP: {self.punkte}")

    def fleck_reinigen(self):  # Gereinigte Flecken bringen 2 SP
        print("Fleck erfolgreich gereinigt!")
        self.punkte_hinzufuegen(2, "Fleck reinigen")

    def wolllaus_besiegen(self):  # Besiegte Wollläuse bringen 1 SP
        print("Wolllaus besiegt!")
        self.punkte_hinzufuegen(1, "Wolllaus besiegen")

    def staubmonster_besiegen(self):  # Besiegte Staubmonster bringen 2 SP
        print("Staubmonster besiegt!")
        self.punkte_hinzufuegen(2, "Staubmonster besiegen")

    def beute_einsammeln(self):  # Eingesammelte Beute bringt 1 SP
        print("Beute eingesammelt!")
        self.punkte_hinzufuegen(1, "Beute einsammeln")

    def alle_highscores_laden(self) -> list:
        """Lädt alle bisherigen Spielstände aus der JSON-Datei."""
        if not os.path.exists(self.dateiname):
            return []
        try:
            with open(self.dateiname, "r", encoding="utf-8") as datei:
                daten = json.load(datei)
                return daten if isinstance(daten, list) else []
        except (json.JSONDecodeError, IOError):
            return []

    def punkte_von(self, nutzername: str) -> int:
        """Gespeicherte SP eines Nutzers, 0 wenn er noch nicht gespielt hat."""
        for eintrag in self.alle_highscores_laden():
            if eintrag.get("name") == nutzername:
                return eintrag.get("punkte", 0)
        return 0

    def punkte_setzen(self, punkte: int) -> int:
        """Übernimmt einen gespeicherten Punktestand beim Einloggen."""
        self.punkte = punkte
        return self.punkte

    def speichern(self, nutzername: str) -> list:
        """Speichert die SP des Nutzers, ohne nach dem Namen zu fragen.

        Jeder Nutzer hat genau einen Eintrag (#31). Spielt er erneut,
        wird sein bisheriger Eintrag aktualisiert.
        """
        scores = self.alle_highscores_laden()

        for eintrag in scores:
            if eintrag.get("name") == nutzername:
                eintrag["punkte"] = self.punkte
                break
        else:
            scores.append({"name": nutzername, "punkte": self.punkte})

        with open(self.dateiname, "w", encoding="utf-8") as datei:
            json.dump(scores, datei, ensure_ascii=False, indent=4)

        return scores

    def spiel_beenden_und_speichern(self, nutzername: str = None):
        """Speichert den Punktestand und zeigt die Rangliste.

        Ohne übergebenen Namen wird er im Terminal abgefragt.
        """
        print("\n--- Spiel beendet ---")

        if nutzername is None:
            nutzername = input("Bitte deinen Nutzernamen eingeben: ").strip()

        if not nutzername:
            nutzername = "Mr. Nobody"  # Standardname, falls kein Name eingegeben wurde

        scores = self.speichern(nutzername)

        print(f"Punkte für {nutzername} ({self.punkte} SP) gespeichert!")
        self.rangliste_anzeigen(scores)

    def rangliste_anzeigen(self, scores: list = None):
        """Zeigt eine sortierte Rangliste aller Einträge an."""
        if scores is None:
            scores = self.alle_highscores_laden()

        print("\n" + "=" * 20 + " RANGLISTE " + "=" * 20)
        if not scores:
            print("Noch keine Einträge vorhanden.")
        else:
            # Sortierung nach Punkten absteigend
            sortiert = sorted(
                scores, key=lambda eintrag: eintrag["punkte"], reverse=True
            )
            for platz, eintrag in enumerate(sortiert, start=1):
                name = eintrag.get("name", "Unbekannt")
                punkte = eintrag.get("punkte", 0)
                print(f"{platz:>2}. {name:<20} : {punkte:>3} SP")
        print("=" * 51 + "\n")
