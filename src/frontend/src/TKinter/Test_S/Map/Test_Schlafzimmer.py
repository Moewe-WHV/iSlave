import tkinter as tk
from test_raum import Raum
from test_roboter import Roboter

# ============================================================================
# Bausteine ohne eigenes Verhalten: Farben & Konfiguration
# ============================================================================
from test_modul_konfiguration import Farben, Konfiguration

# ============================================================================
# Baustein: Layout-Berechnung fürs Schlafzimmer (reine Logik, keine
# tkinter-Widgets)
# ============================================================================
from test_modul_schlafzimmerlayout import SchlafzimmerLayout

# ============================================================================
# Baustein: Legende links
# ============================================================================
from test_modul_legendenpanel import LegendenPanel

# ============================================================================
# Baustein: Deko-Terminal unten
# ============================================================================
from test_modul_terminal import Terminal

# ============================================================================
# Baustein: Zeichenfläche (Kacheln + Roboter)
# ============================================================================
from test_modul_raumcanvas import RaumCanvas

# ============================================================================
# "Chef"-Klasse: steckt alle Bausteine zusammen (identischer Aufbau wie
# KuecheGUI, nur mit dem Schlafzimmer-Grundriss und der passenden Legende).
# ============================================================================


class SchlafzimmerGUI:
    """Hält Fenster, Raum und Roboter und verbindet die kleinen Bausteine
    (LegendenPanel, Terminal, RaumCanvas, SchlafzimmerLayout) zu einer
    Anwendung."""

    # Legende passend zum Schlafzimmer-Grundriss (siehe Schlafzimmer.pdf)
    LEGENDE = [
        ("NACHTTISCH", "1: Nachttisch(e)"),
        ("KLEIDERSCHRANK", "2: Kleiderschrank"),
        ("BODEN_SCHLAFZIMMER", "3: Boden"),
        ("BETT", "4: Bett"),
    ]

    def __init__(self, konfiguration=Konfiguration, farben=Farben):
        self.konfiguration = konfiguration
        self.farben = farben

        # ---- Raum, Roboter, Layout (reine Daten/Logik) ----
        self.zimmer = Raum(name="Schlafzimmer", breite=9, hoehe=7,
                            hindernisse=[(0, 5), (8, 5)])
        self.roboter = Roboter(x=4, y=6)
        self.layout = SchlafzimmerLayout(self.zimmer.breite, self.zimmer.hoehe, farben)

        # ---- Fenster-Grundgerüst ----
        self.fenster = tk.Tk()
        self.fenster.title("iSlave - Steuerung (Schlafzimmer)")
        self.fenster.configure(bg=farben.HINTERGRUND_DUNKEL)

        haupt_rahmen = tk.Frame(self.fenster, bg=farben.HINTERGRUND_DUNKEL)
        haupt_rahmen.pack(fill="both", expand=True)

        rechts_rahmen = tk.Frame(haupt_rahmen, bg=farben.HINTERGRUND_DUNKEL)

        # ---- Bausteine erzeugen ----
        self.legende = LegendenPanel(haupt_rahmen, konfiguration, farben, self.LEGENDE)
        rechts_rahmen.pack(side="left", fill="both", expand=True)
        self.canvas = RaumCanvas(rechts_rahmen, self.zimmer, self.layout,
                                  self.roboter, konfiguration, farben)
        self.terminal = Terminal(rechts_rahmen, self.zimmer, konfiguration, farben)

    def starten(self):
        """Zeichnet die Karte einmal initial und startet die tkinter-Mainloop."""
        self.canvas.neu_zeichnen()
        self.fenster.mainloop()


if __name__ == "__main__":
    app = SchlafzimmerGUI()
    app.starten()
