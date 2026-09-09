from test_modul_konfiguration import Konfiguration, Farben
import tkinter as tk

class LegendenPanel:
    """Baut NUR die Legende links im Fenster auf. Bekommt einen Elternframe
    und zeichnet dort Farb-Kästchen mit Beschriftung hinein."""

    EINTRAEGE = [
        ("ARBEITSFLAECHE", "1: Arbeitsfläche"),
        ("KUEHLSCHRANK", "2: Kühlschrank"),
        ("KOCHFELD", "3: Kochfeld"),
        ("TISCH", "4: Tisch"),
        ("STUHL", "5 – 8: Stühle"),
    ]

    def __init__(self, parent, konfiguration=Konfiguration, farben=Farben, eintraege=None):
        """eintraege: optionale Liste von (Farb-Attributname, Beschriftung),
        genau wie EINTRAEGE. Damit kann jeder Raum (Küche, Bad, ...) seine
        eigene Legende mitgeben, ohne dass diese Klasse geändert werden muss.
        Wird nichts übergeben, gilt weiterhin die Küchen-Legende (EINTRAEGE)."""
        self.farben = farben
        self.eintraege = eintraege if eintraege is not None else self.EINTRAEGE
        self.rahmen = tk.Frame(parent, width=konfiguration.LEGENDE_BREITE,
                                bg=farben.HINTERGRUND_DUNKEL)
        self.rahmen.pack(side="left", fill="y")
        self.rahmen.pack_propagate(False)

        self._baue_titel()
        for farb_attribut, text in self.eintraege:
            self._baue_eintrag(getattr(farben, farb_attribut), text)
        self._baue_trennlinie()
        self._baue_eintrag(farben.ROBOTER, "Roboter", ist_kreis=True)

    def _baue_titel(self):
        tk.Label(self.rahmen, text="Legende", font=("Segoe UI", 13, "bold"),
                 fg=self.farben.TEXT_HELL, bg=self.farben.HINTERGRUND_DUNKEL
                 ).pack(anchor="w", padx=10, pady=(15, 10))

    def _baue_trennlinie(self):
        tk.Frame(self.rahmen, bg="#555555", height=1).pack(fill="x", padx=10, pady=15)

    def _baue_eintrag(self, farbe, text, ist_kreis=False):
        """Eine einzelne Legenden-Zeile: kleines Farbsymbol + Beschriftung."""
        zeile = tk.Frame(self.rahmen, bg=self.farben.HINTERGRUND_DUNKEL)
        zeile.pack(anchor="w", padx=10, pady=4, fill="x")

        swatch = tk.Canvas(zeile, width=18, height=18,
                            bg=self.farben.HINTERGRUND_DUNKEL, highlightthickness=0)
        swatch.pack(side="left")
        if ist_kreis:
            swatch.create_oval(2, 2, 16, 16, fill=farbe, outline="black")
        else:
            swatch.create_rectangle(1, 1, 17, 17, fill=farbe, outline="white")

        tk.Label(zeile, text=text, fg=self.farben.TEXT_HELL,
                 bg=self.farben.HINTERGRUND_DUNKEL,
                 font=("Segoe UI", 10)).pack(side="left", padx=8)

