# Haupteinstiegspunkt der Terminalanwendung
from akku import Akku

if __name__ == "__main__":

    mein_akku = Akku()  # Akku objekt erstellt
    mein_akku.akkustand_anzeigen()  # Akkustand anzeigen
    mein_akku.zyklen_anzeigen(mein_akku.zyklen_zaehler)  # Zyklen anzeigen

    weitere_aufgabe = "ja"

    while weitere_aufgabe == "ja":  # Abfrage ob noch eine Aufgabe erledigt werden soll
        mein_akku.aufgabe()
        weitere_aufgabe = input(
            "Soll noch eine weitere Aufgabe ausgeführt werden? (ja / nein)"
        )
