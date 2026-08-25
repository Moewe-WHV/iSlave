class Raumsteuerung:

    gueltige_raeume = ["Wohnzimmer", "Bad", "Küche", "Schlafzimmer"]

    def __init__(self):
        self.aktueller_raum = None

    def raum_wechseln(self, zielraum):
        if zielraum in self.gueltige_raeume:
            self.aktueller_raum = zielraum
            return zielraum
        else:
            return "Raum nicht vorhanden!"
