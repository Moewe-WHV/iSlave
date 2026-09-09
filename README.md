# iSlave
Terminalanwendung (Python) zur Steuerung eines humanoiden Haushaltsroboters.  
Klassenprojekt - IBB FIAE Winter A1 – 8 Wochen, 6 Sprints.


## Setup Windows
```bash
python3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```
## Setup Mac
```bash
python -m venv .venv
source .venv/bin/activate      
pip install -r requirements-dev.txt
```

## Starten
```bash
python src/main.py
```
Mit Kartenansicht. Nur Terminal (z. B. ohne Bildschirm):
```bash
python src/main.py --ohne-gui
```

Ablauf: Nutzer auswählen oder anlegen, danach das Menü. Gesteuert wird
ausschließlich über das Terminal, die Kartenansicht ist reine Anzeige.
Punktestand und Roboterzustand werden beim Beenden im Nutzerprofil
gespeichert (`src/nutzer.json`, `highscores.json` – beide nicht im Repo).

## Tests
```bash
pytest
```

## Projektstruktur
```
iSlave/
├── docs/
│   ├── burndown_charts/            # Sprint Burndown Charts
|   ├── mockups/                    # Desgignvorlagen
│   ├── diagrams/                   # Alle Arten von Diagrammen 
│   ├── protocols/                  # Sitzungsprotokolle & Daylies
│   └── iSlave_Onboarding.md        # Onboarding-File          
├── src/                            # Hier liegt der Code  
|   ├── frontend/                   # Prototypen (Tkinter, Pygame)
│   ├── main.py                     # Einstiegspunkt
│   ├── spiel.py                    # gemeinsamer Spielzustand
│   ├── karte.py                    # Rasterkarte der Wohnung
│   ├── roboter.py                  # Position und Blickrichtung
│   ├── equipment.py                # Spülmittel und Aufsätze
│   ├── gui.py                      # Tkinter-Kartenansicht
│   ├── akku.py                     # Akkustand und Ladezyklen
│   ├── aktionen.py                 # Saugen, Wischen, Spülen
│   ├── raeume.py                   # Raumsteuerung
│   ├── interaktion.py              # Terminalmenü und Dialoge
│   ├── wartung.py                  # Wartungsintervall
│   ├── highscore.py                # Sauberkeitspunkte
│   └── nutzerverwaltung.py         # Nutzer und Profile
├── tests/                          # Test-Skripte, ein Modul je Datei
├── .gitignore                      # Was soll beim push ignoriert werden
├── CONTRIBUTING.md                 # GitHub Projekt-Knigge
├── pyproject.toml                  # black-Konfiguration
├── pytest.ini                      # pytest-Konfiguration
├── README.md                       # Projektbeschreibung
└── requirements-dev.txt            # pytest, flake8, black
```

Branching-Strategie und Contribution-Regeln: siehe [CONTRIBUTING.md](CONTRIBUTING.md).  
Bei Fragen: Tim

## Team (Sprint 1 - 3)

| Rolle           | Person    |
|---              |---        |
| Product Owner   | Jendrik                                                               |
| Scrum Master    | Henning                                                               |
| Teamleiter      | Tim                                                                   |
| Entwicklerteam  | Sascha, Benjamin, Phillipp, Niklas, Jesse, Radu, Cicero, Amer, Süheyl |
