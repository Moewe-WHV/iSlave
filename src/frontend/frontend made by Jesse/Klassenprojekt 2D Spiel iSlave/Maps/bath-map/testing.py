import pygame #import von pygame
import os #import von os-Modul für Betriebssystem-Funktionen u.a. Dateipfade
import random #import von random, das zufallsfunktionen bereitstellt

pygame.init()

TILE_GROESSE = 64 #Die Anzahl der Pixel pro Feld

# Die Größe der Karte ---------------------------------------------------------------------------

#Aussehen der Karte durch das Tileset
karte = [                                   # Y
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 0
    [ 0,  0,  0,  0, 14, 14, 14, 14,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 1
    [ 0,  0,  0,  0,  1,  4,  6, 13,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 2
    [ 0, 14, 14, 14,  2,  5,  7,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 3
    [ 0, 13, 15, 13,  3, 12, 12,  9,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 4
    [ 0, 18, 16, 13, 20, 21, 22, 10,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 5
    [ 0, 19, 17, 11, 23, 24, 25, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 6
    [ 0, 11, 11, 11, 26, 27, 28, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 7
    [ 0, 11, 11, 11, 11, 11, 11, 11,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],   # 8
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    
    
    
# X   0   1   2   3   4   5   6   7   8
]

#Begehbare und nicht begehbare Felder zuordnen 
kollision = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 0
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 1
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 2
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 3
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 4
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 5
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 6
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 7
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 8
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 9
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    
    
    
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
# Bewegungs-Zustand des Spielers
spieler_pixel_x = spieler_x * TILE_GROESSE
spieler_pixel_y = spieler_y * TILE_GROESSE
ziel_x, ziel_y = spieler_x, spieler_y
ist_in_bewegung = False

GEH_GESCHWINDIGKEIT = 2
ANIMATION_GESCHWINDIGKEIT = 8
animation_timer = 0
animation_frame_index = 0
DREH_VERZOEGERUNG = 150   # in Millisekunden: so lange muss die Taste nach dem Drehen noch gehalten werden, bevor der Spieler losläuft
spieler_dreh_zeit = 0     # merkt sich, wann zuletzt gedreht wurde
#Startposition der NPCs wie bei Spieler-------------------------------------------------------------

npc_1_x = 5
npc_1_y = 5
npc_1_richtung = "unten"
# Bewegungs-Zustand des NPCs
npc_1_pixel_x = npc_1_x * TILE_GROESSE
npc_1_pixel_y = npc_1_y * TILE_GROESSE
npc_1_ziel_x, npc_1_ziel_y = npc_1_x, npc_1_y
npc_1_ist_in_bewegung = False

npc_1_GEH_GESCHWINDIGKEIT = 2
npc_1_ANIMATION_GESCHWINDIGKEIT = 8
npc_1_animation_timer = 0
npc_1_animation_frame_index = 0
     
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
tileset_pfad = os.path.join(SKRIPT_ORDNER, "..","..", "Assets", "Tilesets", "Bad(64x64).png") # Pfad zum Tileset, ausgehend vom Skript-Ordner / ".." bedeutet eine Ordnerebene nach oben
tileset = pygame.image.load(tileset_pfad).convert() # convert() wandelt das geladene Bild in genau das gleiche Format wie das Fenster um

def hole_tile(tileset, spalte,zeile, groesse):
    rechteck = pygame.Rect(spalte * groesse, zeile * groesse, groesse, groesse)
    return tileset.subsurface(rechteck)

# Koordinaten vom Tileset wird auf die Karte über Zahlen festgelegt------------------------------------------------
tile_bilder = {
    #Schwarzer Rand
    0:  hole_tile(tileset, 4, 0, TILE_GROESSE),
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
    #Waschbecken und Spiegel
    15: hole_tile(tileset, 6, 0, TILE_GROESSE), #Spiegel und Hahn
    16: hole_tile(tileset, 6, 1, TILE_GROESSE), #Becken
    17: hole_tile(tileset, 6, 2, TILE_GROESSE), #Schatten vom Becken
    #Toilette
    18: hole_tile(tileset, 5, 1, TILE_GROESSE),
    19: hole_tile(tileset, 5, 2, TILE_GROESSE), 
    #Teppich
    20: hole_tile(tileset, 7, 0, TILE_GROESSE),
    21: hole_tile(tileset, 8, 0, TILE_GROESSE),
    22: hole_tile(tileset, 9, 0, TILE_GROESSE),
    23: hole_tile(tileset, 7, 1, TILE_GROESSE),
    24: hole_tile(tileset, 8, 1, TILE_GROESSE),
    25: hole_tile(tileset, 9, 1, TILE_GROESSE),
    26: hole_tile(tileset, 7, 2, TILE_GROESSE),
    27: hole_tile(tileset, 8, 2, TILE_GROESSE),
    28: hole_tile(tileset, 9, 2, TILE_GROESSE),
}

# Einfügen von Charakter-Tileset auf Charakter----------------------------------------------------------------------

spieler_spritesheet_pfad = os.path.join(SKRIPT_ORDNER,"..","..", "Assets", "Charakter", "Grundform", "Charakter_Grundform-tranzparent.png") # ".." nach dem SKRIPT_ORDNER nicht vergessen
spieler_spritesheet = pygame.image.load(spieler_spritesheet_pfad).convert_alpha() #wandelt Bild in ein Pixelformat um, dass zum Bildschirm passt

def hole_bild(spritesheet, spalte, zeile , breite , hoehe): # Im Kern das Gleiche wie bei hole_tile nur dass Breite und Höhe jetzt unabhängig sind, statt beide von groesse abzuhängen.
    rechteck = pygame.Rect(spalte * breite, zeile * hoehe, breite, hoehe)
    return spritesheet.subsurface(rechteck)

# Koordinaten vom Tileset des Charakters wird auf die Bewegung über Zahlen festgelegt---------------------------------------------------------------

# Da der Charakter nicht nur aus 64x64px besteht, muss Höhe und Breite beim Charakter neu angepasst werden
CHAR_BREITE = 64
CHAR_HOEHE = 128 

# Beim Spieler ist jetzt eine Kachel 64x128 groß und nicht mehr 64x64, daher verändert sich auch der Index des Charaktersets, also aller 2 Zeilen ist jetzt eine Kachel 
spieler_animation = {
    "unten": {
        "stehen": hole_bild(spieler_spritesheet, 1, 0, CHAR_BREITE, CHAR_HOEHE),
        "gehen": [
            hole_bild(spieler_spritesheet, 0, 0, CHAR_BREITE, CHAR_HOEHE),
            hole_bild(spieler_spritesheet, 2, 0, CHAR_BREITE, CHAR_HOEHE),
        ],
    },
    "oben": {
        "stehen": hole_bild(spieler_spritesheet, 1, 1, CHAR_BREITE, CHAR_HOEHE),
        "gehen": [
            hole_bild(spieler_spritesheet, 0, 1, CHAR_BREITE, CHAR_HOEHE),
            hole_bild(spieler_spritesheet, 2, 1, CHAR_BREITE, CHAR_HOEHE),
        ],
    },
    "links": {
        "stehen": hole_bild(spieler_spritesheet, 1, 2, CHAR_BREITE, CHAR_HOEHE),
        "gehen": [
            hole_bild(spieler_spritesheet, 0, 2, CHAR_BREITE, CHAR_HOEHE),
            hole_bild(spieler_spritesheet, 2, 2, CHAR_BREITE, CHAR_HOEHE),
        ],
    },
    "rechts": {
        "stehen": hole_bild(spieler_spritesheet, 1, 3, CHAR_BREITE, CHAR_HOEHE),
        "gehen": [
            hole_bild(spieler_spritesheet, 0, 3, CHAR_BREITE, CHAR_HOEHE),
            hole_bild(spieler_spritesheet, 2, 3, CHAR_BREITE, CHAR_HOEHE),
        ],
    },
}

def berechne_ziel(x, y, richtung):
    if richtung == "oben":
        return x, y - 1
    elif richtung == "unten":
        return x, y + 1
    elif richtung == "links":
        return x - 1, y
    elif richtung == "rechts":
        return x + 1, y
    return x, y

# Einfügen von NPC_1-Tileset auf NPC_1-----------------------------------------------------------

npc_1_spritesheet_pfad = os.path.join(SKRIPT_ORDNER,"..","..", "Assets", "Charakter", "NPCs", "Katze-tranzparent.png") # ".." nach dem SKRIPT_ORDNER nicht vergessen
npc_1_spritesheet = pygame.image.load(npc_1_spritesheet_pfad).convert_alpha() #wandelt Bild in ein Pixelformat um, dass zum Bildschirm passt

def hole_bild(spritesheet, spalte, zeile , breite , hoehe): # Im Kern das Gleiche wie bei hole_tile nur dass Breite und Höhe jetzt unabhängig sind, statt beide von groesse abzuhängen.
    rechteck = pygame.Rect(spalte * breite, zeile * hoehe, breite, hoehe)
    return spritesheet.subsurface(rechteck)

# Koordinaten vom Tileset des Charakters wird auf die Bewegung über Zahlen festgelegt---------------------------------------------------------------

# Da der Charakter nicht nur aus 64x64px besteht, muss Höhe und Breite beim Charakter neu angepasst werden, in dem Fall aber schon weil es nur die Katze ist
NPC_1_BREITE = 64
NPC_1_HOEHE = 64 

# Beim Spieler ist jetzt eine Kachel 64x128 groß und nicht mehr 64x64, daher verändert sich auch der Index des Charaktersets, also aller 2 Zeilen ist jetzt eine Kachel 
npc_1_animation = {
    "unten": {
        "stehen": hole_bild(npc_1_spritesheet, 0, 0, NPC_1_BREITE, NPC_1_HOEHE),
        "gehen": [
            hole_bild(npc_1_spritesheet, 0, 3, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 2, 3, NPC_1_BREITE, NPC_1_HOEHE),
        ],
    },
    "oben": {
        "stehen": hole_bild(npc_1_spritesheet, 2, 0, NPC_1_BREITE, NPC_1_HOEHE),
        "gehen": [
            hole_bild(npc_1_spritesheet, 1, 3, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 3, 3, NPC_1_BREITE, NPC_1_HOEHE),
        ],
    },
    "links": {
        "stehen": hole_bild(npc_1_spritesheet, 3, 0, NPC_1_BREITE, NPC_1_HOEHE),
        "gehen": [
            hole_bild(npc_1_spritesheet, 0, 1, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 1, 1, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 2, 1, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 3, 1, NPC_1_BREITE, NPC_1_HOEHE),
        ],
    },
    "rechts": {
        "stehen": hole_bild(npc_1_spritesheet, 1, 0, NPC_1_BREITE, NPC_1_HOEHE),
        "gehen": [
            hole_bild(npc_1_spritesheet, 0, 2, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 1, 2, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 2, 2, NPC_1_BREITE, NPC_1_HOEHE),
            hole_bild(npc_1_spritesheet, 3, 2, NPC_1_BREITE, NPC_1_HOEHE),
        ],
    },
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

def zeichne_spieler(bildschirm, spieler_pixel_x, spieler_pixel_y, spieler_richtung, ist_in_bewegung, animation_frame_index):
    if ist_in_bewegung:
        bild = spieler_animation[spieler_richtung]["gehen"][animation_frame_index]
    else:
        bild = spieler_animation[spieler_richtung]["stehen"]

    pixel_x = spieler_pixel_x
    pixel_y = spieler_pixel_y - (CHAR_HOEHE - TILE_GROESSE)
    bildschirm.blit(bild, (pixel_x, pixel_y))

# Funktion für die NPCs-------------------------------------------------------------------------------------------------

def zeichne_npc(bildschirm, npc_1_pixel_x, npc_1_pixel_y, npc_1_richtung, npc_1_ist_in_bewegung, npc_1_animation_frame_index):
    if npc_1_ist_in_bewegung:
        bild = npc_1_animation[npc_1_richtung]["gehen"][npc_1_animation_frame_index]
    else:
        bild = npc_1_animation[npc_1_richtung]["stehen"]

    pixel_x = npc_1_pixel_x
    pixel_y = npc_1_pixel_y - (CHAR_HOEHE - TILE_GROESSE)
    bildschirm.blit(bild, (pixel_x, pixel_y))

#Zuweisung des NPCs und Dauereinstellung eines Events zB. zufällige Bewegung--------------------------------------------

NPC_1_BEWEGUNG_EVENT= pygame.USEREVENT + 1
pygame.time.set_timer(NPC_1_BEWEGUNG_EVENT, 4000) # alle 4000ms = 4 Sekunden

# Game Loop, damit sich das Fenster nicht schließt ----------------------------------------------------------------------------------

laeuft = True
while laeuft:
    for event in pygame.event.get(): # Prüft ob Tasten gedrückt oder Fenster geschlossen werden
        if event.type == pygame.QUIT: 
            laeuft = False

        #Hier kommt die OPTIONALE Möglichkeit, einen NPC einem zufälligen Bewegungsrythmus zuzuweisen
        if event.type == NPC_1_BEWEGUNG_EVENT:
            if not npc_1_ist_in_bewegung:
                richtung = random.choice(["hoch", "runter", "links", "rechts"])

                neues_x = npc_1_x
                neues_y = npc_1_y

                if richtung == "hoch":
                    neues_y = npc_1_y - 1
                    npc_1_richtung = "oben"
                elif richtung == "runter":
                    neues_y = npc_1_y + 1
                    npc_1_richtung = "unten"
                elif richtung == "links":
                    neues_x = npc_1_x -1
                    npc_1_richtung = "links"
                elif richtung == "rechts":
                    neues_x = npc_1_x + 1
                    npc_1_richtung = "rechts"

                if kollision[neues_y][neues_x] != 1:
                    npc_1_ziel_x, npc_1_ziel_y = neues_x, neues_y
                    npc_1_ist_in_bewegung = True

    # Ab hier beginnt die Steuerung des Charakters und die Blickrichtung wird zugewiesen sowie die Animation
    if not ist_in_bewegung:
        tasten = pygame.key.get_pressed()
        gewuenschte_richtung = None

        if tasten[pygame.K_UP]:
            gewuenschte_richtung = "oben"
        elif tasten[pygame.K_DOWN]:
            gewuenschte_richtung = "unten"
        elif tasten[pygame.K_LEFT]:
            gewuenschte_richtung = "links"
        elif tasten[pygame.K_RIGHT]:
            gewuenschte_richtung = "rechts"

        if gewuenschte_richtung is not None:
            if spieler_richtung != gewuenschte_richtung:
                spieler_richtung = gewuenschte_richtung
                spieler_dreh_zeit = pygame.time.get_ticks()  # Zeitpunkt des Drehens merken
            else:
                jetzt = pygame.time.get_ticks()
                if jetzt - spieler_dreh_zeit >= DREH_VERZOEGERUNG:
                    neues_x, neues_y = berechne_ziel(spieler_x, spieler_y, spieler_richtung)
                    if kollision[neues_y][neues_x] != 1:
                        ziel_x, ziel_y = neues_x, neues_y
                        ist_in_bewegung = True
    else:
        ziel_pixel_x = ziel_x * TILE_GROESSE
        ziel_pixel_y = ziel_y * TILE_GROESSE

        if spieler_pixel_x < ziel_pixel_x:
            spieler_pixel_x = min(spieler_pixel_x + GEH_GESCHWINDIGKEIT, ziel_pixel_x)
        elif spieler_pixel_x > ziel_pixel_x:
            spieler_pixel_x = max(spieler_pixel_x - GEH_GESCHWINDIGKEIT, ziel_pixel_x)

        if spieler_pixel_y < ziel_pixel_y:
            spieler_pixel_y = min(spieler_pixel_y + GEH_GESCHWINDIGKEIT, ziel_pixel_y)
        elif spieler_pixel_y > ziel_pixel_y:
            spieler_pixel_y = max(spieler_pixel_y - GEH_GESCHWINDIGKEIT, ziel_pixel_y)

        animation_timer += 1
        if animation_timer >= ANIMATION_GESCHWINDIGKEIT:
            animation_timer = 0
            animation_frame_index = (animation_frame_index + 1) % len(spieler_animation[spieler_richtung]["gehen"])

        if spieler_pixel_x == ziel_pixel_x and spieler_pixel_y == ziel_pixel_y:
            spieler_x, spieler_y = ziel_x, ziel_y
            ist_in_bewegung = False
            animation_timer = 0
            animation_frame_index = 0

    if npc_1_ist_in_bewegung:
        npc_1_ziel_pixel_x = npc_1_ziel_x * TILE_GROESSE
        npc_1_ziel_pixel_y = npc_1_ziel_y * TILE_GROESSE

        if npc_1_pixel_x < npc_1_ziel_pixel_x:
            npc_1_pixel_x = min(npc_1_pixel_x + npc_1_GEH_GESCHWINDIGKEIT, npc_1_ziel_pixel_x)
        elif npc_1_pixel_x > npc_1_ziel_pixel_x:
            npc_1_pixel_x = max(npc_1_pixel_x - npc_1_GEH_GESCHWINDIGKEIT, npc_1_ziel_pixel_x)

        if npc_1_pixel_y < npc_1_ziel_pixel_y:
            npc_1_pixel_y = min(npc_1_pixel_y + npc_1_GEH_GESCHWINDIGKEIT, npc_1_ziel_pixel_y)
        elif npc_1_pixel_y > npc_1_ziel_pixel_y:
            npc_1_pixel_y = max(npc_1_pixel_y - npc_1_GEH_GESCHWINDIGKEIT, npc_1_ziel_pixel_y)

        npc_1_animation_timer += 1
        if npc_1_animation_timer >= npc_1_ANIMATION_GESCHWINDIGKEIT:
            npc_1_animation_timer = 0
            npc_1_animation_frame_index = (npc_1_animation_frame_index + 1) % len(npc_1_animation[npc_1_richtung]["gehen"])

        if npc_1_pixel_x == npc_1_ziel_pixel_x and npc_1_pixel_y == npc_1_ziel_pixel_y:
            npc_1_x, npc_1_y = npc_1_ziel_x, npc_1_ziel_y
            npc_1_ist_in_bewegung = False
            npc_1_animation_timer = 0
            npc_1_animation_frame_index = 0

    bildschirm.fill((0, 0, 0)) #Hier wird die Farbe des Inhalts des Fensters festgelegt
    zeichne_karte(bildschirm, karte)
    zeichne_spieler(bildschirm, spieler_pixel_x, spieler_pixel_y, spieler_richtung, ist_in_bewegung, animation_frame_index)
    zeichne_npc(bildschirm, npc_1_pixel_x, npc_1_pixel_y, npc_1_richtung, npc_1_ist_in_bewegung, npc_1_animation_frame_index)
    pygame.display.flip() #Zeigt das aktuelle Bild an

    uhr.tick(60) # 60 FPS 

pygame.quit()