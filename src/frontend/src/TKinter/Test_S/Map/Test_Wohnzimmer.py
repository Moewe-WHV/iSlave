import tkinter as tk
from test_raum import Raum
from test_roboter import Roboter

# ============================================================================
# Bausteine ohne eigenes Verhalten: Farben & Konfiguration
# ============================================================================
from test_modul_konfiguration import Farben, Konfiguration

# ============================================================================
# Baustein: Layout-Berechnung fürs Wohnzimmer (reine Logik, keine
# tkinter-Widgets)
# ============================================================================
from test_modul_wohnzimmerlayout import WohnzimmerLayout

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
# KuecheGUI, nur mit dem Wohnzimmer-Grundriss und der passenden Legende).
# ============================================================================


class WohnzimmerGUI:
    """Hält Fenster, Raum und Roboter und verbindet die kleinen Bausteine
    (LegendenPanel, Terminal, RaumCanvas, WohnzimmerLayout) zu einer
    Anwendung."""

    # Legende passend zum Wohnzimmer-Grundriss (siehe Wohnzimmer.pdf)
    LEGENDE = [
        ("LADESTATION", "1: Ladestation"),
        ("FERNSEHTISCH", "2: Fernsehtisch + Fernseher"),
        ("SOFA", "3: Sofa"),
        ("BODEN_WOHNZIMMER", "4: Boden"),
    ]

    def __init__(self, konfiguration=Konfiguration, farben=Farben):
        self.konfiguration = konfiguration
        self.farben = farben

        # ---- Raum, Roboter, Layout (reine Daten/Logik) ----
        self.zimmer = Raum(name="Wohnzimmer", breite=9, hoehe=6,
                            hindernisse=[(0, 0), (0, 1)])
        self.roboter = Roboter(x=4, y=2)
        self.layout = WohnzimmerLayout(self.zimmer.breite, self.zimmer.hoehe, farben)

        # ---- Fenster-Grundgerüst ----
        self.fenster = tk.Tk()
        self.fenster.title("iSlave - Steuerung (Wohnzimmer)")
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
    app = WohnzimmerGUI()
    app.starten()
