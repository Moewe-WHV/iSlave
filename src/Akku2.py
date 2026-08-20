class Akku:
    max_zyklen = 500
    min_akkustand = 20
    
    def laden(self, akkustand, batterie_laden=False):
        if akkustand < self.min_akkustand or batterie_laden:
            laden = 100 - akkustand
            zyklen_zaehler = self.max_zyklen - laden
            akkustand = 100
            if zyklen_zaehler >= 495:
                print("Achtung: Die Batterie ist fast am Ende ihrer Lebensdauer!")
            return laden, zyklen_zaehler, akkustand
    def zyklen_anzeigen(self, zyklen_zaehler):
        print(f"Zyklen: {zyklen_zaehler}/{self.max_zyklen}")
 