class Akku:
    max_zyklen = 500
    min_akkustand = 20

    def laden(self, akkustand, batterie_laden=False):
        if akkustand < self.min_akkustand or batterie_laden:
            laden = 100 - akkustand
            zyklen_zaehler = self.max_zyklen - laden
            akkustand = 100
            return laden, zyklen_zaehler, akkustand
