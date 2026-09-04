class RoboterAktionen:

    gueltige_aktionen = ["Spülen", "Saugen", "Wischen"]

    def __init__(self):
        self.aktuelle_aktion = None

    def aktion_ausfuehren(self, aktion):
        if aktion in self.gueltige_aktionen:
            self.aktuelle_aktion = aktion
            return aktion
        else:
            return "Aktion nicht möglich!"

    def aktionen_bereits_gewaehlt(self, ausgewaehlte_aktionen, aktion):
        return aktion in ausgewaehlte_aktionen

    def reihenfolge_festlegen(self, ausgewaehlte_aktionen):
        if "Saugen" in ausgewaehlte_aktionen and "Wischen" in ausgewaehlte_aktionen:
            return ["Saugen", "Wischen"]
        return ausgewaehlte_aktionen
