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


MENUEPUNKTE = {
    "1": "auftrag",
    "2": "aufsatz",
    "3": "laden",
    "4": "wartung",
    "5": "karte",
    "6": "rangliste",
    "0": "beenden",
}


def menu_auswahl(auswahl):
    return MENUEPUNKTE.get(auswahl, "Falsche Eingabe!")


def weitere_aktion_auswaehlen(auswahl):
    if auswahl == "j":
        return True
    elif auswahl == "n":
        return False


def meldungen_ausgeben(meldungen):
    """Gibt die Rückmeldungen des Spiels im Terminal aus."""
    for meldung in meldungen:
        print(meldung)


def aktionen_waehlen(spiel):
    """Fragt eine oder zwei Aktionen für den Auftrag ab (#24)."""
    ausgewaehlte_aktionen = [terminal_aktion_dialog(spiel.aktionen)]

    while True:
        auswahl = input("Weitere Aktion (j/n): ").strip().lower()
        weitere_aktion = weitere_aktion_auswaehlen(auswahl)
        if weitere_aktion is None:
            print("Bitte 'j' oder 'n' eingeben.")
            continue
        break

    if weitere_aktion:
        zweite_aktion = terminal_aktion_dialog(spiel.aktionen)
        if spiel.aktionen.aktionen_bereits_gewaehlt(
            ausgewaehlte_aktionen, zweite_aktion
        ):
            print("Aktion bereits gewählt.")
        else:
            ausgewaehlte_aktionen.append(zweite_aktion)

    return ausgewaehlte_aktionen


def aufsatz_dialog(spiel):
    """Lässt den Nutzer Aufsatz 1 oder 2 wählen (#27)."""
    print("\n1 - Aufsatz 1 (für Fusseln)")
    print("2 - Aufsatz 2 (für Staubansammlungen)")
    auswahl = input("\nAufsatz wählen: ").strip()

    if auswahl.isdigit():
        return spiel.aufsatz_waehlen(int(auswahl))
    return spiel.aufsatz_waehlen(auswahl)


def terminal_menu(spiel):
    """Strukturiertes Menü zur Steuerung des Roboters (#24)."""
    while True:
        print("\n===== iSlave =====")
        print(spiel.statuszeile())
        print(spiel.ausruestungszeile())
        print("\n1 - Auftrag starten")
        print("2 - Aufsatz wählen")
        print("3 - Akku laden")
        print("4 - Wartung durchführen")
        print("5 - Karte anzeigen")
        print("6 - Rangliste anzeigen")
        print("0 - Beenden")

        ergebnis = menu_auswahl(input("\nAuswahl: ").strip())

        if ergebnis == "Falsche Eingabe!":
            print(ergebnis)
            continue

        if ergebnis == "beenden":
            meldungen_ausgeben(spiel.beenden())
            spiel.highscore.rangliste_anzeigen()
            return spiel

        if ergebnis == "auftrag":
            terminal_raum_dialog(spiel.raumsteuerung)
            meldungen_ausgeben(spiel.raum_wechseln(spiel.aktueller_raum))
            meldungen_ausgeben(spiel.auftrag_ausfuehren(aktionen_waehlen(spiel)))

        elif ergebnis == "aufsatz":
            meldungen_ausgeben(aufsatz_dialog(spiel))

        elif ergebnis == "laden":
            meldungen_ausgeben(spiel.akku_laden())

        elif ergebnis == "wartung":
            meldungen_ausgeben(spiel.wartung_ausfuehren())

        elif ergebnis == "karte":
            print()
            print(spiel.karte_als_text())

        elif ergebnis == "rangliste":
            spiel.highscore.rangliste_anzeigen()

        elif ergebnis == "beenden":
            return
