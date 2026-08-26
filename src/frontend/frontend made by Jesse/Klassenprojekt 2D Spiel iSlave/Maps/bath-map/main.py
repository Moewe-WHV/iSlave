import os
import pygame

from tilemap import TileMap
from spieler import Spieler
from npc import NPC

pygame.init()

TILE_GROESSE = 64

# Aussehen der Karte durch das Tileset ------------------------------------------------------
karte = [                                   # Y
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0],   # 0
    [ 0,  0,  0,  0, 14, 14, 14, 14,  0],   # 1
    [ 0,  0,  0,  0,  1,  4,  6, 13,  0],   # 2
    [ 0, 14, 14, 14,  2,  5,  7,  8,  0],   # 3
    [ 0, 13, 15, 13,  3, 12, 12,  9,  0],   # 4
    [ 0, 18, 16, 13, 20, 21, 22, 10,  0],   # 5
    [ 0, 19, 17, 11, 23, 24, 25, 11,  0],   # 6
    [ 0, 11, 11, 11, 26, 27, 28, 11,  0],   # 7
    [ 0, 11, 11, 11, 11, 11, 11, 11,  0],   # 8
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0],   # 9
# X   0   1   2   3   4   5   6   7   8
]

# Begehbare und nicht begehbare Felder -------------------------------------------------------
kollision = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 0
    [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
    [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 2
    [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 3
    [1, 1, 1, 1, 1, 0, 0, 1, 1],  # 4
    [1, 1, 1, 1, 0, 0, 0, 0, 1],  # 5
    [1, 0, 0, 0, 0, 0, 0, 0, 1],  # 6
    [1, 0, 0, 0, 0, 0, 0, 0, 1],  # 7
    [1, 0, 0, 0, 0, 0, 0, 0, 1],  # 8
    [1, 1, 1, 1, 1, 1, 1, 1, 1],  # 9
]

# Asset-Pfade, relativ zu diesem Skript-Ordner -----------------------------------------------
SKRIPT_ORDNER = os.path.dirname(__file__)
tileset_pfad = os.path.join(SKRIPT_ORDNER, "..", "..", "Assets", "Tilesets", "Bad(64x64).png")
spieler_spritesheet_pfad = os.path.join(
    SKRIPT_ORDNER, "..", "..", "Assets", "Charakter", "Hauptcharakter", "Roboter-tranzparent.png"
)
npc_spritesheet_pfad = os.path.join(
    SKRIPT_ORDNER, "..", "..", "Assets", "Charakter", "NPCs", "Katze-tranzparent.png"
)

# Fenstergröße lässt sich direkt aus der Karte ableiten, ganz ohne TileMap-Objekt
breite = len(karte[0]) * TILE_GROESSE
hoehe = len(karte) * TILE_GROESSE

# WICHTIG: Das Fenster muss existieren, BEVOR irgendein Bild mit .convert()
# oder .convert_alpha() geladen wird (TileMap, Spieler, NPC) - sonst:
# "pygame.error: No video mode has been set"
bildschirm = pygame.display.set_mode((breite, hoehe))
pygame.display.set_caption("Karte testen")
uhr = pygame.time.Clock()

# Aufbau von Karte, Spieler und NPC ----------------------------------------------------------
tilemap = TileMap(karte, kollision, tileset_pfad, TILE_GROESSE)

# Spieler und NPC -----------------------------------------------------------------------------
spieler = Spieler(2, 7, TILE_GROESSE, spieler_spritesheet_pfad)
npc_1 = NPC(5, 5, TILE_GROESSE, npc_spritesheet_pfad)

# Game Loop -------------------------------------------------------------------------------------
laeuft = True
while laeuft:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laeuft = False
        npc_1.verarbeite_event(event, tilemap)

    spieler.verarbeite_eingabe(tilemap)
    spieler.aktualisiere_bewegung()
    npc_1.aktualisiere_bewegung()

    bildschirm.fill((0, 0, 0))
    tilemap.zeichne(bildschirm)
    spieler.zeichne(bildschirm)
    npc_1.zeichne(bildschirm)
    pygame.display.flip()

    uhr.tick(60)

pygame.quit()