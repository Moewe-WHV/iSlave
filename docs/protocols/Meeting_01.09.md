# Meeting 01.09.2026 – Start 08:00 Uhr - Ende 09:35 Uhr

**Art:** Daily / Planning / Review
**Ort:** Online
**Teilnehmer:** Radu, Jesse, Philipp, Benjamin, Jendrik, Süheyl, Niklas, Holger, Sascha, Cicero (kam verspätet)
**Abwesend:** Tim (entschuldigte sich wegen Bombenräumung), Henning (krank), Amer (fehlt aus unbekannten Gründen)
**Schriftführer:** Benjamin

---

## 1️⃣ Themen / Besprochen

- **Sprint Review**
  - Radu stellte den Sprint der letzten Woche vor:
    - Roboterklasse definiert, Schnittstellen definiert, Räume vorgestellt, Klassen und Module vorgestellt.
    - Aktivitätsdiagramm gezeigt.
    - Akzeptanzkriterien alle abgedeckt.
    - Testfälle vorgeführt.
  - Süheyl stellte den Sprint der letzten Woche vor:
    - Sprach die Probleme mit Freiheiten durch Product Owner an.
    - Umstellung auf TKinter.
    - Räume in 2D fertigstellen.
  - Sascha stellte den Sprint der letzten Woche nicht vor, da er den Code nicht vorliegen hatte. Ihm war auch nicht bewusst, dass dies im heutigen Meeting nochmal behandelt wird.

- **Planning Poker**
  - **Interaktion 1:**
    - Runde 1 (5: Philipp; 8: Cicero, Jesse, Radu, Sascha; 13: Benjamin, Niklas, Süheyl):
      - Philipp findet, dass es schneller geht, da man sich im Team eingearbeitet hat und man schon teils Klassen hat.
      - Niklas empfindet es nicht als so einfach und befürchtet Probleme bei der Vernetzung.
      - Süheyl fürchtet, dass die Feinjustierung Probleme und bei der Anbindung an die grafische Oberfläche geben wird.
      - Benjamin sieht es komplexer an als die anderen Sprints und kann somit nicht bei einer Bewertung von 8 bleiben.
    - Runde 2 (8: Cicero, Jesse, Philipp, Süheyl; 13: Benjamin, Niklas, Radu, Sascha):
      - Holger erklärte, auf Nachfrage von Süheyl, nochmal die Grundlagen vom Planning Poker und der Fibonacci-Folge.
      - Jesse gab zu bedenken, dass 13 Stunden bei einem 3-köpfigen Team schon sehr viel sei.
        - Benjamin erwähnte daraufhin, dass die Zeit für das gesamte Team ist, nicht für jeden Teilnehmer einzeln.
      - Süheyl fragte, ob der Code für Akku schon fertig ist.
        - Holger erklärte daraufhin, dass der Code als fertig gemeldet wurde. Des Weiteren gab er zu bedenken, dass eigentlich ab dem zweiten Sprint alle alten Testfälle nochmals durchlaufen lassen müssten. Hierfür hat er einen automatisierten Testablauf empfohlen.
    - Runde 3 (8: Cicero; 13: Rest):
      - Es wurde sich auf 13 Stunden geeinigt.

  - **Nutzerverwaltung**
    - Philipp hinterfragte nochmals, warum in der Userstory noch immer "Spieler" steht:
      - Süheyl gab an, dass man sich gemeinsam auf eine Simulation geeinigt hat.
      - Jendrik passt die Userstory entsprechend an.
      - Holger merkte an, die Vision noch entsprechend anzupassen.
    - Runde 1 (8: Benjamin, Cicero, Jesse, Radu, Sascha, Süheyl; 13: Niklas, Philipp):
      - Jendrik hat das Abspeichern der Spielstände aus der Userstory genommen.
      - Süheyl gab an, dass man ja Code aus den anderen Sprints übernehmen kann.
      - Philipp merkte an, dass hierfür Datenbanken angelegt werden müssen.
      - Sascha erklärte, dass in dem vergangenen Sprint bereits JSON verwendet wurde, welches hierfür auch wieder verwendet werden soll.
      - Niklas fehlte das Verständnis über die genaue Definition der Userstory.
      - Jendrik hinterfragte, ob die Simulation nur aus einem Durchgang bestehen soll.
      - Philipp hinterfragte, ob JSON nicht zu simpel sei.
        - Holger erklärte, dass JSON hierfür vollkommen ausreicht.
      - Jendrik hinterfragte, warum man überhaupt speichern soll, wenn es nur einen Charakter geben soll.
        - Süheyl erklärte nochmals seine Ansicht der Simulation.
        - Philipp erklärte nochmal die ursprüngliche Idee für das Projekt in Anlehnung an einen Saugroboter.
        - Niklas erwähnte nochmals, dass dies bereits mehrfach besprochen wurde. Er bat darum, die Userstorys entsprechend zu überarbeiten. Ebenso hinterfragte er, ob eine Nutzerverwaltung überhaupt noch sinnhaftig sei.
        - Benjamin hinterfragte, welche Punkte in der Userstory aufgenommen werden sollen.
        - Holger betonte nochmals, dass Gaming-Begriffe rausgelassen werden sollen.
        - Jendrik hinterfragte, wofür man dann überhaupt noch einen Nutzernamen bräuchte, wenn es eh nur einen geben soll.
          - Benjamin merkte an, dass es am Anfang einfacher ist, einen Nutzernamen mit einzubauen. Schwieriger wird es, ihn am Ende hinzuzufügen, falls die Anwendung doch auf mehrere Benutzer erweitert werden soll.
        - Folgende Punkte sollen aufgenommen werden:
          - Nutzernamen anlegen.
          - Speicherung des Raumes, in dem sich der Roboter befindet.
          - Akkustand, Spülmittel und Wartungszeiten sollen gespeichert werden.
    - Runde 2: Alle Teilnehmer haben mit 8 Stunden abgestimmt.

  - **Umgebung 1**
    - Philipp fragte, ob jetzt der komplette Code neu geschrieben werden muss, wegen der Umstellung auf TKinter.
      - Jesse sagte, er kann komplett von vorne anfangen.
    - Sascha hat darum gebeten, noch einmal komplett abgeholt zu werden, wie es zu der Umstellung auf TKinter kam.
    - Benjamin hat hinterfragt, ob der Code komplett anhand des Sprints neu aufgebaut werden soll.
      - Jesse hat dies bestätigt.
    - Runde 1 (8: Cicero, Jesse, Niklas, Radu, Süheyl; 13: Benjamin, Sascha; 20: Philipp):
      - Philipp gab zu bedenken, dass sich Jesse und Süheyl ja erstmal in Tkinter einlesen müssen.
        - Süheyl gab an, dass er dies mit seinen 8 Stunden berücksichtigt hat.
      - Philipp gab zu bedenken, dass es sich um einen sehr großen Arbeitsaufwand handelt, den Code nochmal auf TKinter umzubauen. Er sagte, dass für 8 Stunden mindestens 80% des alten Codes recycelt werden müsste.
        - Jesse gab an, dass der große Arbeitsaufwand in den ersten Sprints daher rührte, dass er sowohl Backend als auch Frontend programmiert hatte. Er vermutete, dass Süheyl den Arbeitsaufwand unterschätzt, da er glaubt, dass Süheyl den Code noch nicht richtig kennt. Er merkte an, eigentlich zu viel gemacht zu haben.
        - Holger regte an, sich auf 8 Stunden zu einigen und am Donnerstag nochmal eine Einschätzung zu machen. Der genaue Zeitpunkt muss aber noch geklärt werden. Hier sollen Jesse und Süheyl nochmal eine Rückmeldung an den Projektleiter geben.
          - Jesse gab an, dies am Mittwoch zu machen.
          - Es wurde sich auf Donnerstag 8 Uhr geeinigt.
          - Holger sagte, dass sich die Teilnehmer melden sollten, sobald etwas dazwischen kommt, was den Termin gefährdet.
      - Benjamin, Niklas und Sascha änderten ihre Einschätzung nochmal auf 20 Stunden.

- Holger erklärte, wie man ein Sprint Review macht: Weniger Source Code zeigen, lieber mehr Diagramme.
- Holger erklärte, was ein Abnahmeprotokoll ist und was es beinhaltet.
- Holger hinterfragte die Umstellung auf TKinter und erklärte die Beschränkungen. Hier hat er CustomTkinter empfohlen.
- Holger hatte angeregt, vor dem nächsten Meeting eine Agenda rumzuschicken.
- Jendrik sprach die Zeitproblematik bzgl. der LEK in dieser Woche an. Er fragte, ob manche Teilnehmer mehr Sprints machen sollen. Sein Gedanke war, dass man gleichzeitig fertig sein sollte.
  - Holger sprach die Zeitplanung diesbezüglich an. Notfalls kann der Sprint in der jeweiligen Woche nicht abgeschlossen werden.

---

## 2️⃣ Entscheidungen

| # | Entscheidung | Begründung / Alternative | Entschieden von (A) |
|---|---|---|---|
| 1 | Frontend über TKinter | (Bitte nachtragen) | Jendrik |

---

## 3️⃣ Action Items (RACI)

| # |        Aufgabe       |    R    |    A    |   C  |   I  |  Frist |  Status   |
|---|----------------------|---------|---------|------|------|--------|-----------|
| 1 | User Storys anpassen | Jendrik | Jendrik | Team | Team | 01.09. | In Arbeit |
| 2 | GitHub Anpassung     | Tim     | Jendrik | Team | Team | 01.09. | In Arbeit |
| 3 |                      |         |         |      |      |        | Offen     |
| 4 |                      |         |         |      |      |        | Offen     |

> **R** = Responsible | macht die Arbeit (kann mehrere sein)
> **A** = Accountable | trägt die Verantwortung, gibt ab / nimmt ab – **genau eine Person**
> **C** = Consulted   | wird vorher gefragt, liefert Input 
> **I** = Informed    | wird über das Ergebnis informiert 
> 
> *Status: Offen / In Arbeit / Erledigt / Verschoben*

---

## 4️⃣ Offene Punkte / Parkplatz

- (Noch ungeklärt, später aufgreifen)

---

## 5️⃣ Nächstes Meeting

**Wann:** [TT.MM.JJJJ] – [Uhrzeit]  
**Ort / Link:** [z.B. Teams / Discord]  
**Schriftführer:** [Name]  
**Vorzubereiten:** [Wer bringt was mit]
