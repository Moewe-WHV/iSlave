import pygame


class TileMap:
    """Verwaltet Kartendaten, Kollision und das Tileset."""

    def __init__(self, karte, kollision, tileset_pfad, tile_groesse=64):
        self.karte = karte
        self.kollision = kollision
        self.tile_groesse = tile_groesse

        self._pruefe_dimensionen()

        self.tileset = pygame.image.load(tileset_pfad).convert()
        self.tile_bilder = self._baue_tile_bilder()

    def _pruefe_dimensionen(self):
        assert len(self.karte) == len(self.kollision), \
            "karte und kollision müssen gleich viele Zeilen haben!"
        assert len(self.karte[0]) == len(self.kollision[0]), \
            "karte und kollision müssen gleich viele Spalten haben!"

    def _hole_tile(self, spalte, zeile):
        rechteck = pygame.Rect(
            spalte * self.tile_groesse,
            zeile * self.tile_groesse,
            self.tile_groesse,
            self.tile_groesse,
        )
        return self.tileset.subsurface(rechteck)

    def _baue_tile_bilder(self):
        # Koordinaten vom Tileset werden auf die Kartenzahlen gemappt
        return {
            0: self._hole_tile(4, 0),   # Schwarzer Rand
            1: self._hole_tile(0, 1),   # Dusche
            2: self._hole_tile(0, 2),
            3: self._hole_tile(0, 3),
            4: self._hole_tile(1, 1),   # Fenster
            5: self._hole_tile(1, 2),
            6: self._hole_tile(2, 1),
            7: self._hole_tile(2, 2),
            8: self._hole_tile(4, 2),   # Badewanne
            9: self._hole_tile(4, 3),
            10: self._hole_tile(4, 4),
            11: self._hole_tile(1, 3),  # helle Fliesen
            12: self._hole_tile(2, 3),  # dunkle Fliesen
            13: self._hole_tile(3, 1),  # Wand
            14: self._hole_tile(0, 0),  # Decke
            15: self._hole_tile(6, 0),  # Spiegel und Hahn
            16: self._hole_tile(6, 1),  # Becken
            17: self._hole_tile(6, 2),  # Schatten vom Becken
            18: self._hole_tile(5, 1),  # Toilette
            19: self._hole_tile(5, 2),
            20: self._hole_tile(7, 0),  # Teppich
            21: self._hole_tile(8, 0),
            22: self._hole_tile(9, 0),
            23: self._hole_tile(7, 1),
            24: self._hole_tile(8, 1),
            25: self._hole_tile(9, 1),
            26: self._hole_tile(7, 2),
            27: self._hole_tile(8, 2),
            28: self._hole_tile(9, 2),
        }

    def ist_begehbar(self, x, y):
        return self.kollision[y][x] != 1

    def breite_pixel(self):
        return len(self.karte[0]) * self.tile_groesse

    def hoehe_pixel(self):
        return len(self.karte) * self.tile_groesse

    def zeichne(self, bildschirm):
        for y, zeile in enumerate(self.karte):
            for x, tile in enumerate(zeile):
                bild = self.tile_bilder[tile]
                bildschirm.blit(bild, (x * self.tile_groesse, y * self.tile_groesse))