import tkinter as tk
from test_raum import Raum
from test_roboter import Roboter

# ============================================================================
# Bausteine ohne eigenes Verhalten: Farben & Konfiguration
# ============================================================================
from test_modul_konfiguration import Farben, Konfiguration

# ============================================================================
# Baustein: Layout-Berechnung fürs Bad (reine Logik, keine tkinter-Widgets)
# ============================================================================
from test_modul_badlayout import BadLayout

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
# KuecheGUI, nur mit dem Bad-Grundriss und der Bad-Legende).
# ============================================================================


class BadGUI:
    """Hält Fenster, Raum und Roboter und verbindet die kleinen Bausteine
    (LegendenPanel, Terminal, RaumCanvas, BadLayout) zu einer Anwendung."""

    # Legende passend zum Bad-Grundriss (siehe Bad.png)
    LEGENDE = [
        ("DUSCHE", "1: Dusche"),
        ("BADEWANNE", "2: Badewanne"),
        ("TOILETTE", "3: Toilette"),
        ("WASCHBECKEN", "4: Waschbecken"),
        ("WASCHMASCHINE", "5: Waschmaschine"),
        ("WAESCHETROCKNER", "6: Wäschetrockner"),
    ]

    def __init__(self, konfiguration=Konfiguration, farben=Farben):
        self.konfiguration = konfiguration
        self.farben = farben

        # ---- Raum, Roboter, Layout (reine Daten/Logik) ----
        self.zimmer = Raum(name="Bad", breite=11, hoehe=7,
                            hindernisse=[(0, 1), (0, 5)])
        self.roboter = Roboter(x=4, y=3)
        self.layout = BadLayout(self.zimmer.breite, self.zimmer.hoehe, farben)

        # ---- Fenster-Grundgerüst ----
        self.fenster = tk.Tk()
        self.fenster.title("iSlave - Steuerung (Bad)")
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
    app = BadGUI()
    app.starten()
