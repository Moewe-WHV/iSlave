from test_modul_konfiguration import Konfiguration, Farben
import tkinter as tk

class Terminal:
    """Baut NUR das (noch rein dekorative) Befehlsterminal unten auf.
    Ist aktuell nicht mit dem Roboter verbunden - reine Optik."""

    def __init__(self, parent, zimmer, konfiguration=Konfiguration, farben=Farben):
        self.farben = farben
        self.rahmen = tk.Frame(parent, bg=self.farben.HINTERGRUND_DUNKEL)
        self.rahmen.pack(side="bottom", fill="x")

        self._baue_titelleiste()
        self._baue_textbereich(zimmer, konfiguration)

    def _baue_titelleiste(self):
        """Fenster-Look mit macOS-artigen Kreisen, rein dekorativ."""
        titelleiste = tk.Frame(self.rahmen, bg=self.farben.HINTERGRUND_TITELLEISTE, height=26)
        titelleiste.pack(side="top", fill="x")
        titelleiste.pack_propagate(False)

        knopf_rahmen = tk.Frame(titelleiste, bg=self.farben.HINTERGRUND_TITELLEISTE)
        knopf_rahmen.pack(side="left", padx=8)
        for farbe in ("#ff5f56", "#ffbd2e", "#27c93f"):
            punkt = tk.Canvas(knopf_rahmen, width=12, height=12,
                               bg=self.farben.HINTERGRUND_TITELLEISTE, highlightthickness=0)
            punkt.pack(side="left", padx=3)
            punkt.create_oval(1, 1, 11, 11, fill=farbe, outline="")

        tk.Label(titelleiste, text="iSlave – Befehlsterminal", fg="#cccccc",
                 bg=self.farben.HINTERGRUND_TITELLEISTE,
                 font=("Consolas", 9)).pack(side="left", padx=6)

    def _baue_textbereich(self, zimmer, konfiguration):
        text_rahmen = tk.Frame(self.rahmen, bg=self.farben.HINTERGRUND_TERMINAL)
        text_rahmen.pack(side="top", fill="both", expand=True, padx=1, pady=(0, 1))

        terminal = tk.Text(
            text_rahmen,
            height=konfiguration.TERMINAL_ZEILEN,
            bg=self.farben.HINTERGRUND_TERMINAL, fg=self.farben.TERMINAL_TEXT,
            insertbackground=self.farben.TERMINAL_TEXT,
            font=("Consolas", 10),
            borderwidth=0, highlightthickness=0,
            wrap="none",
        )
        terminal.pack(side="top", fill="both", expand=True, padx=8, pady=6)

        demo_zeilen = [
            "iSlave System Terminal v0.1",
            f"Initialisiere Raum \"{zimmer.name}\"...",
            f"Raumgröße erkannt: {zimmer.breite} x {zimmer.hoehe} Kacheln",
            "Roboter-Status: bereit",
            "Warte auf Befehl...",
            "> _",
        ]
        terminal.insert("1.0", "\n".join(demo_zeilen))
        terminal.configure(state="disabled")  # noch nicht steuerbar, nur Anzeige