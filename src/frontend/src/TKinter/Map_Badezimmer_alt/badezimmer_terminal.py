import tkinter as tk
from tkinter import ttk


class Terminal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.befehle = {}

        self.log = tk.Text(self, height=8, state="disabled", bg="#111111", fg="#33ff33")
        self.log.pack(fill="both", expand=True, padx=4, pady=(4, 2))

        eingabe_frame = ttk.Frame(self)
        eingabe_frame.pack(fill="x", padx=4, pady=(0, 4))

        self.eingabe_var = tk.StringVar()
        self.eingabe_feld = ttk.Entry(eingabe_frame, textvariable=self.eingabe_var)
        self.eingabe_feld.pack(side="left", fill="x", expand=True)
        self.eingabe_feld.bind("<Return>", self._on_enter)

        ttk.Button(eingabe_frame, text="Senden", command=self._on_enter).pack(side="left", padx=(4, 0))

        self.register_command("hilfe", self._befehl_hilfe)
        self.schreibe("Terminal bereit. Tippe 'hilfe' fuer eine Uebersicht.")

    def register_command(self, name, funktion):
         """Registriert einen neuen Befehl. name = Schluesselwort, funktion = Callback."""
         self.befehle[name.lower()] = funktion

    def schreibe(self, text):
        """Schreibt eine Zeile in das Ausgabe-Log."""
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _on_enter(self, event=None):
        eingabe = self.eingabe_var.get().strip()
        self.eingabe_var.set("")
        if not eingabe:
            return

        self.schreibe(f"> {eingabe}")
        teile = eingabe.split()
        befehl = teile[0]
        argumente = teile[1:]

        funktion = self.befehle.get(befehl.lower())
        if funktion is None:
            self.schreibe(f"Unbekannter Befehl: '{befehl}'. Tippe 'hilfe' fuer eine Uebersicht.")
            return

        ergebnis = funktion(argumente)
        if ergebnis:
            self.schreibe(ergebnis)

    def _befehl_hilfe(self, args):
        zeilen = ["Verfuegbare Befehle:"]
        for name in sorted(self.befehle):
            zeilen.append(f"  - {name}")
        return "\n".join(zeilen)

    #-----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    fenster = tk.Tk()
    t = Terminal(fenster)
    t.pack(fill="both", expand=True)
    fenster.mainloop()