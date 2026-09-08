import tkinter as tk
from wohnzimmer_raum import Raum             #Alles mit template davor kann geändert werden
from wohnzimmer_roboter import Roboter

# Konfiguration des Rasters 
TILE_SIZE = 64      # Größe der Kacheln in Pixel (zb 64x64 px)

#Raum und Roboterklasse werden implementiert (Die Bezeichnung Zimmer kann später umgeändert werden, dann aber im ganzen Code der Main)

kachel_farben = {}

ladestation_kacheln = [(0,0), (0,1), (1,0), (1,1)]
for koordinate in ladestation_kacheln:
    kachel_farben[koordinate] = "#f01d0e"

sofa_kacheln = [(10,6), (10,5), (10,4), (10,3), (9,6), (9,5), (9,4), (9,3), (8,6), (8,5), (7,6), (7,5), (6,6), (6,5), (5,6), (5,5), (4,6), (4,5), (3,6), (3,5), (2,6), (2,5)]
for koordinate in sofa_kacheln:
    kachel_farben[koordinate] = "#1F2CE4"

fernsehr_kacheln = [(3,0), (4,0), (5,0), (6,0), (7,0), (8,0)]
for koordinate in fernsehr_kacheln:
    kachel_farben[koordinate] = "#DFDBD9"


zimmer = Raum(
    name="Zimmer", 
    hindernisse=[(3,0), (4,0), (5,0), (6,0), (7,0), (8,0)], #wenn kein Hindernis, dann None
    kachel_farben=kachel_farben,
) 

roboter = Roboter()

#Fenster
fenster = tk.Tk()                   #Funktionsaufruf für Fenster
fenster.title("iSlave - Steuerung") #Titel des Fensters

canvas = tk.Canvas(
    fenster,
    width = zimmer.breite * TILE_SIZE,
    height = zimmer.hoehe * TILE_SIZE,
    bg = "white"
)
canvas.pack()

def zeichne_karte():
    """Löscht die Zeichenfläche und zeichnet Raster und Roboter neu."""
    canvas.delete("all") #alles Vorherige wird entfernt, sonst stapeln sich die Zeichnungen

    # Raster zeichnen
    for gx in range(zimmer.breite):
        for gy in range(zimmer.hoehe):
            x0 = gx * TILE_SIZE
            y0 = gy * TILE_SIZE
            x1 = x0 + TILE_SIZE
            y1 = y0 + TILE_SIZE
            ist_hinderniss = (gx, gy) in zimmer.hindernisse

            if (gx, gy) in zimmer.kachel_farben:
                fill = zimmer.kachel_farben[(gx, gy)]           # individuelle Farbe (egal ob Hindernis oder nicht)
            elif ist_hinderniss:
                fill = "#555555"                                 # Fallback: Hindernis ohne eigene Farbe -> Standardgrau
            else:
                fill = "#7c430d"                                     # sonst: Standardboden
            
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#999999")

    #Roboter zeichnen (Platzhalter:grüner Kreis)
    rx0 = roboter.x * TILE_SIZE + 6
    ry0 = roboter.y * TILE_SIZE + 6
    rx1 = rx0 + TILE_SIZE - 12
    ry1 = ry0 + TILE_SIZE - 12
    canvas.create_oval(rx0, ry0, rx1, ry1, fill="#2b7a0b", outline="black", width=2)


# Dient nur jetzt zur Steuerung als Orientierung, wird im fertigen Projekt entfernt
def taste_gedrueckt(event):
    """Wird bei jedem Tastendruck aufgerufen, event.keysym enthält den Tastennamen."""
    richtungen= {
        "Up": (0, -1), "Down": (0, 1),
        "Left": (-1, 0), "Right": (1, 0)
    }
    if event.keysym in richtungen:
        dx, dy = richtungen[event.keysym]
        roboter.bewege(dx, dy, zimmer)
        zeichne_karte()


fenster.bind("<Key>", taste_gedrueckt)
zeichne_karte()
fenster.mainloop()

