import pygame #import von pygame
import os #import von os-Modul für Betriebssystem-Funktionen u.a. Dateipfade
import random #import von random, das zufallsfunktionen bereitstellt

pygame.init()

TILE_GROESSE = 64 #Die Anzahl der Pixel pro Feld

# Die Größe der Karte ---------------------------------------------------------------------------

#Aussehen der Karte durch das Tileset
karte = [                                   # Y
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0],   # 0
    [ 0,  0,  0,  0, 14, 14, 14, 14,  0],   # 1
    [ 0,  0,  0,  0,  1,  4,  6, 13,  0],   # 2
    [ 0,  0,  0,  0,  2,  5,  7,  8,  0],   # 3
    [ 0, 13, 13, 13,  3, 12, 12,  9,  0],   # 4
    [ 0, 13, 13, 13, 11, 11, 11, 10,  0],   # 5
    [ 0, 11, 11, 11, 11, 11, 11, 11,  0],   # 6
    [ 0, 11, 11, 11, 11, 11, 11, 11,  0],   # 7
    [ 0, 11, 11, 11, 11, 11, 11, 11,  0],   # 8
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0],   # 9
# X   0   1   2   3   4   5   6   7   8
]

#Begehbare und nicht begehbare Felder zuordnen 
kollision = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1], # 0
    [1, 1, 1, 1, 1, 1, 1, 1, 1], # 1
    [1, 1, 1, 1, 1, 1, 1, 1, 1], # 2
    [1, 1, 1, 1, 1, 1, 1, 1, 1], # 3
    [1, 1, 1, 1, 1, 0, 0, 1, 1], # 4
    [1, 1, 1, 1, 0, 0, 0, 0, 1], # 5
    [1, 0, 0, 0, 0, 0, 0, 0, 1], # 6
    [1, 0, 0, 0, 0, 0, 0, 0, 1], # 7
    [1, 0, 0, 0, 0, 0, 0, 0, 1], # 8
    [1, 1, 1, 1, 1, 1, 1, 1, 1], # 9
]

#Überprüfung, ob Karte und Kollision gleich groß sind, wenn nicht, dann wird es in der Konsole ausgegeben
assert len(karte) == len(kollision), "karte und kollision müssen gleich viele Zeilen haben!"
assert len(karte[0]) == len(kollision[0]), "karte und kollision müssen gleich viele Spalten haben!"

# Farben der Karte wie Wand und Boden (ohne Tileset)----------------------------------------------------------

###Farben = {
#Farben= R   G   B          0 - 255
###    0: (34, 139, 34),       # Boden = Grün
###    1: (105, 105, 105),     # Wand = Grau
###}

#Startposition des Spielers (in Kachel-Koordinaten, nicht in Pixel!)---------------------------------

spieler_x = 2 #Spalte 2
spieler_y = 7 #Zeile 7
spieler_richtung = "unten" #Zeigt die Blickrichtung beim Start ( wird weiter unten definiert! Zeile: )

#Startposition der NPCs wie bei Spieler-------------------------------------------------------------

npc_x = 5
npc_y = 5

# Die Festlegung der Fensterhöhe und Breite (kann von karte oder von kollision abgeleitet werden) -----------------------------------------------------

breite = len(karte[0]) * TILE_GROESSE
hoehe = len(karte) * TILE_GROESSE
# Die Größe kann auch beliebig eingestellt werden


# Größe und Überschrift des Fensters ------------------------------------------------------------

bildschirm = pygame.display.set_mode((breite, hoehe))
pygame.display.set_caption("Karte testen")
uhr = pygame.time.Clock()

# Einfügen von Tileset (in Koordinaten aufgeteilt)----------------------------------------------------------------
SKRIPT_ORDNER = os.path.dirname(__file__) # Ordner, in dem diese .py-Datei selbst liegt
tileset_pfad = os.path.join(SKRIPT_ORDNER, "..", "Assets", "Tilesets", "Bad(64x64).png") # Pfad zum Tileset, ausgehend vom Skript-Ordner / ".." bedeutet eine Ordnerebene nach oben
tileset = pygame.image.load(tileset_pfad).convert() # convert() wandelt das geladene Bild in genau das gleiche Format wie das Fenster um

def hole_tile(tileset, spalte,zeile, groesse):
    rechteck = pygame.Rect(spalte * groesse, zeile * groesse, groesse, groesse)
    return tileset.subsurface(rechteck)

# Koordinaten vom Tileset wird auf die Karte über Zahlen festgelegt------------------------------------------------
tile_bilder = {
    #Schwarzer Rand
    0:  hole_tile(tileset, 4, 1, TILE_GROESSE),
    #Dusche
    1:  hole_tile(tileset, 0, 1, TILE_GROESSE),
    2:  hole_tile(tileset, 0, 2, TILE_GROESSE),
    3:  hole_tile(tileset, 0, 3, TILE_GROESSE),
    #Fenster
    4:  hole_tile(tileset, 1, 1, TILE_GROESSE),
    5:  hole_tile(tileset, 1, 2, TILE_GROESSE),
    6:  hole_tile(tileset, 2, 1, TILE_GROESSE),
    7:  hole_tile(tileset, 2, 2, TILE_GROESSE),
    #Badewanne
    8:  hole_tile(tileset, 4, 2, TILE_GROESSE),
    9:  hole_tile(tileset, 4, 3, TILE_GROESSE),
    10: hole_tile(tileset, 4, 4, TILE_GROESSE),
    #Bodenfliesen und Wand und Decke
    11: hole_tile(tileset, 1, 3, TILE_GROESSE), #helle Fliesen
    12: hole_tile(tileset, 2, 3, TILE_GROESSE), #dunkle Fliesen
    13: hole_tile(tileset, 3, 1, TILE_GROESSE), #Wand
    14: hole_tile(tileset, 0, 0, TILE_GROESSE), #Decke
}

# Einfügen von Charakter-Tileset auf Charakter----------------------------------------------------------------------

spieler_spritesheet_pfad = os.path.join(SKRIPT_ORDNER,"..", "Assets", "Charakter", "Charakter_Grundform.png") # ".." nach dem SKRIPT_ORDNER nicht vergessen
spieler_spritesheet = pygame.image.load(spieler_spritesheet_pfad).convert_alpha() #convert_alpha macht den weißen Hintergrund transparent

def hole_bild(spritesheet, spalte, zeile , breite , hoehe): # Im Kern das Gleiche wie bei hole_tile nur dass Breite und Höhe jetzt unabhängig sind, statt beide von groesse abzuhängen.
    rechteck = pygame.Rect(spalte * breite, zeile * hoehe, breite, hoehe)
    return spritesheet.subsurface(rechteck)

# Koordinaten vom Tileset des Charakters wird auf die Bewegung über Zahlen festgelegt---------------------------------------------------------------

# Da der Charakter nicht nur aus 64x64px bsteht , muss Höhe und Breite beim Charakter neu angepasst werden
CHAR_BREITE = 64
CHAR_HOEHE = 128 

# Beim Spieler ist jetzt eine Kachel 64x128 groß und nicht mehr 64x64, daher verändert sich auch der Index des Charaktersets, also aller 2 Zeilen ist jetzt eine Kachel 
spieler_bilder = {
    "unten":    hole_bild(spieler_spritesheet, 1, 0, CHAR_BREITE, CHAR_HOEHE),
    "oben":     hole_bild(spieler_spritesheet, 1, 1, CHAR_BREITE, CHAR_HOEHE),
    "links":    hole_bild(spieler_spritesheet, 1, 2, CHAR_BREITE, CHAR_HOEHE),
    "rechts":   hole_bild(spieler_spritesheet, 1, 3, CHAR_BREITE, CHAR_HOEHE),
}

# Funktion für das Zeichnen der Karte nach fill() und vor flip() im Game Loop---------------------------------------------------

def zeichne_karte(bildschirm, karte):
    for y, zeile in enumerate(karte):           #emurate() zeigt den Index beim Durchlauf der Schleife mit an
        for x, tile in enumerate(zeile):
            # Folgendes in den Kommentaren nur anwendbar, wenn ohne Tileset gearbeitet wird
            ###farbe = Farben[tile]
            ###rechteck = pygame.Rect(x * TILE_GROESSE, y * TILE_GROESSE, TILE_GROESSE, TILE_GROESSE) #pygame.Rect(x_pixel, y_pixel, breite, hoehe) erstellt ein Rechteck
            ###pygame.draw.rect(bildschirm, farbe, rechteck) # zeichnet auf bildschirm in der farbe das rechteck
            bild = tile_bilder[tile]
            bildschirm.blit(bild, (x * TILE_GROESSE, y * TILE_GROESSE))

# Funktion für das Zeichnen des Charakters-------------------------------------------------------------------------------

def zeichne_spieler(bildschirm, spieler_x, spieler_y, spieler_richtung):
    bild = spieler_bilder[spieler_richtung]
    pixel_x = spieler_x * TILE_GROESSE
    pixel_y = spieler_y * TILE_GROESSE - (CHAR_HOEHE - TILE_GROESSE)
    bildschirm.blit(bild, (pixel_x, pixel_y))

# Funktion für die NPCs-------------------------------------------------------------------------------------------------

def zeichne_npc(bildschirm, npc_x, npc_y):
    rechteck = pygame.Rect(npc_x * TILE_GROESSE, npc_y * TILE_GROESSE, TILE_GROESSE, TILE_GROESSE)
    pygame.draw.rect(bildschirm, (0, 255, 0), rechteck) # Grün, als Platzhalter

#Zuweisung des NPCs und Dauereinstellung eines Events zB. zufällige Bewegung--------------------------------------------

NPC_BEWEGUNG_EVENT= pygame.USEREVENT + 1
pygame.time.set_timer(NPC_BEWEGUNG_EVENT, 4000) # alle 4000ms = 4 Sekunden

# Game Loop, damit sich das Fenster nicht schließt ----------------------------------------------------------------------------------

laeuft = True
while laeuft:
    for event in pygame.event.get(): # Prüft ob Tasten gedrückt oder Fenster geschlossen werden
        if event.type == pygame.QUIT: 
            laeuft = False

        #Hier kommt die OPTIONALE Möglichkeit, einen NPC einem zufälligen Bewegungsrythmus zuzuweisen
        if event.type == NPC_BEWEGUNG_EVENT:
            richtung = random.choice(["hoch", "runter", "links", "rechts"])

            neues_x = npc_x
            neues_y = npc_y

            if richtung == "hoch":
                neues_y = npc_y - 1
            elif richtung == "runter":
                neues_y = npc_y + 1
            elif richtung == "links":
                neues_x = npc_x -1
            elif richtung == "rechts":
                neues_x = npc_x + 1

            if kollision[neues_y][neues_x] != 1:
                npc_x = neues_x
                npc_y = neues_y

        # Ab hier beginnt die Steuerung des Charakters und die Blickrichtung wird zugewiesen
        if event.type == pygame.KEYDOWN:
            neues_x = spieler_x
            neues_y = spieler_y

            if event.key == pygame.K_UP:
                neues_y = spieler_y - 1
                spieler_richtung = "oben"
            elif event.key == pygame.K_DOWN:
                neues_y = spieler_y + 1
                spieler_richtung = "unten"
            elif event.key == pygame.K_LEFT:
                neues_x = spieler_x - 1
                spieler_richtung = "links"
            elif event.key == pygame.K_RIGHT:
                neues_x = spieler_x + 1
                spieler_richtung = "rechts"

            if kollision[neues_y][neues_x] != 1:
                spieler_x = neues_x
                spieler_y = neues_y

    bildschirm.fill((0, 0, 0)) #Hier wird die Farbe des Inhalts des Fensters festgelegt
    zeichne_karte(bildschirm, karte)
    zeichne_spieler(bildschirm, spieler_x, spieler_y, spieler_richtung)
    zeichne_npc(bildschirm, npc_x, npc_y)
    pygame.display.flip() #Zeigt das aktuelle Bild an

    uhr.tick(60) # 60 FPS 

pygame.quit()