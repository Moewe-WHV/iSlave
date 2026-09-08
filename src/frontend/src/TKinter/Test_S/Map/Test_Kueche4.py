import tkinter as tk
from test_raum import Raum              # Alles mit template davor kann geändert werden
from test_roboter import Roboter

# ============================================================================
# Bausteine ohne eigenes Verhalten: Farben & Konfiguration
# ============================================================================
from test_modul_konfiguration import Farben, Konfiguration

# ============================================================================
# Baustein: Layout-Berechnung (reine Logik, keine tkinter-Widgets)
# ============================================================================
from test_modul_kuechenlayout import KuechenLayout 

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
# "Chef"-Klasse: steckt alle Bausteine zusammen
# ============================================================================

class KuecheGUI:
    # """Hält Fenster, Raum und Roboter und verbindet die kleinen Bausteine
    # (LegendenPanel, Terminal, RaumCanvas, KuechenLayout) zu einer Anwendung.

    # Diese Klasse baut selbst möglichst wenig - sie delegiert an die
    # spezialisierten Klassen und ruft am Ende nur noch neu_zeichnen()
    # und mainloop() auf.
    # """

    def __init__(self, konfiguration=Konfiguration, farben=Farben):
        self.konfiguration = konfiguration
        self.farben = farben

        # ---- Raum, Roboter, Layout (reine Daten/Logik) ----
        self.zimmer = Raum(name="Küche", hindernisse=[(5, 5), (6, 5), (7, 5)])
        self.roboter = Roboter()
        self.layout = KuechenLayout(self.zimmer.breite, self.zimmer.hoehe, farben)

        # ---- Fenster-Grundgerüst ----
        self.fenster = tk.Tk()
        self.fenster.title("iSlave - Steuerung")
        self.fenster.configure(bg=farben.HINTERGRUND_DUNKEL)

        haupt_rahmen = tk.Frame(self.fenster, bg=farben.HINTERGRUND_DUNKEL)
        haupt_rahmen.pack(fill="both", expand=True)

        rechts_rahmen = tk.Frame(haupt_rahmen, bg=farben.HINTERGRUND_DUNKEL)

        # ---- Bausteine erzeugen ----
        self.legende = LegendenPanel(haupt_rahmen, konfiguration, farben)
        rechts_rahmen.pack(side="left", fill="both", expand=True)
        self.canvas = RaumCanvas(rechts_rahmen, self.zimmer, self.layout,
                                  self.roboter, konfiguration, farben)
        self.terminal = Terminal(rechts_rahmen, self.zimmer, konfiguration, farben)

    def starten(self):
        """Zeichnet die Karte einmal initial und startet die tkinter-Mainloop."""
        self.canvas.neu_zeichnen()
        self.fenster.mainloop()


if __name__ == "__main__":
    app = KuecheGUI()
    app.starten()