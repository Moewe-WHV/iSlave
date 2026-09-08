# iSlave Desktop MVP

Eigenständige Haushaltsroboter-Simulation. Alle ursprünglichen Projektdateien bleiben unverändert. Die Raumpläne orientieren sich an den vorhandenen Mockups; die isolierte Anwendung übernimmt keine importseitig startenden Fenster aus den Prototypen.

## Start

Windows: `mvp/start.bat` doppelklicken. Alternativ im Repository-Ordner:

```powershell
python -m mvp
```

Voraussetzung: Python 3.10 oder neuer mit Tkinter/Tcl-Tk. Die Anwendung benötigt keine zusätzlichen Python-Pakete. Der Starter verwendet zuerst die vorhandene `.venv`, anschließend `py -3` oder `python`.

## Vorführung

1. Namen links eingeben und **Anlegen / Laden** wählen.
2. Wohnzimmer wählen, **Saugen** starten. Der Roboter fährt zusammenhängende Wege um Möbel herum; bearbeitete Flächen erscheinen mintfarben.
3. Nach Abschluss **Wischen** starten. Akku und Spülmittel werden verbraucht.
4. Küche auswählen und **Spülen** starten. Spülen ist eine stationäre, zeitlich simulierte Aufgabe.
5. **Akku laden**, **Spülmittel nachfüllen** und **Wartung durchführen** ausprobieren. Diese Serviceaktionen werden sofort simuliert.
6. Fenster schließen und erneut starten; das Profil über seinen Namen laden. Raum, Akku, Material, Ladezyklen, Wartung und abgeschlossene Aufträge bleiben erhalten.

## Regeln und Grenzen

- Saugen verbraucht 15 % Akku, Wischen 20 % und eine Materialeinheit, Spülen 10 % und eine Materialeinheit. Aufträge starten ab 20 % Akku, bei gültiger Wartung und ausreichendem Material.
- Wischen und Saugen sind in jedem Raum möglich, Spülen ausschließlich in der Küche.
- Wartung wird nach zwei Jahren fällig. Der 29. Februar wird bei Bedarf auf den 28. Februar abgebildet. Eine fällige Wartung sperrt neue Aufträge.
- Ein voller nachgeladener Akku entspricht einem äquivalenten Ladezyklus; Teilaufladungen zählen anteilig.
- Stoppen erhält den bisherigen Akkuverbrauch. Material wird bei Auftragsbeginn verbraucht. Abgebrochene Aufträge gelten nicht als abgeschlossen.
- **Neue Runde** setzt erledigte Aufträge zurück, erhält aber Akku, Material und Wartung.
- Raumwechsel werden sofort simuliert. Innerhalb eines Raums fährt der Roboter bei Saugen/Wischen einen vollständigen Rasterweg. Keine physische Roboteranbindung.
- Profile werden automatisch bei Zustandswechseln, Abschluss und Schließen in `mvp/data/profiles.json` gespeichert. Dieser Ordner ist vom Git-Tracking ausgeschlossen. Laufende Routen und Zwischenpositionen werden nicht wieder aufgenommen. Bei abruptem Prozessabbruch kann Fortschritt seit der letzten Speicherung verloren gehen.
- Defekte Profildateien werden gemeldet und nicht überschrieben. Vor manueller Reparatur eine Sicherung der Datei erstellen.
- Die aktuelle Version ist für einen gleichzeitig laufenden Prozess ausgelegt. Kein Passwortsystem, keine Cloud, keine Spielmechaniken.

## Aufbau und Tests

- `core.py`: Raumdaten, Roboterzustand, Auftragsprüfung, Wegplanung und JSON-Speicherung.
- `app.py`: eine Tkinter-Oberfläche und eine Ereignisschleife; Animation über `after()`.
- `__main__.py`: Einstiegspunkt.

```powershell
.venv\Scripts\python.exe -m pytest tests mvp/tests
.venv\Scripts\python.exe -m black --check mvp
.venv\Scripts\python.exe -m flake8 mvp
```

Die UI-Tests öffnen kurz ein zurückgezogenes Tk-Fenster und prüfen reale Widgets und Ereignisse. Auf Systemen ohne verfügbares Display werden ausschließlich diese Tests übersprungen.
