from src.raeume import Raumsteuerung
#from src.aktionen import RoboterAktionen


def verfuegbare_raeume_anzeigen(raumsteuerung):
   return raumsteuerung.gueltige_raeume

def raum_auswaehlen(raumsteuerung, auswahl):
    return raumsteuerung.raum_wechseln(auswahl)

def terminal_raeume_anzeigen(raumsteuerung):
    return "\n".join(raumsteuerung.gueltige_raeume)

def raum_dialog(raumsteuerung, auswahl):
    return raum_auswaehlen(raumsteuerung, auswahl)

def terminal_raum_dialog(raumsteuerung):
    while True:
        print("\nVerfügbare Räume: ")
        print (terminal_raeume_anzeigen(raumsteuerung))

        auswahl = input("\nRaum wählen: ")

        ergebnis = raum_dialog(raumsteuerung, auswahl) 

        if ergebnis != "Raum nicht vorhanden!":
            return ergebnis

        print("Raum nicht vorhanden!")
        input("Enter drücken, um erneut einen Raum auszuwählen...")

def aktion_auswaehlen(aktionen, auswahl):
    return aktionen.aktion_ausfuehren(auswahl)

def terminal_interaktion(raumsteuerung, aktionen):
    zielraum = terminal_raum_dialog(raumsteuerung)

    print(f"\nZielraum: {zielraum}")

    return terminal_aktion_dialog(aktionen)

def terminal_aktion_dialog(aktionen):
    while True: 
        print("\nVerfügbare Aktionen:")
        print("\n".join(aktionen.gueltige_aktionen))

        auswahl = input("\nAktion wählen: ")

        ergebnis = aktion_auswaehlen(aktionen, auswahl)

        if ergebnis != "Aktion nicht möglich!":
            print(f"\nAktion ausgeführt: {ergebnis}")
            return ergebnis
        print("Aktion nicht möglich!")
        input("Enter drücken, um erneut eine Aktion auszuwählen...")

