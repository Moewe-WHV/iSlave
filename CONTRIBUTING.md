

# 🤝 Wie wir zusammenarbeiten (Contribution-Regeln)

### 🌿 Unsere Strategie: Der „GitHub Flow“

Stell dir unser Projekt wie ein **Baugerüst** vor.

* **`main` (Haupt-Code):** Das ist das fertige Gebäude. Das muss **immer** funktionieren und stabil stehen! Niemand baut hier einfach unangemeldet direkt drauf los (ist extra gesperrt).

---

#### 1. Für jede Aufgabe einen eigenen Arbeitszweig („Branch“) anlegen

Bevor du loslegst, machst du dir eine Kopie des aktuellen Stands. Auf dieser Kopie arbeitest nur du. So geht im Haupt-Code nichts kaputt!

Benenne deinen Zweig nach diesem Muster:

* `feature: #<Issue-Nr>-kurzbeschreibung` ➡️ Du baust etwas **Neues**
* `fix: #<Issue-Nr>-kurzbeschreibung` ➡️ Du reparierst einen **Fehler**
* `docs: #<Issue-Nr>-kurzbeschreibung` ➡️ Du schreibst nur **Texte/Erklärungen**
* `chore: #<Issue-Nr>-kurzbeschreibung` ➡️ Du änderst etwas im **Hintergrund** (z. B. Einstellungen)

> **Beispiel:** `feature: #7-datenmodell-roboter`

---

#### 2. Klein und zügig arbeiten

Baut keine riesigen Riesen-Baustellen, die 3 Wochen offen bleiben!

* Macht eure Aufgaben lieber **klein und überschaubar**.
* So seid ihr in 1–2 Tagen fertig, könnt eure Änderungen schnell abgeben und habt nicht das Risiko, dass der Code nach Wochen völlig veraltet ist.

---

#### 3. Regelmäßig den neuesten Stand abholen

Während du arbeitest, machen deine Teammitglieder ja auch Fortschritte. Damit ihr euch am Ende nicht im Weg steht, holst du dir regelmäßig die neuesten Änderungen der anderen in deinen Arbeitszweig:

```bash
git fetch origin       # „Guck mal nach, was die anderen Neues gemacht haben“
git merge origin/main  # „Hol den neuesten Stand in meinen eigenen Zweig rein“

```

---

#### 4. Fertig? Änderungen einreichen („Pull Request“ / PR)

Wenn dein Code läuft und du fertig bist:

1. Erstelle auf GitHub einen **Pull Request (PR)** gegen den `main`-Zweig. Das bedeutet einfach: *„Hey Team, ich bin fertig. Bitte prüft meinen Code und schiebt ihn ins Hauptprojekt!“*
2. Fülle die Vorlage aus und verlinke deine Aufgabe (z. B. `Closes #7`).
3. **Freigabe abwarten:** Mindestens **1 Teammitglied** muss drüber schauen und grünes Licht geben.
4. **Automatische Tests (CI):** GitHub testet im Hintergrund automatisch, ob dein Code sauber ist und nichts kaputt macht. Der Test-Haken muss **grün** sein!

---

#### 5. Aufräumen

Sobald dein Code im `main` gelandet ist, wird dein Arbeitszweig gelöscht. Weg mit dem Müll! 🧹

---

## 📝 Commit-Nachrichten (Deine Speicherpunkte)

Wenn du deinen Zwischenstand speicherst (`git commit`), schreibst du eine kurze Notiz dazu.

**Regel:** Kurz und knackig, als Befehl oder Aussage, **was** gemacht wurde (nicht *wie*):

* ✅ `Datenmodell Roboter implementiert`
* ✅ `Terminal-Eingabe-Loop fängt leere Eingabe ab`
* ❌ *„Hab mal kurz was am Roboter probiert und dann Kaffee getrunken“*

---

## 🧼 Sauberer Code (Coding-Standards)

Damit der Code nicht aussieht wie ein Kraut-und-Rüben-Salat, nutzen wir automatische Hilfsmittel:

* **PEP 8:** Die offiziellen Regeln, wie Python-Code hübsch aussieht.
* **`black`:** Formatiert deinen Code automatisch schön.
* **`flake8`:** Meckert, wenn du z. B. ungenutzte Variablen rumstehen lässt.
* **`pytest`:** Führt automatische Funktionstests aus.

**Bevor du deine Arbeit hochlädst („pushst“), tippst du das hier im Terminal ein:**

```bash
black src tests   # Macht den Code hübsch
flake8 src tests  # Prüft auf Fehler/Schlampereien
pytest            # Testet, ob noch alles funktioniert

```

---

## ⏱️ Unser Sprint-Rhythmus

* Ein **Sprint** ist ein Arbeitsblock von **1 Woche** (Montag bis Freitag).
* **Freitags:** Wir schauen uns gemeinsam an, was fertig geworden ist (Review).
* Für den Sprint gibt es *keinen* eigenen Arbeitszweig in Git – das ist rein organisatorisch für uns im Kopf und im Board!