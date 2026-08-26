from raumsteuerung import Raumsteuerung
from aktionen import RoboterAktionen

raumsteuerung = Raumsteuerung()
aktionen = RoboterAktionen()

print("Verfügbare Räume:", ", ".join(Raumsteuerung.gueltige_raeume))

zielraum = input("In welchen Raum soll der Roboter fahren? ")

if zielraum not in Raumsteuerung.gueltige_raeume:
    print("Raum nicht vorhanden!")
    exit()

aktion = input("Welche Aktion soll ausgeführt werden? ")

if aktion not in RoboterAktionen.gueltige_aktionen:
    print("Aktion nicht möglich")
    exit()

raumsteuerung.raum_wechseln(zielraum)
ergebnis = aktionen.aktion_ausfuehren(aktion)
print("Aktion erfolgreich ausgeführt!")