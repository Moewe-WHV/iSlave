"""Wartungsintervall des Roboters (#21).

Das Intervall beträgt zwei Jahre und wird ab der letzten Wartung
gerechnet. Eine fällige Wartung sperrt die Nutzung des Roboters.
"""

from datetime import date

WARTUNGSINTERVALL_JAHRE = 2


def berechne_naechste_wartung(letzte_wartung: date) -> date:
    """Termin zwei Jahre nach der letzten Wartung.

    Der 29. Februar wird auf den 28. Februar abgebildet, weil das
    Zieljahr kein Schaltjahr sein muss.
    """
    zieljahr = letzte_wartung.year + WARTUNGSINTERVALL_JAHRE
    if letzte_wartung.month == 2 and letzte_wartung.day == 29:
        return date(zieljahr, 2, 28)
    return letzte_wartung.replace(year=zieljahr)


def wartung_durchfuehren(aktuelles_datum: date) -> date:
    """Setzt die letzte Wartung auf heute und gibt sie zurück."""
    return aktuelles_datum


def ist_wartung_faellig(wartungstermin: date, aktuelles_datum: date) -> bool:
    return aktuelles_datum >= wartungstermin


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
