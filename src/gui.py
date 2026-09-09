"""Tkinter-Kartenansicht (#22).

Zeigt alle vier Raeume gemeinsam als 2D-Top-View und markiert die
aktuelle Roboterposition. Die Ansicht ist reine Anzeige: sie nimmt keine
Eingaben an, gesteuert wird ausschliesslich ueber das Terminal.

Damit das Terminal weiterhin auf input() warten kann, laeuft das Fenster
in einem eigenen Thread und liest den Spielzustand regelmaessig neu.
"""

import threading
import time
import tkinter as tk

import karte

FELDGROESSE = 24
RANDBREITE = 10
AKTUALISIERUNG_SEKUNDEN = 0.3

HINTERGRUND = "#20232a"
SCHRIFTFARBE = "#f0f0f0"
ROBOTERFARBE = "#4caf50"

# Farbe je Kartenzeichen
FARBEN = {
    karte.WAND: "#4a4f5a",
    karte.LEER: "#e8e4d9",
    karte.MOEBEL: "#8d6e63",
    karte.FLECK: "#7e57c2",
    karte.STAUB: "#9e9e9e",
    karte.FUSSEL: "#bdb76b",
    karte.SPUELMITTEL: "#29b6f6",
    karte.LADEKABEL: "#ef5350",
    karte.WERKZEUG: "#ffa726",
}

BESCHRIFTUNG = {
    karte.FLECK: "Fleck",
    karte.STAUB: "Staub",
    karte.FUSSEL: "Fusseln",
    karte.SPUELMITTEL: "Spülmittel",
    karte.LADEKABEL: "Ladekabel",
    karte.WERKZEUG: "Werkzeug",
    karte.MOEBEL: "Möbel",
}


def feld_farbe(zeichen: str) -> str:
    """Farbe eines Kartenfeldes, unbekannte Zeichen werden hell dargestellt."""
    return FARBEN.get(zeichen, FARBEN[karte.LEER])


def feld_rechteck(x: int, y: int, groesse: int = FELDGROESSE) -> tuple:
    """Pixelkoordinaten (links, oben, rechts, unten) eines Feldes."""
    links = RANDBREITE + x * groesse
    oben = RANDBREITE + y * groesse
    return links, oben, links + groesse, oben + groesse


def leinwandgroesse(groesse: int = FELDGROESSE) -> tuple:
    """Benoetigte Breite und Hoehe der Zeichenflaeche in Pixeln."""
    breite = 2 * RANDBREITE + karte.BREITE * groesse
    hoehe = 2 * RANDBREITE + karte.HOEHE * groesse
    return breite, hoehe


def raumbeschriftungen() -> list:
    """Raumname mit Pixelposition oberhalb des Raumes."""
    beschriftungen = []
    for name, (x_von, y_von, x_bis, y_bis) in karte.RAEUME.items():
        mitte_x = RANDBREITE + (x_von + x_bis + 1) * FELDGROESSE / 2
        mitte_y = RANDBREITE + y_von * FELDGROESSE - FELDGROESSE / 3
        beschriftungen.append((name, mitte_x, mitte_y))
    return beschriftungen


class Anzeige:
    """Fenster mit der gemeinsamen Karte aller vier Raeume."""

    def __init__(self, spiel, aktualisierung: float = AKTUALISIERUNG_SEKUNDEN):
        self.spiel = spiel
        self.aktualisierung = aktualisierung
        self._stopp = threading.Event()
        self._thread = None
        self.fenster = None
        self.leinwand = None
        self.statusanzeige = None

    # -- Steuerung ------------------------------------------------------
    def starten(self) -> "Anzeige":
        """Öffnet das Fenster in einem eigenen Thread."""
        self._thread = threading.Thread(target=self._laufen, daemon=True)
        self._thread.start()
        return self

    def schliessen(self) -> None:
        """Bittet das Fenster, sich zu schließen."""
        self._stopp.set()
        if self._thread is not None:
            self._thread.join(timeout=2)

    def laeuft(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    # -- Fensterschleife ------------------------------------------------
    def _laufen(self) -> None:
        try:
            self._aufbauen()
        except tk.TclError as fehler:
            print(f"Kartenansicht konnte nicht geöffnet werden: {fehler}")
            return

        while not self._stopp.is_set():
            try:
                self.zeichnen()
                self.fenster.update()
            except tk.TclError:
                break  # Fenster wurde vom Nutzer geschlossen
            time.sleep(self.aktualisierung)

        try:
            self.fenster.destroy()
        except tk.TclError:
            pass

    def _aufbauen(self) -> None:
        breite, hoehe = leinwandgroesse()

        self.fenster = tk.Tk()
        self.fenster.title("iSlave - Kartenansicht")
        self.fenster.configure(bg=HINTERGRUND)
        self.fenster.resizable(False, False)

        self.statusanzeige = tk.Label(
            self.fenster,
            text="",
            bg=HINTERGRUND,
            fg=SCHRIFTFARBE,
            font=("Consolas", 10),
            anchor="w",
            justify="left",
        )
        self.statusanzeige.pack(fill="x", padx=RANDBREITE, pady=(RANDBREITE, 0))

        self.leinwand = tk.Canvas(
            self.fenster,
            width=breite,
            height=hoehe,
            bg=HINTERGRUND,
            highlightthickness=0,
        )
        self.leinwand.pack(padx=RANDBREITE, pady=RANDBREITE)

        self._legende_aufbauen()

    def _legende_aufbauen(self) -> None:
        legende = tk.Frame(self.fenster, bg=HINTERGRUND)
        legende.pack(fill="x", padx=RANDBREITE, pady=(0, RANDBREITE))

        eintraege = list(BESCHRIFTUNG.items()) + [("R", "Roboter")]
        for spalte, (zeichen, text) in enumerate(eintraege):
            farbe = ROBOTERFARBE if zeichen == "R" else feld_farbe(zeichen)
            tk.Label(legende, text="   ", bg=farbe).grid(
                row=0, column=spalte * 2, padx=(0, 3)
            )
            tk.Label(
                legende,
                text=text,
                bg=HINTERGRUND,
                fg=SCHRIFTFARBE,
                font=("Consolas", 9),
            ).grid(row=0, column=spalte * 2 + 1, padx=(0, 10))

    # -- Zeichnen -------------------------------------------------------
    def zeichnen(self) -> None:
        """Zeichnet Karte, Raumnamen und Roboter neu."""
        self.leinwand.delete("all")

        for y in range(karte.HOEHE):
            for x in range(karte.BREITE):
                links, oben, rechts, unten = feld_rechteck(x, y)
                self.leinwand.create_rectangle(
                    links,
                    oben,
                    rechts,
                    unten,
                    fill=feld_farbe(self.spiel.karte.zeichen(x, y)),
                    outline=HINTERGRUND,
                )

        for name, mitte_x, mitte_y in raumbeschriftungen():
            self.leinwand.create_text(
                mitte_x,
                mitte_y,
                text=name,
                fill=SCHRIFTFARBE,
                font=("Consolas", 9, "bold"),
            )

        self._roboter_zeichnen()
        self.statusanzeige.config(
            text=f"{self.spiel.statuszeile()}\n{self.spiel.ausruestungszeile()}"
        )

    def _roboter_zeichnen(self) -> None:
        links, oben, rechts, unten = feld_rechteck(*self.spiel.roboter.position)
        self.leinwand.create_oval(
            links + 3,
            oben + 3,
            rechts - 3,
            unten - 3,
            fill=ROBOTERFARBE,
            outline=SCHRIFTFARBE,
        )


def anzeige_starten(spiel):
    """Startet die Kartenansicht. Gibt None zurueck, wenn kein Tk laeuft."""
    try:
        return Anzeige(spiel).starten()
    except tk.TclError as fehler:
        print(f"Kartenansicht nicht verfügbar: {fehler}")
        return None
