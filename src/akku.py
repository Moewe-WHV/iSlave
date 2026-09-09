class Akku:
    max_zyklen = 500
    min_akkustand = 20
    warngrenze_zyklen = 495

    def __init__(
        self,
        akkustand: int = 90,
        zyklen_zaehler: int = 2,
        verbrauchte_kapazitaet: int = 0,
    ):  # Konstruktor = Akkustand sofort gültig
        self.akkustand = akkustand
        self.zyklen_zaehler = zyklen_zaehler
        # Summe des Verbrauchs seit dem letzten vollen Ladezyklus (AKKU2)
        self.verbrauchte_kapazitaet = verbrauchte_kapazitaet

    def akkustand_anzeigen(self) -> int:  # zeigt Akkustand in Prozent
        print(f"Akkustand: {self.akkustand}%")
        return self.akkustand

    def kann_aufgabe_ausfuehren(self) -> bool:  # prüft ob Aufgabe möglich ist
        return self.akkustand >= self.min_akkustand

    def verbrauchen(self, wert: int) -> int:  # zieht Akku ab und aktualisiert Stand
        self.akkustand -= wert
        if self.akkustand < 0:
            self.akkustand = 0
        self.kapazitaet_verbuchen(wert)
        self.akkustand_anzeigen()
        if self.akkustand < self.min_akkustand:
            print("Warnung: Akku unter 20%! Roboter muss geladen werden.")
        return self.akkustand

    def kapazitaet_verbuchen(self, wert: int) -> int:
        """Zählt den Verbrauch zusammen.

        Ein Ladezyklus entspricht 100 % insgesamt verbrauchter Kapazität.
        Sind 100 % erreicht, wird der Zyklenzähler um 1 erhöht und der
        Rest für den nächsten Zyklus übernommen.
        """
        self.verbrauchte_kapazitaet += wert
        while self.verbrauchte_kapazitaet >= 100:
            self.verbrauchte_kapazitaet -= 100
            self.zyklen_zaehler += 1
            self.verschleiss_pruefen()
        return self.zyklen_zaehler

    def verschleiss_pruefen(self) -> bool:
        """Warnt den Spieler, wenn der Verschleiß droht."""
        if self.zyklen_zaehler >= self.warngrenze_zyklen:
            print("Achtung: Die Batterie ist fast am Ende ihrer Lebensdauer!")
            return True
        return False

    def aufgabe(self):  # Aufgabe mit festem Verbrauch
        if self.kann_aufgabe_ausfuehren():
            print("Roboter erfüllt Aufgabe...")
            self.verbrauchen(15)  # Standardverbrauch einer Aufgabe
        else:
            print("Akku zu niedrig, Aufgabe kann nicht ausgeführt werden.")

    def laden(self, batterie_laden=False):
        """Lädt den Akku auf 100 %.

        Geladen wird nur unter 20 % oder wenn das Laden ausdrücklich
        verlangt wird. Sonst gibt die Methode None zurück und der Stand
        bleibt unverändert.
        """
        if self.akkustand >= self.min_akkustand and not batterie_laden:
            return None

        geladener_prozentsatz = 100 - self.akkustand
        self.akkustand = 100
        self.verschleiss_pruefen()
        return geladener_prozentsatz, self.zyklen_zaehler, self.akkustand

    def zyklen_anzeigen(self, zyklen=None):
        if zyklen is None:
            zyklen = self.zyklen_zaehler
        print(f"{zyklen}/{self.max_zyklen}")
        return zyklen
