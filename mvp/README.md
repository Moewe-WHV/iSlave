# iSlave Desktop MVP

Eigenständige Haushaltsroboter-Simulation. Alle ursprünglichen Projektdateien bleiben unverändert. Die Raumpläne orientieren sich an den vorhandenen Mockups; die isolierte Anwendung übernimmt keine importseitig startenden Fenster aus den Prototypen.

## Pixelgrafik

Die gemeinsame Karte verwendet eigene Pixelgrafiken im Stil klassischer Top-View-Rollenspiele: Holzböden, Fliesen, Wände, Fenster, Türen, Möbel und ein Roboter-Sprite. Es werden keine Pokémon-Assets verwendet. Die Darstellung liegt in `pixel_view.py`, benötigt keine zusätzlichen Pakete und übernimmt Raumgeometrie und Roboterzustand aus der bestehenden Simulation. Flure und Türen stellen die Verbindung grafisch dar; Raumwechsel werden weiterhin sofort simuliert.

Diese Überarbeitung betrifft ausschließlich die Grafik. Die zuvor festgestellten Abweichungen von den GitHub-User-Stories (unter anderem Nutzerpflicht, geführter Dialog, Aktionsverbrauch, Equipment, Highscore und ausschließlich externe Terminaleingabe) werden dadurch noch nicht behoben.

## Start

Windows: `mvp/start.bat` doppelklicken. Alternativ im Repository-Ordner:

```powershell
python -m mvp --terminal
```

Voraussetzung: Python 3.10 oder neuer mit Tkinter/Tcl-Tk. Die Anwendung benötigt keine zusätzlichen Python-Pakete. Der Starter verwendet zuerst die vorhandene `.venv`, anschließend `py -3` oder `python`.

## Vorführung

Alle vier Räume bleiben gleichzeitig auf einer Karte sichtbar. Der aktive Raum ist hervorgehoben. Die Steuerung erfolgt vollständig durch Textbefehle – im eingebauten Terminal oder im Konsolenfenster des Starters. Mit Enter abschicken. Ohne `--terminal` wird nur das Kartenfenster mit eingebautem Terminal geöffnet.

1. `nutzer Dein Name` legt ein Profil an oder lädt es. `profile` listet vorhandene Profile.
2. `raum Wohnzimmer`, danach `saugen`. Der Roboter reinigt den Raum sichtbar auf der gemeinsamen Karte.
3. Nach Abschluss `wischen`. Akku und Spülmittel werden verbraucht.
4. `raum Küche`, danach `spülen` für eine stationär simulierte Aufgabe.
5. `laden`, `nachfüllen` oder `wartung` führen die jeweiligen Serviceaktionen aus.
6. `stopp` bricht einen Auftrag ab. `status` zeigt den aktuellen Zustand, `speichern` sichert ihn, `neustart` beginnt eine neue Reinigungsrunde.
7. `hilfe` zeigt Befehle und Verbrauchsregeln. Nach dem nächsten Programmstart das Profil mit `nutzer Dein Name` wieder laden.

Raumnamen und Befehle ignorieren Groß-/Kleinschreibung. Profilnamen dürfen Leerzeichen enthalten. Ungültige Befehle ändern den Zustand nicht. Raum- und Nutzerwechsel werden während eines Auftrags abgelehnt; zuerst `stopp` eingeben. Zum Beenden das Kartenfenster schließen, damit der Zustand gespeichert wird.

## Regeln und Grenzen

- Saugen verbraucht 15 % Akku, Wischen 20 % und eine Materialeinheit, Spülen 10 % und eine Materialeinheit. Aufträge starten ab 20 % Akku, bei gültiger Wartung und ausreichendem Material.
- Wischen und Saugen sind in jedem Raum möglich, Spülen ausschließlich in der Küche.
- Wartung wird nach zwei Jahren fällig. Der 29. Februar wird bei Bedarf auf den 28. Februar abgebildet. Eine fällige Wartung sperrt neue Aufträge.
- Ein voller nachgeladener Akku entspricht einem äquivalenten Ladezyklus; Teilaufladungen zählen anteilig.
- Stoppen erhält den bisherigen Akkuverbrauch. Material wird bei Auftragsbeginn verbraucht. Abgebrochene Aufträge gelten nicht als abgeschlossen.
- `neustart` setzt erledigte Aufträge zurück, erhält aber Akku, Material und Wartung.
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

Die UI-Tests öffnen kurz ein zurückgezogenes Tk-Fenster und prüfen Terminalbefehle, die gemeinsame Karte, reale Widgets und Ereignisse. Auf Systemen ohne verfügbares Display werden ausschließlich diese Tests übersprungen.
