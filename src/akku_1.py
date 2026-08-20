class Akku:
    def __init__(self, akkustand: int): #Kostruktor Akkustand sofort gültig
        self.akkustand = akkustand

    def akkustand_anzeigen(self) -> int: #Methode
        print(f"Akkustand: {self.akkustand}%")
        return self.akkustand

mein_akku = Akku(100) #Objekt
mein_akku.akkustand_anzeigen() #Ausgabe