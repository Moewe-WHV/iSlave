class Charakter:
    """
    Gemeinsame Basisklasse für Spieler und NPCs.
    Enthält die kachelweise Bewegung (sanftes Gleiten von Kachel zu Kachel)
    und die Animations-Frame-Logik. Das eigentliche Sprite-Set (animation-Dict)
    wird von den Unterklassen befüllt.
    """

    def __init__(self, start_x, start_y, tile_groesse,
                 geh_geschwindigkeit=2, animation_geschwindigkeit=16, richtung="unten"):
        self.x = start_x
        self.y = start_y
        self.tile_groesse = tile_groesse

        self.pixel_x = start_x * tile_groesse
        self.pixel_y = start_y * tile_groesse
        self.ziel_x = start_x
        self.ziel_y = start_y

        self.richtung = richtung
        self.ist_in_bewegung = False

        self.geh_geschwindigkeit = geh_geschwindigkeit
        self.animation_geschwindigkeit = animation_geschwindigkeit
        self.animation_timer = 0
        self.animation_frame_index = 0

        # Wird von den Unterklassen gesetzt: {richtung: {"stehen": Bild, "gehen": [Bilder]}}
        self.animation = {}

    def bewege_zu(self, ziel_x, ziel_y, tilemap):
        """Startet eine Bewegung zur Zielkachel, falls diese begehbar ist."""
        if self.ist_in_bewegung:
            return False
        if tilemap.ist_begehbar(ziel_x, ziel_y):
            self.ziel_x, self.ziel_y = ziel_x, ziel_y
            self.ist_in_bewegung = True
            return True
        return False

    def aktualisiere_bewegung(self):
        """Muss jeden Frame aufgerufen werden, bewegt den Charakter Pixel für Pixel zum Ziel."""
        if not self.ist_in_bewegung:
            return

        ziel_pixel_x = self.ziel_x * self.tile_groesse
        ziel_pixel_y = self.ziel_y * self.tile_groesse

        if self.pixel_x < ziel_pixel_x:
            self.pixel_x = min(self.pixel_x + self.geh_geschwindigkeit, ziel_pixel_x)
        elif self.pixel_x > ziel_pixel_x:
            self.pixel_x = max(self.pixel_x - self.geh_geschwindigkeit, ziel_pixel_x)

        if self.pixel_y < ziel_pixel_y:
            self.pixel_y = min(self.pixel_y + self.geh_geschwindigkeit, ziel_pixel_y)
        elif self.pixel_y > ziel_pixel_y:
            self.pixel_y = max(self.pixel_y - self.geh_geschwindigkeit, ziel_pixel_y)

        self.animation_timer += 1
        if self.animation_timer >= self.animation_geschwindigkeit:
            self.animation_timer = 0
            anzahl_frames = len(self.animation[self.richtung]["gehen"])
            self.animation_frame_index = (self.animation_frame_index + 1) % anzahl_frames

        if self.pixel_x == ziel_pixel_x and self.pixel_y == ziel_pixel_y:
            self.x, self.y = self.ziel_x, self.ziel_y
            self.ist_in_bewegung = False
            self.animation_timer = 0
            self.animation_frame_index = 0

    def aktuelles_bild(self):
        if self.ist_in_bewegung:
            return self.animation[self.richtung]["gehen"][self.animation_frame_index]
        return self.animation[self.richtung]["stehen"]

    def zeichne(self, bildschirm, char_hoehe, tile_groesse):
        bild = self.aktuelles_bild()
        pixel_y = self.pixel_y - (char_hoehe - tile_groesse)
        bildschirm.blit(bild, (self.pixel_x, pixel_y))