class Akku:
    def __init__(self, akkustand: int):
        self.akkustand = akkustand

    def akkustand_anzeigen(self) -> int:
        print(f"Akkustand: {self.akkustand}%")
        return self.akkustand

mein_akku = Akku(100)
mein_akku.akkustand_anzeigen()