# Haupteinstiegspunkt der Terminalanwendung
import akku1 
import wartung 

if __name__ == "__main__": 
    
    mein_akku = Akku(100)           #Akku objekt erstellt
    mein_akku.akkustand_anzeigen()  #Akkustand anzeigen
    weitere_aufgabe = "ja"

    while weitere_aufgabe == "ja":  #Abfrage ob noch eine Aufgabe erledigt werden soll
        mein_akku.aufgabe()
        weitere_aufgabe = input("Soll noch eine weitere Aufgabe ausgeführt werden? (ja / nein)")
