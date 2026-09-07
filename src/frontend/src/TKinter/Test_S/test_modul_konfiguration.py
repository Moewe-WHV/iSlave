class Farben:
    """Reine Sammlung von Farbwerten. Enthält keine Logik, nur Konstanten,
    damit alle anderen Klassen dieselben Farben verwenden."""

    BODEN = "#efe3a3"           # helles Beige/Gelb
    ARBEITSFLAECHE = "#b9764a"  # Braun
    KUEHLSCHRANK = "#808080"    # Grau
    KOCHFELD = "#000000"        # Schwarz
    TISCH = "#b9764a"           # Braun (wie Arbeitsfläche)
    STUHL = "#c98b5e"           # helleres Braun
    RASTER = "#c9bd7d"
    ROBOTER = "#2b7a0b"

    HINTERGRUND_DUNKEL = "#2b2b2b"
    HINTERGRUND_TERMINAL = "#0c0c0c"
    HINTERGRUND_TITELLEISTE = "#3a3a3a"
    TEXT_HELL = "white"
    TERMINAL_TEXT = "#4be04b"


class Konfiguration:
    """Reine Sammlung von Größen/Stellschrauben. Auch hier: keine Logik,
    nur Werte, die andere Klassen zum Bauen der Oberfläche brauchen."""

    TILE_SIZE = 64          # Größe der Kacheln in Pixel (zb 64x64 px)
    LEGENDE_BREITE = 190
    TERMINAL_ZEILEN = 8     # sichtbare Zeilen im Terminal (bestimmt die Höhe automatisch)