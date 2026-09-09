"""Rasterbasierte 2D-Karte der Wohnung.

Setzt die User Stories "Umgebung 1" (#29) und "Umgebung 2" (#30) um:
eine gemeinsame Karte mit den vier Raeumen, raeumlicher Trennung durch
Waende, Moebeln als Hindernissen sowie Verschmutzungen und Gegenstaenden,
die der Roboter bearbeiten bzw. aufnehmen kann.
"""

from collections import deque

# Zeichen der Karte
LEER = "."
WAND = "#"
MOEBEL = "M"
FLECK = "F"
STAUB = "S"
FUSSEL = "U"
SPUELMITTEL = "P"
LADEKABEL = "L"
WERKZEUG = "W"

# Verschmutzungen werden beseitigt, Gegenstaende werden aufgenommen
VERSCHMUTZUNGEN = [FLECK, STAUB, FUSSEL]
GEGENSTAENDE = [SPUELMITTEL, LADEKABEL, WERKZEUG]

BREITE = 25
HOEHE = 19

# Raumname -> (x_von, y_von, x_bis, y_bis), jeweils einschliesslich
RAEUME = {
    "Wohnzimmer": (1, 1, 11, 8),
    "Bad": (13, 1, 23, 8),
    "Küche": (1, 10, 11, 17),
    "Schlafzimmer": (13, 10, 23, 17),
}

# Durchgaenge in den Trennwaenden, damit alle Raeume erreichbar bleiben
TUEREN = [(12, 4), (12, 13), (5, 9), (17, 9)]

# Startfeld je Raum (immer begehbar, orientiert an den Mockups)
STARTFELDER = {
    "Wohnzimmer": (1, 1),
    "Bad": (13, 1),
    "Küche": (1, 11),
    "Schlafzimmer": (13, 10),
}

# Moeblierung nach den Mockups: Rechtecke, die als Hindernis gelten
MOEBLIERUNG = [
    (2, 2, 4, 2),  # Wohnzimmer: Sofa
    (6, 4, 7, 5),  # Wohnzimmer: Couchtisch
    (10, 1, 10, 3),  # Wohnzimmer: Regal
    (14, 1, 16, 2),  # Bad: Badewanne
    (19, 1, 20, 1),  # Bad: Waschbecken
    (22, 1, 22, 1),  # Bad: WC
    (1, 10, 4, 10),  # Kueche: Arbeitsplatte
    (11, 10, 11, 11),  # Kueche: Kuehlschrank
    (6, 14, 8, 15),  # Kueche: Esstisch
    (14, 11, 16, 13),  # Schlafzimmer: Bett
    (22, 10, 23, 12),  # Schlafzimmer: Schrank
    (17, 11, 17, 11),  # Schlafzimmer: Nachttisch
]

# Startverschmutzungen ueber alle vier Raeume verteilt
STARTVERSCHMUTZUNGEN = [
    (3, 6, FLECK),
    (8, 2, FUSSEL),
    (9, 7, STAUB),
    (15, 5, FLECK),
    (21, 6, STAUB),
    (2, 13, FLECK),
    (10, 16, FUSSEL),
    (15, 16, STAUB),
    (20, 14, FUSSEL),
    (18, 16, FLECK),
]

# Gegenstaende, die der Roboter automatisch aufnimmt
STARTGEGENSTAENDE = [
    (1, 8, SPUELMITTEL),
    (11, 17, SPUELMITTEL),
    (13, 8, SPUELMITTEL),
    (23, 16, SPUELMITTEL),
    (11, 8, LADEKABEL),
    (23, 17, WERKZEUG),
]


class Karte:
    """Verwaltet das Raster der Wohnung."""

    def __init__(self):
        self.raster = self._raster_aufbauen()
        self._inhalte_setzen(STARTVERSCHMUTZUNGEN)
        self._inhalte_setzen(STARTGEGENSTAENDE)

    # -- Aufbau ---------------------------------------------------------
    def _raster_aufbauen(self) -> list:
        """Erzeugt Waende, Raumflaechen, Tueren und Moebel."""
        raster = [[WAND for _ in range(BREITE)] for _ in range(HOEHE)]

        for x_von, y_von, x_bis, y_bis in RAEUME.values():
            for y in range(y_von, y_bis + 1):
                for x in range(x_von, x_bis + 1):
                    raster[y][x] = LEER

        for x, y in TUEREN:
            raster[y][x] = LEER

        for x_von, y_von, x_bis, y_bis in MOEBLIERUNG:
            for y in range(y_von, y_bis + 1):
                for x in range(x_von, x_bis + 1):
                    raster[y][x] = MOEBEL

        return raster

    def _inhalte_setzen(self, inhalte: list) -> None:
        """Setzt Inhalte nur auf freie Felder, damit Moebel frei bleiben."""
        for x, y, zeichen in inhalte:
            if self.zeichen(x, y) == LEER:
                self.raster[y][x] = zeichen

    # -- Abfragen -------------------------------------------------------
    def zeichen(self, x: int, y: int) -> str:
        """Gibt das Zeichen eines Feldes zurueck, ausserhalb gilt Wand."""
        if 0 <= y < HOEHE and 0 <= x < BREITE:
            return self.raster[y][x]
        return WAND

    def ist_begehbar(self, x: int, y: int) -> bool:
        """Waende und Moebel sind Hindernisse, alles andere ist befahrbar."""
        return self.zeichen(x, y) not in (WAND, MOEBEL)

    def ist_hindernis(self, x: int, y: int) -> bool:
        return not self.ist_begehbar(x, y)

    def raum_von(self, x: int, y: int):
        """Gibt den Raumnamen eines Feldes zurueck, sonst None."""
        for name, (x_von, y_von, x_bis, y_bis) in RAEUME.items():
            if x_von <= x <= x_bis and y_von <= y <= y_bis:
                return name
        return None

    def startfeld(self, raum: str):
        """Begehbares Startfeld eines Raumes."""
        return STARTFELDER.get(raum)

    def felder_im_raum(self, raum: str) -> list:
        """Alle Felder eines Raumes von links oben nach rechts unten."""
        if raum not in RAEUME:
            return []
        x_von, y_von, x_bis, y_bis = RAEUME[raum]
        felder = []
        for y in range(y_von, y_bis + 1):
            for x in range(x_von, x_bis + 1):
                felder.append((x, y))
        return felder

    def suchen(self, zeichen: str, raum: str = None) -> list:
        """Alle Positionen mit dem gesuchten Zeichen."""
        if raum is not None:
            felder = self.felder_im_raum(raum)
        else:
            felder = [(x, y) for y in range(HOEHE) for x in range(BREITE)]
        return [(x, y) for x, y in felder if self.zeichen(x, y) == zeichen]

    def verschmutzungen_im_raum(self, raum: str) -> list:
        """Positionen aller Verschmutzungen eines Raumes."""
        return [
            (x, y)
            for x, y in self.felder_im_raum(raum)
            if self.zeichen(x, y) in VERSCHMUTZUNGEN
        ]

    def gegenstaende_im_raum(self, raum: str) -> list:
        """Positionen aller aufnehmbaren Gegenstaende eines Raumes."""
        return [
            (x, y)
            for x, y in self.felder_im_raum(raum)
            if self.zeichen(x, y) in GEGENSTAENDE
        ]

    def ist_sauber(self, raum: str) -> bool:
        """True, wenn der Raum keine Verschmutzungen mehr enthaelt."""
        return self.verschmutzungen_im_raum(raum) == []

    # -- Veraendern -----------------------------------------------------
    def feld_leeren(self, x: int, y: int) -> str:
        """Entfernt den Inhalt eines Feldes und gibt ihn zurueck."""
        inhalt = self.zeichen(x, y)
        if inhalt in VERSCHMUTZUNGEN or inhalt in GEGENSTAENDE:
            self.raster[y][x] = LEER
        return inhalt

    # -- Wegsuche -------------------------------------------------------
    def nachbarfelder(self, x: int, y: int) -> list:
        """Begehbare Nachbarfelder, ohne Diagonalen."""
        moeglich = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        return [(nx, ny) for nx, ny in moeglich if self.ist_begehbar(nx, ny)]

    def weg_suchen(self, start: tuple, ziel: tuple) -> list:
        """Kuerzester Weg um Hindernisse herum (Breitensuche).

        Gibt die Felder von start (ohne) bis ziel (mit) zurueck. Ist das
        Ziel nicht erreichbar, wird eine leere Liste zurueckgegeben.
        """
        if start == ziel:
            return []
        if not self.ist_begehbar(*ziel):
            return []

        vorgaenger = {start: None}
        warteschlange = deque([start])

        while warteschlange:
            aktuell = warteschlange.popleft()
            if aktuell == ziel:
                return self._weg_zusammensetzen(vorgaenger, ziel)
            for nachbar in self.nachbarfelder(*aktuell):
                if nachbar not in vorgaenger:
                    vorgaenger[nachbar] = aktuell
                    warteschlange.append(nachbar)

        return []

    @staticmethod
    def _weg_zusammensetzen(vorgaenger: dict, ziel: tuple) -> list:
        """Verfolgt die Vorgaenger vom Ziel zum Start zurueck."""
        weg = []
        feld = ziel
        while vorgaenger[feld] is not None:
            weg.append(feld)
            feld = vorgaenger[feld]
        weg.reverse()
        return weg

    # -- Anzeige --------------------------------------------------------
    def als_text(self, position: tuple = None) -> str:
        """Textansicht der Karte, der Roboter wird als R dargestellt."""
        zeilen = []
        for y in range(HOEHE):
            zeichen = []
            for x in range(BREITE):
                if position == (x, y):
                    zeichen.append("R")
                else:
                    zeichen.append(self.raster[y][x])
            zeilen.append("".join(zeichen))
        return "\n".join(zeilen)
