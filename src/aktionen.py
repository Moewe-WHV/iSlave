class RoboterAktionen:

    gueltige_aktionen = ["Spülmittel", "Staubsaugeraufsätze"]

    def __init__(self):
        self.aktuelle_aktion = None
 
    def aktion_ausfuehren(self, aktion):
        if aktion in self.gueltige_aktionen:
            self.aktuelle_aktion = aktion
            return aktion
        else: 
            return "Aktion nicht möglich"

 
