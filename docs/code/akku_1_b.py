class Akku:
    def __init__(self, akkustand: int): #Konstruktor = Akkustand sofort gültig
        self.akkustand = akkustand

    def akkustand_anzeigen(self) -> int: #zeigt Akkustand in Prozent
        print(f"Akkustand: {self.akkustand}%")
        return self.akkustand

    def kann_aufgabe_ausfuehren(self) -> bool: #prüft ob Aufgabe möglich ist
        return self.akkustand >= 20

    def verbrauchen(self, wert: int): #zieht Akku ab und aktualisiert Stand
        self.akkustand -= wert
        if self.akkustand < 0:
            self.akkustand = 0
        self.akkustand_anzeigen()
        if self.akkustand < 20:
            print("Warnung: Akku unter 20%! Roboter muss geladen werden.")

    def aufgabe(self): #Aufgabe mit festem Verbrauch
        if self.kann_aufgabe_ausfuehren():
            print("Roboter erfüllt Aufgabe...")
            self.verbrauchen(15) #beliebiger Verbrauch, 15 ist ein Platzhalter  
        else:
            print("Akku zu niedrig, Aufgabe kann nicht ausgeführt werden.")




mein_akku = Akku(100)
mein_akku.aufgabe()
