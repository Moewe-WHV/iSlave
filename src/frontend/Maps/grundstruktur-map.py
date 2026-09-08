import pygame  # import von pygame
import os  # import von os-Modul für Betriebssystem-Funktionen u.a. Dateipfade
import random  # import von random, das zufallsfunktionen bereitstellt

pygame.init()

TILE_GROESSE = 64  # Die Anzahl der Pixel pro Feld

# Die Größe der Karte ---------------------------------------------------------------------------

# Aussehen der Karte durch das Tileset
karte = [  # Y
    [50, 50, 50, 50, 50, 50, 50, 50, 50, 50],  # 0
    [50, 1, 1, 4, 25, 1, 1, 6, 7, 50],  # 1
    [50, 3, 3, 5, 26, 21, 23, 8, 9, 50],  # 2
    [50, 2, 2, 20, 2, 22, 24, 2, 2, 50],  # 3
    [50, 0, 0, 0, 0, 0, 0, 0, 0, 50],  # 4
    [50, 0, 0, 11, 14, 14, 14, 17, 0, 50],  # 5
    [50, 0, 0, 12, 15, 15, 15, 18, 0, 50],  # 6
    [50, 0, 0, 13, 16, 16, 16, 19, 0, 50],  # 7
    [50, 0, 0, 0, 0, 0, 0, 0, 0, 50],  # 8
    [50, 50, 50, 50, 50, 50, 50, 50, 50, 50],  # 9
    # X   0   1   2   3   4   5   6   7   8   9
]

# Begehbare und nicht begehbare Felder zuordnen
kollision = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 2
    [1, 0, 0, 1, 0, 1, 1, 0, 0, 1],  # 3
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 4
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 5
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 6
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 7
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # 8
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 9
]

# Überprüfung, ob Karte und Kollision gleich groß sind, wenn nicht, dann wird es in der Konsole ausgegeben
assert len(karte) == len(
    kollision
), "karte und kollision müssen gleich viele Zeilen haben!"
assert len(karte[0]) == len(
    kollision[0]
), "karte und kollision müssen gleich viele Spalten haben!"

# Farben der Karte wie Wand und Boden (ohne Tileset)----------------------------------------------------------

# Farben = {
# Farben= R   G   B          0 - 255
#    0: (34, 139, 34),       # Boden = Grün
#    1: (105, 105, 105),     # Wand = Grau
# }

# Startposition des Spielers (in Kachel-Koordinaten, nicht in Pixel!)---------------------------------

spieler_x = 2
spieler_y = 7

# Startposition der NPCs wie bei Spieler-------------------------------------------------------------

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
SKRIPT_ORDNER = os.path.dirname(__file__)  # Ordner, in dem diese .py-Datei selbst liegt
tileset_pfad = os.path.join(
    SKRIPT_ORDNER, "..", "Assets", "Tilesets", "Tileset(64x64).png"
)  # Pfad zum Tileset, ausgehend vom Skript-Ordner
tileset = pygame.image.load(
    tileset_pfad
).convert()  # convert() wandelt das geladene Bild in genau das gleiche Format wie das Fenster um


def hole_tile(tileset, spalte, zeile, groesse):
    rechteck = pygame.Rect(spalte * groesse, zeile * groesse, groesse, groesse)
    return tileset.subsurface(rechteck)


# Koordinaten vom Tileset wird auf die Karte über Zahlen festgelegt
tile_bilder = {
    0: hole_tile(tileset, 5, 3, TILE_GROESSE),
    1: hole_tile(tileset, 5, 0, TILE_GROESSE),
    # Boden an der Wand
    2: hole_tile(tileset, 4, 3, TILE_GROESSE),
    3: hole_tile(tileset, 8, 1, TILE_GROESSE),
    # Kühlschrank
    4: hole_tile(tileset, 1, 0, TILE_GROESSE),
    5: hole_tile(tileset, 1, 1, TILE_GROESSE),
    20: hole_tile(tileset, 1, 2, TILE_GROESSE),
    # Fenster
    6: hole_tile(tileset, 6, 0, TILE_GROESSE),
    7: hole_tile(tileset, 7, 0, TILE_GROESSE),
    8: hole_tile(tileset, 6, 1, TILE_GROESSE),
    9: hole_tile(tileset, 7, 1, TILE_GROESSE),
    # Teppich
    11: hole_tile(tileset, 6, 2, TILE_GROESSE),
    12: hole_tile(tileset, 6, 3, TILE_GROESSE),
    13: hole_tile(tileset, 6, 4, TILE_GROESSE),
    14: hole_tile(tileset, 7, 2, TILE_GROESSE),
    15: hole_tile(tileset, 7, 3, TILE_GROESSE),
    16: hole_tile(tileset, 7, 4, TILE_GROESSE),
    17: hole_tile(tileset, 8, 2, TILE_GROESSE),
    18: hole_tile(tileset, 8, 3, TILE_GROESSE),
    19: hole_tile(tileset, 8, 4, TILE_GROESSE),
    # Waschmaschine und Korb
    21: hole_tile(tileset, 3, 1, TILE_GROESSE),
    22: hole_tile(tileset, 3, 2, TILE_GROESSE),
    23: hole_tile(tileset, 4, 1, TILE_GROESSE),
    24: hole_tile(tileset, 4, 2, TILE_GROESSE),
    # Bild an der Wand
    25: hole_tile(tileset, 2, 0, TILE_GROESSE),
    26: hole_tile(tileset, 2, 1, TILE_GROESSE),
    # Schwarzer Rand
    50: hole_tile(tileset, 8, 0, TILE_GROESSE),
}
# Funktion für das Zeichnen der Karte nach fill() und vor flip() im Game Loop---------------------------------------------------


def zeichne_karte(bildschirm, karte):
    for y, zeile in enumerate(
        karte
    ):  # emurate() zeigt den Index beim Durchlauf der Schleife mit an
        for x, tile in enumerate(zeile):
            # Folgendes in den Kommentaren nur anwendbar, wenn ohne Tileset gearbeitet wird
            # farbe = Farben[tile]
            # rechteck = pygame.Rect(x * TILE_GROESSE, y * TILE_GROESSE, TILE_GROESSE, TILE_GROESSE) #pygame.Rect(x_pixel, y_pixel, breite, hoehe) erstellt ein Rechteck
            # pygame.draw.rect(bildschirm, farbe, rechteck) # zeichnet auf bildschirm in der farbe das rechteck
            bild = tile_bilder[tile]
            bildschirm.blit(bild, (x * TILE_GROESSE, y * TILE_GROESSE))


# Funktion für das Zeichnen des Charakters


def zeichne_spieler(bildschirm, spieler_x, spieler_y):
    rechteck = pygame.Rect(
        spieler_x * TILE_GROESSE, spieler_y * TILE_GROESSE, TILE_GROESSE, TILE_GROESSE
    )
    pygame.draw.rect(bildschirm, (255, 0, 0), rechteck)  # Rot, als Platzhalter


# Funktion für die NPCs


def zeichne_npc(bildschirm, npc_x, npc_y):
    rechteck = pygame.Rect(
        npc_x * TILE_GROESSE, npc_y * TILE_GROESSE, TILE_GROESSE, TILE_GROESSE
    )
    pygame.draw.rect(bildschirm, (0, 255, 0), rechteck)  # Grün, als Platzhalter


# Zuweisung des NPCs und Dauereinstellung eines Events zB. zufällige Bewegung

NPC_BEWEGUNG_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(NPC_BEWEGUNG_EVENT, 4000)  # alle 4000ms = 4 Sekunden

# Game Loop, damit sich das Fenster nicht schließt ----------------------------------------------

laeuft = True
while laeuft:
    for (
        event
    ) in pygame.event.get():  # Prüft ob Tasten gedrückt oder Fenster geschlossen werden
        if event.type == pygame.QUIT:
            laeuft = False

        # Hier kommt die OPTIONALE Möglichkeit, einen NPC einem zufälligen Bewegungsrythmus zuzuweisen
        if event.type == NPC_BEWEGUNG_EVENT:
            richtung = random.choice(["hoch", "runter", "links", "rechts"])

            neues_x = npc_x
            neues_y = npc_y

            if richtung == "hoch":
                neues_y = npc_y - 1
            elif richtung == "runter":
                neues_y = npc_y + 1
            elif richtung == "links":
                neues_x = npc_x - 1
            elif richtung == "rechts":
                neues_x = npc_x + 1

            if kollision[neues_y][neues_x] != 1:
                npc_x = neues_x
                npc_y = neues_y

        # Ab hier beginnt die Steuerung des Charakters
        if event.type == pygame.KEYDOWN:
            neues_x = spieler_x
            neues_y = spieler_y

            if event.key == pygame.K_UP:
                neues_y = spieler_y - 1
            elif event.key == pygame.K_DOWN:
                neues_y = spieler_y + 1
            elif event.key == pygame.K_LEFT:
                neues_x = spieler_x - 1
            elif event.key == pygame.K_RIGHT:
                neues_x = spieler_x + 1

            if kollision[neues_y][neues_x] != 1:
                spieler_x = neues_x
                spieler_y = neues_y

    bildschirm.fill(
        (0, 0, 0)
    )  # Hier wird die Farbe des Inhalts des Fensters festgelegt
    zeichne_karte(bildschirm, karte)
    zeichne_spieler(bildschirm, spieler_x, spieler_y)
    zeichne_npc(bildschirm, npc_x, npc_y)
    pygame.display.flip()  # Zeigt das aktuelle Bild an

    uhr.tick(60)  # 60 FPS

pygame.quit()
