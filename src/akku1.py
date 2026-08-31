class Akku:
    def __init__(
        self, akkustand: int = 90, zyklen_zaehler: int = 2
    ):  # Konstruktor = Akkustand sofort gültig
        self.akkustand = akkustand
        self.zyklen_zaehler = zyklen_zaehler

    def akkustand_anzeigen(self) -> int:  # zeigt Akkustand in Prozent
        print(f"Akkustand: {self.akkustand}%")
        return self.akkustand

    def kann_aufgabe_ausfuehren(self) -> bool:  # prüft ob Aufgabe möglich ist
        return self.akkustand >= 20

    def verbrauchen(self, wert: int):  # zieht Akku ab und aktualisiert Stand
        self.akkustand -= wert
        if self.akkustand < 0:
            self.akkustand = 0
        self.akkustand_anzeigen()
        if self.akkustand < 20:
            print("Warnung: Akku unter 20%! Roboter muss geladen werden.")

    def aufgabe(self):  # Aufgabe mit festem Verbrauch
        if self.kann_aufgabe_ausfuehren():
            print("Roboter erfüllt Aufgabe...")
            self.verbrauchen(15)  # beliebiger Verbrauch, 15 ist ein Platzhalter
        else:
            print("Akku zu niedrig, Aufgabe kann nicht ausgeführt werden.")

    max_zyklen = 500
    min_akkustand = 20

    def laden(self, akkustand, batterie_laden=False):
        if self.akkustand < self.min_akkustand or batterie_laden:
            geladener_prozentsatz = 100 - self.akkustand
            self.zyklen_zaehler = self.max_zyklen - geladener_prozentsatz
            self.akkustand = 100
            if self.zyklen_zaehler >= 495:
                print("Achtung: Die Batterie ist fast am Ende ihrer Lebensdauer!")
            return geladener_prozentsatz, self.zyklen_zaehler, self.akkustand

    def zyklen_anzeigen(self, zyklen):
        print(f"{zyklen}/500")


# Akku(0,100)
