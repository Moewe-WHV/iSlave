import random
import pygame
from charakter import Charakter


class NPC(Charakter):
    BREITE = 64
    HOEHE = 64

    def __init__(self, start_x, start_y, tile_groesse, spritesheet_pfad, bewegungs_intervall_ms=4000):
        super().__init__(start_x, start_y, tile_groesse)
        self.spritesheet = pygame.image.load(spritesheet_pfad).convert_alpha()
        self.animation = self._baue_animation()

        # Eigenes Timer-Event für diesen NPC (falls mehrere NPCs: jeder bekommt eine eigene USEREVENT-Nummer)
        self.bewegungs_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.bewegungs_event, bewegungs_intervall_ms)

    def _hole_bild(self, spalte, zeile):
        rechteck = pygame.Rect(
            spalte * self.BREITE, zeile * self.HOEHE,
            self.BREITE, self.HOEHE,
        )
        return self.spritesheet.subsurface(rechteck)

    def _baue_animation(self):
        return {
            "unten": {
                "stehen": self._hole_bild(0, 0),
                "gehen": [self._hole_bild(0, 3), self._hole_bild(2, 3)],
            },
            "oben": {
                "stehen": self._hole_bild(2, 0),
                "gehen": [self._hole_bild(1, 3), self._hole_bild(3, 3)],
            },
            "links": {
                "stehen": self._hole_bild(3, 0),
                "gehen": [
                    self._hole_bild(0, 1), self._hole_bild(1, 1),
                    self._hole_bild(2, 1), self._hole_bild(3, 1),
                ],
            },
            "rechts": {
                "stehen": self._hole_bild(1, 0),
                "gehen": [
                    self._hole_bild(0, 2), self._hole_bild(1, 2),
                    self._hole_bild(2, 2), self._hole_bild(3, 2),
                ],
            },
        }

    def verarbeite_event(self, event, tilemap):
        """Reagiert auf das eigene Timer-Event und wählt eine zufällige Richtung."""
        if event.type != self.bewegungs_event or self.ist_in_bewegung:
            return

        richtung_wahl = random.choice(["hoch", "runter", "links", "rechts"])
        neues_x, neues_y = self.x, self.y

        if richtung_wahl == "hoch":
            neues_y -= 1
            self.richtung = "oben"
        elif richtung_wahl == "runter":
            neues_y += 1
            self.richtung = "unten"
        elif richtung_wahl == "links":
            neues_x -= 1
            self.richtung = "links"
        elif richtung_wahl == "rechts":
            neues_x += 1
            self.richtung = "rechts"

        self.bewege_zu(neues_x, neues_y, tilemap)

    def zeichne(self, bildschirm):
        super().zeichne(bildschirm, self.HOEHE, self.tile_groesse)