from akku1 import Akku 


#raum = input("Wohin?")  # raum 
aktion = input("was?")  # Aktion


class Roboter():

    def spuellmittel_aktion1(self, akku_objekt):
        print("Spuellmittel Aktion 1 wird ausgeführt")
        akku_objekt.aufgabe()
    
        
    def spuellmittel_aktion2():
        pass

    def staubsauger_aktion1():
        pass

    def staubsauger_aktion2():
        pass




class Spuellmittel:

    def __init__(self, anzahl):
        self.anzahl = anzahl


class Staubsauger:

    def __init__(self, aufsaetze):
        self.aufsaetze = aufsaetze
    
roboter = Roboter()    
akku_test = Akku(100)

methode = getattr(roboter, aktion, None)
methode(akku_test)

#roboter.spuellmittel_aktion1(akku_test)
