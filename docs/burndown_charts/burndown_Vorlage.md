```mermaid
---
config:
  themeVariables:
    xyChart:
      plotColorPalette: "#1500ff, #c21307, #00a300"
---
xychart-beta
    title "Sprint <N> Burndown"
    x-axis ["Start", "<Tag 1>", "<Tag 2>", "<Tag 3>", "<Tag 4>", "<Tag 5>"]
    y-axis "Restaufwand in Stunden" 0 --> <Max>
    line "SOLL"  [<Startwert>, ..., 0]
    line "IST"   [<Startwert>, ...]
    line "IDEAL" [<Startwert>, ..., 0]
```
 <span style="color:#0000ff">■</span> SOLL &nbsp;&nbsp; <span style="color:#ff0000">■</span> IST &nbsp;&nbsp; <span style="color:#00a300">■</span> IDEAL

<!--
Farben (plotColorPalette, Reihenfolge = Reihenfolge der line-Einträge):
  SOLL  = #1500ff (blau)
  IST   = #c21307 (rot)
  IDEAL = #00a300 (grün)
Datenpunkte: 1 Startwert + 1 Wert pro Sprinttag. Alle line-Arrays gleich lang;
für noch nicht erreichte Tage bei IST den Wert weglassen (Linie endet dort).
-->

## Kapazität
Eingeplante Issues: **<Anzahl>** mit insgesamt **<Summe> h** geschätztem Aufwand *(ursprünglich <X> h im Planning Poker)*
- <Issue A>: <h> h
- <Issue B>: <h> h
- <Issue C>: <h> h  *(am <TT.MM.> von <alt> h hochgesetzt)*

**Linien:**
- **IDEAL** – gleichmäßige lineare Abnahme von <Summe> h auf 0 über die <Anzahl> Sprinttage (Referenz), ~<h/Tag> h/Tag.
- **SOLL** – geplanter Restaufwand nach Schätzung. Bei Scope-Änderung im Sprint: bis zum Änderungstag alter Plan, am Änderungstag Sprung um ±<Δ> h, danach linear auf 0 bis zum Sprintende.
- **IST** – tatsächlicher Restaufwand (siehe unten).

---

## Geleistete Stunden (IST)
Berechnung IST-Linie: Restaufwand = <Summe> h − kumulierte geleistete Stunden (auf 0 begrenzt).

| Tag          | <Tag 1> | <Tag 2> | <Tag 3> | <Tag 4> | <Tag 5> | Summe |
|---           |---      |---      |---      |---      |---      |---    |
| Stunden/Tag  |         |         |         |         |         |       |
| kumuliert    |         |         |         |         |         |       |
| Restaufwand  |         |         |         |         |         |       |

> Nur Story-bezogene Stunden eintragen (siehe Zeiterfassung unten). Meetings, allgemeines Lernen und Setup zählen **nicht** in diese Tabelle.

---

## Zeiterfassung – was wird getrackt?

Jede gebuchte Stunde braucht eine **Issue-Nummer**. Keine losen „x h investiert".


### Regeln

1. Jede Buchung mit Issue-Nummer.
2. Template / Setup vorab als eigenes Issue anlegen und schätzen.
3. Meetings separat tracken, nie in die Story-Stunden.
4. Im Daily abfragen: **welches Issue, wie viel Rest-h noch** – nicht „was hab ich gemacht".

---

## Annahmen / offene Punkte
- Gesamtschätzung **<Summe> h** = <Issue A> (<h> h) + <Issue B> (<h> h) + <Issue C> (<h> h). Ursprüngliche Planning-Poker-Summe: <X> h.
- IDEAL-Linie linear über **<Anzahl> Arbeitstage** (<TT.MM.> – <TT.MM.>, Wochenende ausgenommen), ~<h/Tag> h/Tag.
- SOLL-Linie: <Beschreibung des Plans / etwaiger Scope-Änderung>.
- IST wird gegen die aktuelle Schätzung (<Summe> h) gerechnet.
- IST-Werte sind Team-Tagessummen aus der obigen Tabelle.
- <weitere Annahme, z. B. vorläufige Zahlen, fehlende Erfassungen>
