import pygame


class Textbox:
    """
    Zeichnet eine einfache Textbox am unteren Bildschirmrand.
    Bekommt bei jedem Frame von main.py gesagt, ob und welcher Text
    gerade angezeigt werden soll.
    """

    def __init__(self, breite, hoehe):
        # Breite/Höhe des Spielfensters, damit die Box sich daran ausrichten kann
        self.breite = breite
        self.hoehe = hoehe

        # Schriftart: None = Standard-Systemschrift von Pygame, 24 = Schriftgröße
        # (muss NACH pygame.init() erstellt werden, deswegen erst hier, nicht als Klassen-Attribut)
        self.schrift = pygame.font.SysFont(None, 28)

        # Maße und Position der Box selbst
        self.box_hoehe = 80
        self.box_rand = 10  # Innenabstand vom Boxrand zum Text

    def zeichne(self, bildschirm, text):
        """Zeichnet die Box nur, wenn 'text' nicht None ist."""
        if text is None:
            return

        # Rechteck für die Box: unten im Fenster, über die volle Breite
        box_rechteck = pygame.Rect(
            0,
            self.hoehe - self.box_hoehe,
            self.breite,
            self.box_hoehe,
        )

        # Box-Hintergrund: dunkles Halbtransparent-Grau
        # Dafür brauchen wir eine eigene Surface mit Alphakanal (SRCALPHA),
        # da bildschirm.fill() selbst keine Transparenz kann
        box_oberflaeche = pygame.Surface((box_rechteck.width, box_rechteck.height), pygame.SRCALPHA)
        box_oberflaeche.fill((0, 0, 0, 200))  # R, G, B, Alpha (200 von 255 = fast deckend)
        bildschirm.blit(box_oberflaeche, box_rechteck.topleft)

        # Weißer Rahmen um die Box, damit sie sich vom Hintergrund abhebt
        pygame.draw.rect(bildschirm, (255, 255, 255), box_rechteck, width=2)

        # Text rendern: render(text, antialiasing, farbe)
        text_oberflaeche = self.schrift.render(text, True, (255, 255, 255))
        text_position = (box_rechteck.x + self.box_rand, box_rechteck.y + self.box_rand)
        bildschirm.blit(text_oberflaeche, text_position)