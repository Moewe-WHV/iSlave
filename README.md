# iSlave
Terminalanwendung (Python) zur Steuerung eines humanoiden Haushaltsroboters.  
Klassenprojekt - IBB FIAE Winter A1 – 8 Wochen, 6 Sprints.



## 🪟 Setup Windows 
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```
## 🍎 Setup Mac 
```bash
python -m venv .venv
source .venv/bin/activate      
pip install -r requirements-dev.txt
```

## 🧐 Tests 
```bash
pytest
```

## 📁 Projektstruktur 
```
iSlave/
├── docs/
│   ├── burndown_charts/            # Sprint Burndown Charts
|   ├── mockups/                    # Desgignvorlagen
│   ├── diagrams/                   # Alle Arten von Diagrammen 
│   ├── protocols/                  # Sitzungsprotokolle & Daylies
│   └── iSlave_Onboarding.md        # Onboarding-File          
├── src/     
|   ├── frontend/                   # Alle Arten von Diagrammen                        # Hier liegt der Code  
│   └── main.py
├── tests/                          # Test-Skripte
│   └── test_placeholder.py
├── .gitignore                      # Was soll beim push ignoriert werden
├── CONTRIBUTING.md                 # GitHub Projekt-Knigge
├── README.md                       # Projektbeschreibung
└── requirements.dev.txt            # pytest, flake8, black
```

Branching-Strategie und Contribution-Regeln: siehe [CONTRIBUTING.md](CONTRIBUTING.md).  
Bei Fragen: Tim

## 👥 Team (Sprint 1, 2, 3) 

| Rolle           | Person    |
|---              |---        |
| Product Owner   | Jendrik                                                               |
| Scrum Master    | Henning                                                               |
| Teamleiter      | Tim                                                                   |
| Entwicklerteam  | Sascha, Benjamin, Phillipp, Niklas, Jesse, Radu, Cicero, Amer, Süheyl |
