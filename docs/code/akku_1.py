class Akku:
    def __init__(self, akkustand: int): #Konstruktor = Akkustand sofort gültig
        self.akkustand = akkustand

    def akkustand_anzeigen(self, akkustand: int) -> int: #Methode
        print(f"Akkustand: {akkustand}%")
        return akkustand
    
mein_akku = Akku(100) #Objekt

print("Akkustand", mein_akku.akkustand) #Ausgabe