from datetime import date


def berechne_naechste_wartung(letzte_wartung: date) -> date:
    return letzte_wartung.replace(year=letzte_wartung.year + 2)


def ist_wartung_faellig(wartungstermin: date, aktuelles_datum: date) -> bool:
    return aktuelles_datum >= wartungstermin


def berechne_verbleibende_tage(wartungstermin, aktuelles_datum) -> int:
    return (wartungstermin - aktuelles_datum).days


def berechne_verbleibende_tage(wartungstermin: date, aktuelles_datum: date) -> int:
    return max((wartungstermin - aktuelles_datum).days, 0)


def erstelle_wartungsmeldung(wartungstermin: date, aktuelles_datum: date) -> str:
    if ist_wartung_faellig(wartungstermin, aktuelles_datum):
        return "Wartung fällig. " "Der Roboter kann nicht mehr genutzt werden."

    verbleibende_tage = berechne_verbleibende_tage(wartungstermin, aktuelles_datum)

    formatiertes_datum = wartungstermin.strftime("%d.%m.%Y")
    return (
        f"Nächste Wartung: {formatiertes_datum}. "
        f"Verbleibende Tage: {verbleibende_tage}."
    )
