class Trigger:
    """
    Eine einzelne Trigger-Kachel.
    Speichert nur den Text, der später in der Textbox stehen soll.
    Später (Schritt 3) könnte man hier noch mehr Infos reinpacken,
    z.B. ein Bild oder eine Farbe für die Box.
    """

    def __init__(self, text):
        # Der Text, der angezeigt wird, wenn der Spieler diese Kachel betritt
        self.text = text


class TriggerManager:
    """
    Verwaltet ALLE Trigger einer Karte an einem Ort.
    Prüft jeden Frame, ob der Spieler gerade auf einer Trigger-Kachel steht.

    Prinzip ist das gleiche wie bei 'kollision' neben 'karte':
    Eine eigene, unabhängige Datenstruktur neben der Tilemap,
    die nichts mit dem Aussehen der Karte zu tun hat.
    """

    def __init__(self):
        # Dictionary: Schlüssel ist eine Koordinate (x, y) als Tupel,
        # Wert ist das dazugehörige Trigger-Objekt.
        # Beispiel nach dem Registrieren: {(3, 4): Trigger("Hallo!")}
        self.trigger = {}

        # Hier merkt sich der Manager, welcher Trigger GERADE aktiv ist
        # (also: worauf steht der Spieler aktuell). None = kein Trigger aktiv.
        # Das ist der Wert, den wir später zum Zeichnen der Textbox benutzen.
        self.aktiver_trigger = None

        # Merkt sich die Kachel-Position vom letzten Frame.
        # Wird gebraucht, um zu erkennen, ob der Spieler sich überhaupt
        # bewegt hat, seit wir das letzte Mal geprüft haben.
        self._letzte_position = None

        #True nur in dem einem Frame, wo die Kachel betreten wird, damit sich der Trigger nicht bei jedem Frameneu startet
        self.trigger_neu_ausgeloest = False

    def registriere(self, x, y, text):
        """
        Legt einen neuen Trigger auf der Kachel (x, y) an.
        Wird einmalig beim Programmstart aufgerufen (in main.py),
        ähnlich wie ihr 'karte' und 'kollision' am Anfang definiert.
        """
        # (x, y) wird als Tupel zum Schlüssel im Dictionary gemacht
        self.trigger[(x, y)] = Trigger(text)

    def aktualisiere(self, spieler_x, spieler_y):
        """
        Muss JEDEN Frame aufgerufen werden (so wie aktualisiere_bewegung()
        beim Spieler/NPC auch). Prüft, ob der Spieler auf einem Trigger-Feld steht.
        """
        # Aktuelle Position des Spielers als Tupel zusammenfassen,
        # damit wir sie direkt als Dictionary-Schlüssel benutzen können
        position = (spieler_x, spieler_y)

        # Wenn sich die Kachel-Position seit dem letzten Frame NICHT geändert hat,
        # brauchen wir gar nichts neu zu prüfen -> Funktion vorzeitig verlassen.
        # Das verhindert, dass wir denselben Trigger jeden Frame neu "auslösen",
        # solange der Spieler einfach nur stehen bleibt.
        if position == self._letzte_position:
            self.trigger_neu_ausgeloest = False
            return

        # Aktuelle Position für den nächsten Frame-Vergleich speichern
        self._letzte_position = position

        neuer_trigger = self.trigger.get(position)

        #Nur True, wenn jetzt ein trigger aktiv ist, der vorher nicht aktiv war
        self.trigger_neu_ausgeloest = neuer_trigger is not None and neuer_trigger is not self.aktiver_trigger

        # dictionary.get(schluessel) gibt den Wert zurück, WENN der Schlüssel
        # existiert - existiert er nicht, gibt es automatisch None zurück,
        # ohne dass wir vorher mit "if position in self.trigger" prüfen müssen.
        self.aktiver_trigger = self.trigger.get(position)