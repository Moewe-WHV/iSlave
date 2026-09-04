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
        print(terminal_raeume_anzeigen(raumsteuerung))

        auswahl = input("\nRaum wählen: ").strip()

        ergebnis = raum_dialog(raumsteuerung, auswahl)

        if ergebnis != "Raum nicht vorhanden!":
            return ergebnis

        print("Raum nicht vorhanden!")
        input("Enter drücken, um erneut einen Raum auszuwählen...")


def aktion_auswaehlen(aktionen, auswahl):
    if auswahl in aktionen.gueltige_aktionen:
        return auswahl
    return "Aktion nicht möglich!"

def terminal_interaktion(raumsteuerung, aktionen):
    zielraum = terminal_raum_dialog(raumsteuerung)

    print(f"\nZielraum: {zielraum}")

    return terminal_aktion_dialog(aktionen)


def terminal_aktion_dialog(aktionen):
    while True:
        print("\nVerfügbare Aktionen:")
        print("\n".join(aktionen.gueltige_aktionen))

        auswahl = input("\nAktion wählen: ").strip()

        ergebnis = aktion_auswaehlen(aktionen, auswahl)

        if ergebnis != "Aktion nicht möglich!":
            # print(f"\nAktion ausgeführt: {ergebnis}")
            return ergebnis
        print("Aktion nicht möglich!")
        input("Enter drücken, um erneut eine Aktion auszuwählen...")


def menu_auswahl(auswahl):
    if auswahl == "1":
        return "auftrag"
    elif auswahl == "0":
        return "beenden"
    else:
        return "Falsche Eingabe!"


def weitere_aktion_auswaehlen(auswahl):
    if auswahl == "j":
        return True
    elif auswahl == "n":
        return False


def terminal_menu(raumsteuerung, aktionen, akku):
    while True:
        print("\n===== iSlave =====")
        print("1 - Auftrag starten")
        print("0 - Beenden")
        auswahl = input("\nAuswahl: ")
        ergebnis = menu_auswahl(auswahl)

        if ergebnis == "Falsche Eingabe!":
            print(ergebnis)
            continue

        if ergebnis == "auftrag":
            ausgewaehlte_aktionen = []
            
            terminal_raum_dialog(raumsteuerung)

            erste_aktion = terminal_aktion_dialog(aktionen)
            ausgewaehlte_aktionen.append(erste_aktion)
            # print(ausgewaehlte_aktionen)

            auswahl_weitere_aktion = input("Weitere Aktion (j/n): ")
            weitere_aktion = weitere_aktion_auswaehlen(auswahl_weitere_aktion)

            if weitere_aktion is True:
                zweite_aktion = terminal_aktion_dialog(aktionen)

                if aktionen.aktionen_bereits_gewaehlt(ausgewaehlte_aktionen, zweite_aktion):
                    print("Aktion bereits gewählt.")
                else: 
                    ausgewaehlte_aktionen.append(zweite_aktion)
                    
            sortierte_aktionen = aktionen.reihenfolge_festlegen(ausgewaehlte_aktionen)

            for aktion in sortierte_aktionen:
                ergebnis = aktionen.aktion_ausfuehren(aktion)
                print(f"\nAktion ausgeführt: {ergebnis}")

                akku.verbrauchen(10) 

           
        elif ergebnis == "aktion":
            if raumsteuerung.aktueller_raum is None:
                print("Bitte zuerst eine Raum auwählen.")
            else:
                terminal_aktion_dialog(aktionen)
   
        elif ergebnis == "beenden":
            return

