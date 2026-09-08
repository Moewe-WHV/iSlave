"""Tkinter desktop UI for the isolated MVP."""

from datetime import date
from pathlib import Path
import queue
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from .core import ACTIONS, HEIGHT, ROOMS, WIDTH, Simulation, Store, next_service

BG = "#eef2f5"
INK = "#172b3a"
MUTED = "#607582"
TEAL = "#087f78"


class App:
    def __init__(self, root, store=None, auto_tick=True, terminal=False):
        self.root = root
        self.store = store or Store(Path(__file__).parent / "data" / "profiles.json")
        self.sim = Simulation()
        self.timer = None
        self.auto_tick = auto_tick
        self.terminal = terminal
        self.inbox = queue.Queue()
        root.title("iSlave · Haushaltsroboter")
        root.geometry("1220x840")
        root.minsize(980, 760)
        root.configure(bg=BG)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.configure_style()
        self.build()
        self.log("Willkommen. Profil laden oder direkt mit Demo starten.")
        self.log("Raum wählen und Auftrag starten. 'hilfe' zeigt alle Befehle.")
        try:
            self.sim = Simulation(self.store.load("Demo"))
        except (ValueError, OSError) as exc:
            self.log(str(exc))
        self.refresh()
        self.command.focus_set()
        if auto_tick:
            self.schedule()

    def configure_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=INK, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"))
        style.configure("Sub.TLabel", foreground=MUTED)
        style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 6))
        style.configure("Accent.TButton", background=TEAL, foreground="white")
        style.map(
            "Accent.TButton",
            background=[("active", "#096d68"), ("disabled", "#a2b4b5")],
        )
        style.configure("TProgressbar", background=TEAL, troughcolor="#dce5e8")

    def build(self):
        shell = ttk.Frame(self.root, padding=22)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(1, weight=1)
        header = ttk.Frame(shell)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        ttk.Label(header, text="iSlave", style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="DEIN HAUSHALT. DEIN HELFER.", style="Sub.TLabel").pack(
            side="left", padx=20
        )
        ttk.Label(header, text="DESKTOP MVP  /  SIMULATION", style="Sub.TLabel").pack(
            side="right"
        )
        body = ttk.Frame(shell)
        body.grid(row=1, column=0, sticky="nsew")
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        center = ttk.Frame(body)
        center.grid(row=0, column=0, sticky="nsew")
        self.room_title = ttk.Label(center, style="Heading.TLabel")
        self.room_title.pack(anchor="w")
        ttk.Label(
            center,
            text="Gesamte Wohnung · Steuerung über das Terminal unten",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(3, 10))
        self.canvas = tk.Canvas(
            center, bg="#e3e9ec", highlightthickness=0, width=600, height=420
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda event: self.draw())
        ttk.Label(
            center,
            text="● Roboter     ▧ Möbel     ▪ Mint: bearbeitete Fläche",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=8)
        self.progress = ttk.Progressbar(center, maximum=100)
        self.progress.pack(fill="x", pady=(0, 6))
        self.activity = ttk.Label(center, style="Sub.TLabel")
        self.activity.pack(anchor="w")

        right = ttk.Frame(body, width=200)
        right.grid(row=0, column=1, sticky="ns", padx=(18, 0))
        ttk.Label(right, text="ROBOTERSTATUS", style="Heading.TLabel").pack(anchor="w")
        self.battery_text = ttk.Label(right, font=("Segoe UI", 24, "bold"))
        self.battery_text.pack(anchor="w", pady=(8, 0))
        self.battery_bar = ttk.Progressbar(right, maximum=100, length=195)
        self.battery_bar.pack(fill="x", pady=(4, 10))
        self.details = ttk.Label(right, justify="left", style="Sub.TLabel")
        self.details.pack(anchor="w", pady=(0, 14))
        ttk.Label(right, text="BEFEHLSÜBERSICHT", style="Heading.TLabel").pack(
            anchor="w", pady=(14, 10)
        )
        ttk.Label(
            right,
            text=(
                "nutzer Dein Name\nprofile\nraum Küche\nsaugen / wischen / spülen\n"
                "stopp / status\nladen / nachfüllen\n"
                "wartung / neustart\nspeichern / hilfe"
            ),
            style="Sub.TLabel",
            justify="left",
        ).pack(anchor="w")
        ttk.Label(
            right,
            text="Befehl eingeben + Enter.\nRaumwechsel erfolgt sofort.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=16)

        bottom = ttk.Frame(shell)
        bottom.grid(row=2, column=0, sticky="ew", pady=(18, 0))
        ttk.Label(bottom, text="BEFEHLE & VERLAUF", style="Heading.TLabel").pack(
            anchor="w", pady=(0, 8)
        )
        self.history = tk.Text(
            bottom,
            height=7,
            width=1,
            bg="#152b37",
            fg="#d1e9e7",
            font=("Consolas", 10),
            relief="flat",
            padx=12,
            pady=8,
            state="disabled",
        )
        self.history.pack(fill="x")
        input_row = ttk.Frame(bottom)
        input_row.pack(fill="x", pady=(8, 0))
        self.command = ttk.Entry(input_row, font=("Segoe UI", 11))
        self.command.pack(side="left", fill="x", expand=True, ipady=5)
        self.command.bind("<Return>", self.submit)
        ttk.Button(input_row, text="Senden", command=self.submit).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(input_row, text="Hilfe", command=self.help).pack(
            side="left", padx=(8, 0)
        )

    def log(self, text):
        if self.terminal:
            print(text, flush=True)
        self.history.configure(state="normal")
        self.history.insert("end", text + "\n")
        if int(self.history.index("end-1c").split(".")[0]) > 200:
            self.history.delete("1.0", "2.0")
        self.history.see("end")
        self.history.configure(state="disabled")

    def refresh(self):
        state = self.sim.state
        self.room_title["text"] = (
            f"Wohnungsübersicht  /  {state.name}  /  Roboter: {state.room}"
        )
        self.battery_text["text"] = f"{state.battery:.0f} % Akku"
        self.battery_bar["value"] = state.battery
        due = next_service(date.fromisoformat(state.last_service))
        service = "FÄLLIG" if due <= date.today() else due.strftime("%d.%m.%Y")
        self.details["text"] = (
            f"Spülmittel: {state.detergent} / 4\n"
            f"Ladezyklen: {state.cycles:.2f}\nWartung: {service}\n"
            f"Erledigte Aufträge: {sum(map(len, state.completed.values()))}"
        )
        self.progress["value"] = 100 * self.sim.done / max(1, self.sim.total)
        self.activity["text"] = (
            f"{self.sim.action} · {self.sim.done}/{self.sim.total} Schritte"
            if self.sim.busy
            else "Bereit · "
            + (
                ", ".join(state.completed[state.room])
                or "Noch keine Aufträge abgeschlossen"
            )
        )
        self.draw()

    def draw(self):
        if not hasattr(self, "canvas"):
            return
        c = self.canvas
        c.delete("all")
        gap, label = 22, 28
        size = min(
            (max(c.winfo_width(), 100) - gap * 3) / (WIDTH * 2),
            (max(c.winfo_height(), 100) - gap * 3 - label * 2) / (HEIGHT * 2),
        )
        size = max(2, size)
        full_w = WIDTH * size * 2 + gap
        full_h = (HEIGHT * size + label) * 2 + gap
        left = (c.winfo_width() - full_w) / 2
        top = (c.winfo_height() - full_h) / 2
        for index, room in enumerate(ROOMS.values()):
            ox = left + (index % 2) * (WIDTH * size + gap)
            oy = top + (index // 2) * (HEIGHT * size + label + gap) + label
            active = room.name == self.sim.state.room
            tag = "room:" + room.name
            c.create_text(
                ox,
                oy - 15,
                anchor="w",
                text=room.name,
                font=("Segoe UI", 11, "bold"),
                fill=TEAL if active else INK,
                tags=("room-label", tag),
            )
            cleaned = any(
                a in self.sim.state.completed[room.name] for a in ("Saugen", "Wischen")
            )
            for x in range(WIDTH):
                for y in range(HEIGHT):
                    visited = active and (x, y) in self.sim.visited
                    color = "#bbdfd2" if visited or cleaned else "#fbfaf6"
                    c.create_rectangle(
                        ox + x * size,
                        oy + y * size,
                        ox + (x + 1) * size,
                        oy + (y + 1) * size,
                        fill=color,
                        outline="#e1e5e3",
                        tags=(tag,),
                    )
            for name, x, y, w, h in room.furniture:
                c.create_rectangle(
                    ox + x * size + 1,
                    oy + y * size + 1,
                    ox + (x + w) * size - 1,
                    oy + (y + h) * size - 1,
                    fill=room.accent,
                    outline="",
                    tags=(tag,),
                )
                if w >= 2 and size >= 16:
                    c.create_text(
                        ox + (x + w / 2) * size,
                        oy + (y + h / 2) * size,
                        text=name,
                        width=w * size - 2,
                        font=("Segoe UI", 7),
                        fill=INK,
                        tags=(tag,),
                    )
            c.create_rectangle(
                ox,
                oy,
                ox + WIDTH * size,
                oy + HEIGHT * size,
                outline=TEAL if active else "#a1afb7",
                width=3 if active else 1,
                tags=(tag,),
            )
            if active:
                x, y = self.sim.position
                cx, cy = ox + (x + 0.5) * size, oy + (y + 0.5) * size
                radius = max(5, size * 0.4)
                c.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    fill=TEAL,
                    outline="white",
                    width=2,
                    tags=("robot", tag),
                )

    def perform(self, function):
        try:
            result = function()
            if result:
                self.log(result)
        except (ValueError, OSError) as exc:
            self.log(f"Hinweis: {exc}")
        self.refresh()

    def room(self, name):
        def change():
            self.sim.switch_room(name)
            self.persist()
            return f"Raum gewechselt: {name}."

        self.perform(change)

    def start(self, action):
        def begin():
            self.sim.start(action)
            self.persist()
            return f"Auftrag gestartet: {action} in {self.sim.state.room}."

        self.perform(begin)

    def stop(self):
        self.sim.stop()
        self.log("Auftrag gestoppt. Bisheriger Verbrauch bleibt erhalten.")
        self.save(quiet=True)
        self.refresh()

    def service(self, command):
        def run():
            result = self.sim.maintenance_action(command)
            self.persist()
            return result

        self.perform(run)

    def persist(self):
        self.store.save(self.sim.state)

    def save(self, quiet=False):
        try:
            self.persist()
            if not quiet:
                self.log(
                    "Profil gespeichert. Laufende Aufträge werden "
                    "nach Neustart nicht fortgesetzt."
                )
            return True
        except (ValueError, OSError) as exc:
            self.log(f"Speichern fehlgeschlagen: {exc}")
            return False

    def load_profile(self, name):
        def load():
            if self.sim.busy:
                raise ValueError("Bitte zuerst den laufenden Auftrag stoppen.")
            self.persist()
            target = self.store.load(name)
            self.sim = Simulation(target)
            self.persist()
            return f"Profil {target.name} geladen."

        self.perform(load)

    def step(self):
        if self.sim.busy:
            result = self.sim.tick()
            if result:
                self.log(result)
                self.save(quiet=True)
            self.refresh()

    def schedule(self):
        for _ in range(20):
            try:
                text = self.inbox.get_nowait()
            except queue.Empty:
                break
            self.execute(text)
        self.step()
        self.timer = self.root.after(65, self.schedule)

    def help(self):
        self.log("Profil: nutzer Dein Name | profile. Räume: raum Küche | raum Bad")
        self.log("Aufträge: saugen | wischen | spülen | stopp | status")
        self.log("Service: laden | nachfüllen | wartung | neustart | speichern | hilfe")
        self.log(
            "Saugen: 15 % Akku. Wischen: 20 % + 1 Spülmittel. "
            "Spülen: 10 % + 1 Spülmittel (Küche). Mindestakku: 20 %."
        )

    def submit(self, event=None):
        text = self.command.get().strip()
        self.command.delete(0, "end")
        if not text:
            return
        self.execute(text)

    def execute(self, text):
        self.log("> " + text)
        lower = text.casefold()
        if lower.startswith("nutzer "):
            self.load_profile(text[7:].strip())
        elif lower == "profile":
            self.perform(
                lambda: "Profile: "
                + (", ".join(sorted(self.store.read())) or "Noch keine")
            )
        elif lower.startswith("raum "):
            name = text[5:].strip().casefold()
            target = next((n for n in ROOMS if n.casefold() == name), text[5:].strip())
            self.room(target)
        elif lower in {a.casefold() for a in ACTIONS}:
            self.start(next(a for a in ACTIONS if a.casefold() == lower))
        elif lower in ("laden", "nachfüllen", "wartung", "neustart"):
            self.service(lower)
        elif lower == "stopp":
            self.stop()
        elif lower == "speichern":
            self.save()
        elif lower == "hilfe":
            self.help()
        elif lower == "status":
            self.log(
                f"{self.sim.state.name} · {self.sim.state.room} · "
                f"{self.sim.state.battery:.0f} % Akku · "
                f"{self.sim.action or 'Bereit'}"
            )
        else:
            self.log("Unbekannter Befehl oder falsche Syntax. 'hilfe' zeigt Beispiele.")

    def close(self):
        if not self.save(quiet=True):
            if not messagebox.askyesno(
                "Speichern fehlgeschlagen",
                "Trotzdem schließen? Änderungen seit der letzten "
                "Speicherung gehen verloren.",
                parent=self.root,
            ):
                return
        if self.timer:
            self.root.after_cancel(self.timer)
        self.root.destroy()


def main():
    root = tk.Tk()
    terminal = "--terminal" in sys.argv
    app = App(root, terminal=terminal)
    if terminal:

        def read_commands():
            for line in sys.stdin:
                text = line.strip()
                if text:
                    app.inbox.put(text)

        threading.Thread(target=read_commands, daemon=True).start()
    root.mainloop()
