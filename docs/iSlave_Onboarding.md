# 🤖 Onboarding – iSlave

Hier ist alles, was du brauchst, um von "Repo geklont" zu "erster PR gemerged" zu kommen.

## Was ist iSlave?

Terminalanwendung (Python) zur Steuerung eines humanoiden Haushaltsroboters.
Klassenprojekt der IBB FIAE Umschulung (Winter A1) – **8 Wochen, 6 Sprints**.

## Team (Sprint 1)

| Rolle          | Person                                                                |
| -------------- | --------------------------------------------------------------------- |
| Product Owner  | Jendrik                                                               |
| Scrum Master   | Henning                                                               |
| Teamleiter     | Tim                                                                   |
| Entwicklerteam | Sascha, Benjamin, Phillipp, Niklas, Jesse, Radu, Cicero, Amer, Süheyl |

**Bei Fragen zu Git/GitHub, Branches oder Merge-Konflikten:** Tim ansprechen.

---

## 1. Environment Setup

Repo klonen, dann virtuelle Umgebung anlegen und Dependencies installieren.

**Mac / Linux:**
```bash
git clone https://github.com/Moewe-WHV/iSlave.git
cd iSlave
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

**Windows:**
```bash
git clone https://github.com/Moewe-WHV/iSlave.git
cd iSlave
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

**Testen, ob alles läuft:**
```bash
pytest
```

Wenn das grün durchläuft, bist du startklar.

---

## 2. Projektstruktur – wie hängt das zusammen

```
iSlave/
├── docs/
│   ├── burndown_charts/            # Sprint Burndown Charts
|   ├── mockups/                    # Desgignvorlagen
│   ├── diagrams/                   # Alle Arten von Diagrammen 
│   └── protocols/                  # Sitzungsprotokolle & Daylies
├── src/     
|   ├── frontend/                   # Alle Arten von Diagrammen                        # Hier liegt der Code  
│   └── main.py
├── tests/                          # Test-Skripte
├── .gitignore                      # Was soll beim push ignoriert werden
├── CONTRIBUTING.md                 # GitHub Projekt-Knigge
├── README.md                       # Projektbeschreibung
└── requirements.dev.txt            # pytest, flake8, black
```

`main` ist der stabile, gesperrte Hauptzweig – da wird nicht direkt draufgeschrieben. Jede Aufgabe bekommt einen eigenen Branch.

---

## 3. Workflow – GitHub Flow

Kurzfassung, ausführlich in [CONTRIBUTING.md](https://github.com/Moewe-WHV/iSlave/blob/main/CONTRIBUTING.md):

1. **Branch pro Aufgabe anlegen**, benannt nach Muster:
   - `feature: #<Issue-Nr>-kurzbeschreibung` → etwas Neues
   - `fix: #<Issue-Nr>-kurzbeschreibung` → Bugfix
   - `docs: #<Issue-Nr>-kurzbeschreibung` → nur Text/Doku
   - `chore: #<Issue-Nr>-kurzbeschreibung` → Hintergrund-Änderungen (Config etc.)
   - Beispiel: `feature: #7-datenmodell-roboter`
2. **Klein und zügig arbeiten** – Aufgaben in 1–2 Tagen abschließbar halten.
3. **Regelmäßig aktuellen Stand holen:**
   ```bash
   git fetch origin
   git merge origin/main
   ```
4. **Pull Request gegen `main` stellen**, wenn fertig:
   - Vorlage ausfüllen, Issue verlinken (z. B. `Closes #7`)
   - Mindestens 1 Teammitglied muss reviewen und freigeben
   - CI-Checks müssen grün sein
5. **Aufräumen** – Branch wird nach dem Merge gelöscht.

### Commit-Nachrichten
Kurz, als Aussage was gemacht wurde (nicht wie):
- ✅ `Datenmodell Roboter implementiert`
- ❌ `Hab mal kurz was probiert`

### Coding-Standards
Vor jedem Push:
```bash
black src tests    # Code-Formatierung
flake8 src tests   # Lint-Check
pytest              # Tests
```

---

## 4. Sprint-Rhythmus

- Ein Sprint = **1 Woche** (Montag–Freitag)
- **Freitags:** gemeinsames Review, was fertig geworden ist
- Kein eigener Git-Branch pro Sprint – das ist rein organisatorisch (Board/Kopf)


## 5. Tools & Frameworks
- Visual Studio Code 
- GitHub
- Pytest
- Tkinter 


---

## 6. Erste Schritte – Checkliste

- [ ] Repo geklont, Setup durchgeführt, `pytest` läuft grün
- [ ] [CONTRIBUTING.md](https://github.com/Moewe-WHV/iSlave/blob/main/CONTRIBUTING.md) komplett gelesen
- [ ] Zugriff auf [Issues](https://github.com/Moewe-WHV/iSlave/issues) und [Projects-Board](https://github.com/Moewe-WHV/iSlave/projects) geprüft
- [ ] Erste Aufgabe/Issue mit Tim oder Jendrik abgestimmt
- [ ] Ersten Branch nach Namensschema angelegt
- [ ] `black` / `flake8` / `pytest` lokal einmal durchlaufen lassen, bevor gepusht wird

## Links

- Repo: https://github.com/Moewe-WHV/iSlave
- Contributing-Regeln: https://github.com/Moewe-WHV/iSlave/blob/main/CONTRIBUTING.md
- Issues: https://github.com/Moewe-WHV/iSlave/issues
- Projects-Board: https://github.com/Moewe-WHV/iSlave/projects
