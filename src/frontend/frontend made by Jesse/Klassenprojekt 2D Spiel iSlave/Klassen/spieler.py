import pygame
from charakter import Charakter


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


class Spieler(Charakter):
    CHAR_BREITE = 64
    CHAR_HOEHE = 128
    DREH_VERZOEGERUNG = 150  # ms: Taste muss nach dem Drehen noch gehalten werden, bevor gelaufen wird

    def __init__(self, start_x, start_y, tile_groesse, spritesheet_pfad):
        super().__init__(start_x, start_y, tile_groesse)
        self.spritesheet = pygame.image.load(spritesheet_pfad).convert_alpha()
        self.animation = self._baue_animation()
        self.dreh_zeit = 0

    def _hole_bild(self, spalte, zeile):
        rechteck = pygame.Rect(
            spalte * self.CHAR_BREITE, zeile * self.CHAR_HOEHE,
            self.CHAR_BREITE, self.CHAR_HOEHE,
        )
        return self.spritesheet.subsurface(rechteck)

    def _baue_animation(self):
        return {
            "unten": {
                "stehen": self._hole_bild(1, 0),
                "gehen": [self._hole_bild(0, 0), self._hole_bild(2, 0)],
            },
            "oben": {
                "stehen": self._hole_bild(1, 1),
                "gehen": [self._hole_bild(0, 1), self._hole_bild(2, 1)],
            },
            "links": {
                "stehen": self._hole_bild(1, 2),
                "gehen": [self._hole_bild(0, 2), self._hole_bild(2, 2)],
            },
            "rechts": {
                "stehen": self._hole_bild(1, 3),
                "gehen": [self._hole_bild(0, 3), self._hole_bild(2, 3)],
            },
        }

    def verarbeite_eingabe(self, tilemap):
        """Liest Tasten aus, dreht den Spieler oder startet eine Bewegung."""
        if self.ist_in_bewegung:
            return

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

        if gewuenschte_richtung is None:
            return

        if self.richtung != gewuenschte_richtung:
            self.richtung = gewuenschte_richtung
            self.dreh_zeit = pygame.time.get_ticks()
        else:
            jetzt = pygame.time.get_ticks()
            if jetzt - self.dreh_zeit >= self.DREH_VERZOEGERUNG:
                neues_x, neues_y = berechne_ziel(self.x, self.y, self.richtung)
                self.bewege_zu(neues_x, neues_y, tilemap)

    def zeichne(self, bildschirm):
        super().zeichne(bildschirm, self.CHAR_HOEHE, self.tile_groesse)