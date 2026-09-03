import tkinter as tk
from frontend.src.TKinter.template.template_raum import Raum              # Alles mit template davor kann geändert werden
from frontend.src.TKinter.template.template_roboter import Roboter

# ----------------------------------------------------------------------------------
# Konfiguration
# ----------------------------------------------------------------------------------
TILE_SIZE = 64      # Größe der Kacheln in Pixel (zb 64x64 px)
LEGENDE_BREITE = 190
TERMINAL_ZEILEN = 8   # sichtbare Zeilen im Terminal (bestimmt die Höhe automatisch)

# Farben passend zum Küchen-Schema aus der Vorlage
FARBE_BODEN        = "#efe3a3"   # helles Beige/Gelb
FARBE_ARBEITSFLAECHE = "#b9764a"   # Braun
FARBE_KUEHLSCHRANK  = "#808080"   # Grau
FARBE_KOCHFELD      = "#000000"   # Schwarz
FARBE_TISCH         = "#b9764a"   # Braun (wie Arbeitsfläche)
FARBE_STUHL         = "#c98b5e"   # helleres Braun
FARBE_RASTER        = "#c9bd7d"

# ----------------------------------------------------------------------------------
# Raum und Roboter
# ----------------------------------------------------------------------------------
zimmer = Raum(name="Küche", hindernisse=[(5, 5), (6, 5), (7, 5)])  # wenn keine Hindernisse dann None
roboter = Roboter()


def kuechen_layout(breite, hoehe):
    """Berechnet, welche Kacheln zu welchem Küchenmöbel gehören.

    Gibt ein Dict {(gx, gy): (farbe, label)} zurück. label ist nur bei der
    jeweils mittleren Kachel eines Möbelstücks gesetzt (fürs Beschriften).
    Die Positionen werden proportional zur Raumgröße berechnet, damit das
    Layout unabhängig von zimmer.breite/zimmer.hoehe funktioniert.
    """
    layout = {}

    # --- Schrankzeile links (Kochfeld / Arbeitsfläche / Kühlschrank) ---
    schrank_breite = max(2, round(breite * 0.25))
    kochfeld_ende = max(1, round(hoehe * 0.27))
    arbeitsflaeche_ende = max(kochfeld_ende + 1, round(hoehe * 0.71))

    for gx in range(0, schrank_breite):
        for gy in range(0, hoehe):
            if gy < kochfeld_ende:
                layout[(gx, gy)] = (FARBE_KOCHFELD, None)
            elif gy < arbeitsflaeche_ende:
                layout[(gx, gy)] = (FARBE_ARBEITSFLAECHE, None)
            else:
                layout[(gx, gy)] = (FARBE_KUEHLSCHRANK, None)

    # Labels mittig in jedes der drei Segmente setzen
    mitte_x = schrank_breite // 2
    if kochfeld_ende > 0:
        layout[(mitte_x, kochfeld_ende // 2)] = (FARBE_KOCHFELD, "3")
    layout[(mitte_x, (kochfeld_ende + arbeitsflaeche_ende) // 2)] = (FARBE_ARBEITSFLAECHE, "1")
    layout[(mitte_x, (arbeitsflaeche_ende + hoehe) // 2)] = (FARBE_KUEHLSCHRANK, "2")

    # --- Tisch rechts oben ---
    tisch_x0 = round(breite * 0.55)
    tisch_x1 = max(tisch_x0 + 1, round(breite * 0.85) - 1)
    tisch_y0 = round(hoehe * 0.15)
    tisch_y1 = max(tisch_y0 + 1, round(hoehe * 0.45) - 1)

    for gx in range(tisch_x0, tisch_x1 + 1):
        for gy in range(tisch_y0, tisch_y1 + 1):
            layout[(gx, gy)] = (FARBE_TISCH, None)
    layout[((tisch_x0 + tisch_x1) // 2, (tisch_y0 + tisch_y1) // 2)] = (FARBE_TISCH, "4")

    # --- Stühle rund um den Tisch (nur optisch, blockieren nichts) ---
    stuehle = {
        "6": (tisch_x0,     tisch_y0 - 1),  # oben links
        "8": (tisch_x1,     tisch_y0 - 1),  # oben rechts
        "7": (tisch_x0,     tisch_y1 + 1),  # unten links
        "5": (tisch_x1,     tisch_y1 + 1),  # unten rechts
    }
    for label, (sx, sy) in stuehle.items():
        if 0 <= sx < breite and 0 <= sy < hoehe:
            layout[(sx, sy)] = (FARBE_STUHL, label)

    return layout


KUECHEN_MOEBEL = kuechen_layout(zimmer.breite, zimmer.hoehe)

# ----------------------------------------------------------------------------------
# Fenster-Grundgerüst
# ----------------------------------------------------------------------------------
fenster = tk.Tk()
fenster.title("iSlave - Steuerung")
fenster.configure(bg="#2b2b2b")

haupt_rahmen = tk.Frame(fenster, bg="#2b2b2b")
haupt_rahmen.pack(fill="both", expand=True)

# ---- Legende links ----
legende_rahmen = tk.Frame(haupt_rahmen, width=LEGENDE_BREITE, bg="#2b2b2b")
legende_rahmen.pack(side="left", fill="y")
legende_rahmen.pack_propagate(False)


def baue_legende(parent):
    tk.Label(parent, text="Legende", font=("Segoe UI", 13, "bold"),
             fg="white", bg="#2b2b2b").pack(anchor="w", padx=10, pady=(15, 10))

    eintraege = [
        (FARBE_ARBEITSFLAECHE, "1: Arbeitsfläche"),
        (FARBE_KUEHLSCHRANK, "2: Kühlschrank"),
        (FARBE_KOCHFELD, "3: Kochfeld"),
        (FARBE_TISCH, "4: Tisch"),
        (FARBE_STUHL, "5 – 8: Stühle"),
    ]

    for farbe, text in eintraege:
        zeile = tk.Frame(parent, bg="#2b2b2b")
        zeile.pack(anchor="w", padx=10, pady=4, fill="x")
        swatch = tk.Canvas(zeile, width=18, height=18, bg="#2b2b2b",
                            highlightthickness=0)
        swatch.pack(side="left")
        swatch.create_rectangle(1, 1, 17, 17, fill=farbe, outline="white")
        tk.Label(zeile, text=text, fg="white", bg="#2b2b2b",
                 font=("Segoe UI", 10)).pack(side="left", padx=8)

    tk.Frame(parent, bg="#555555", height=1).pack(fill="x", padx=10, pady=15)

    zeile = tk.Frame(parent, bg="#2b2b2b")
    zeile.pack(anchor="w", padx=10, pady=4, fill="x")
    swatch = tk.Canvas(zeile, width=18, height=18, bg="#2b2b2b", highlightthickness=0)
    swatch.pack(side="left")
    swatch.create_oval(2, 2, 16, 16, fill="#2b7a0b", outline="black")
    tk.Label(zeile, text="Roboter", fg="white", bg="#2b2b2b",
             font=("Segoe UI", 10)).pack(side="left", padx=8)


baue_legende(legende_rahmen)

# ---- Rechter Bereich: Canvas oben, Konsole unten ----
rechts_rahmen = tk.Frame(haupt_rahmen, bg="#2b2b2b")
rechts_rahmen.pack(side="left", fill="both", expand=True)

canvas = tk.Canvas(
    rechts_rahmen,
    width=zimmer.breite * TILE_SIZE,
    height=zimmer.hoehe * TILE_SIZE,
    bg=FARBE_BODEN,
    highlightthickness=0,
)
canvas.pack(side="top")


def zeichne_karte():
    """Löscht die Zeichenfläche und zeichnet Küche, Raster und Roboter neu."""
    canvas.delete("all")  # alles Vorherige wird entfernt, sonst stapeln sich die Zeichnungen

    # Raster inkl. Küchenmöbel zeichnen
    for gx in range(zimmer.breite):
        for gy in range(zimmer.hoehe):
            x0 = gx * TILE_SIZE
            y0 = gy * TILE_SIZE
            x1 = x0 + TILE_SIZE
            y1 = y0 + TILE_SIZE

            if (gx, gy) in KUECHEN_MOEBEL:
                fill, label = KUECHEN_MOEBEL[(gx, gy)]
            else:
                fill, label = FARBE_BODEN, None

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline=FARBE_RASTER)

            if label is not None:
                textfarbe = "white" if fill != FARBE_STUHL else "black"
                canvas.create_text(x0 + TILE_SIZE / 2, y0 + TILE_SIZE / 2,
                                    text=label, fill=textfarbe,
                                    font=("Segoe UI", 11, "bold"))

    # Roboter zeichnen (Platzhalter: grüner Kreis)
    rx0 = roboter.x * TILE_SIZE + 6
    ry0 = roboter.y * TILE_SIZE + 6
    rx1 = rx0 + TILE_SIZE - 12
    ry1 = ry0 + TILE_SIZE - 12
    canvas.create_oval(rx0, ry0, rx1, ry1, fill="#2b7a0b", outline="black", width=2)


# ---- Befehlsterminal unten (nur Optik, noch nicht steuerbar) ----
terminal_rahmen = tk.Frame(rechts_rahmen, bg="#1e1e1e")
terminal_rahmen.pack(side="bottom", fill="x")


def baue_terminal(parent):
    """Rein dekoratives Befehlsterminal. Zeigt aus wie eine echte Konsole,
    ist aber (noch) nicht mit dem Roboter verbunden – dient aktuell nur
    der Optik. Die Höhe ergibt sich automatisch aus TERMINAL_ZEILEN,
    damit nichts abgeschnitten wird."""

    # Titelleiste im "Fenster"-Look (macOS-artige Kreise, nur Deko)
    titelleiste = tk.Frame(parent, bg="#3a3a3a", height=26)
    titelleiste.pack(side="top", fill="x")
    titelleiste.pack_propagate(False)

    knopf_rahmen = tk.Frame(titelleiste, bg="#3a3a3a")
    knopf_rahmen.pack(side="left", padx=8)
    for farbe in ("#ff5f56", "#ffbd2e", "#27c93f"):
        punkt = tk.Canvas(knopf_rahmen, width=12, height=12, bg="#3a3a3a", highlightthickness=0)
        punkt.pack(side="left", padx=3)
        punkt.create_oval(1, 1, 11, 11, fill=farbe, outline="")

    tk.Label(titelleiste, text="iSlave – Befehlsterminal", fg="#cccccc",
             bg="#3a3a3a", font=("Consolas", 9)).pack(side="left", padx=6)

    # Eigentlicher Terminal-Textbereich
    text_rahmen = tk.Frame(parent, bg="#0c0c0c")
    text_rahmen.pack(side="top", fill="both", expand=True, padx=1, pady=(0, 1))

    terminal = tk.Text(
        text_rahmen,
        height=TERMINAL_ZEILEN,
        bg="#0c0c0c", fg="#4be04b",
        insertbackground="#4be04b",
        font=("Consolas", 10),
        borderwidth=0, highlightthickness=0,
        wrap="none",
    )
    terminal.pack(side="top", fill="both", expand=True, padx=8, pady=6)

    demo_zeilen = [
        "iSlave System Terminal v0.1",
        "Initialisiere Raum \"Küche\"...",
        f"Raumgröße erkannt: {zimmer.breite} x {zimmer.hoehe} Kacheln",
        "Roboter-Status: bereit",
        "Warte auf Befehl...",
        "> _",
    ]
    terminal.insert("1.0", "\n".join(demo_zeilen))
    terminal.configure(state="disabled")  # noch nicht steuerbar, nur Anzeige


baue_terminal(terminal_rahmen)

# ----------------------------------------------------------------------------------
# Start
# ----------------------------------------------------------------------------------
zeichne_karte()
fenster.mainloop()