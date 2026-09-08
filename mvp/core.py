"""Simulation and persistence, independent of the graphical interface."""

from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import date
import json
from pathlib import Path

WIDTH, HEIGHT = 12, 9
ACTIONS = ("Saugen", "Wischen", "Spülen")


@dataclass(frozen=True)
class Room:
    name: str
    accent: str
    furniture: tuple
    entry: tuple = (5, 6)

    @property
    def floor(self):
        blocked = set()
        for _, x, y, w, h in self.furniture:
            blocked.update((xx, yy) for xx in range(x, x + w) for yy in range(y, y + h))
        return {(x, y) for x in range(WIDTH) for y in range(HEIGHT)} - blocked


# Room plans follow the four existing project mockups. No original file is imported
# because those prototypes open independent windows during import.
ROOMS = {
    "Wohnzimmer": Room(
        "Wohnzimmer",
        "#b98159",
        (
            ("Ladestation", 0, 0, 3, 2),
            ("TV", 3, 0, 7, 1),
            ("Sofa", 9, 4, 3, 3),
            ("Sofa", 3, 7, 9, 2),
        ),
    ),
    "Küche": Room(
        "Küche",
        "#efe2ae",
        (
            ("Arbeitsfläche", 0, 0, 3, 7),
            ("Kühlschrank", 0, 7, 3, 2),
            ("Esstisch", 7, 2, 4, 3),
            ("Stuhl", 8, 1, 1, 1),
            ("Stuhl", 10, 1, 1, 1),
            ("Stuhl", 8, 5, 1, 1),
            ("Stuhl", 10, 5, 1, 1),
        ),
    ),
    "Bad": Room(
        "Bad",
        "#91d2e1",
        (
            ("Dusche", 0, 0, 2, 3),
            ("Wanne", 0, 6, 2, 3),
            ("Waschbecken", 2, 0, 2, 1),
            ("Toilette", 6, 0, 2, 1),
            ("Waschmaschine", 8, 0, 2, 2),
            ("Trockner", 10, 0, 2, 2),
        ),
    ),
    "Schlafzimmer": Room(
        "Schlafzimmer",
        "#b98159",
        (
            ("Bett", 3, 0, 6, 5),
            ("Nachttisch", 1, 0, 2, 2),
            ("Nachttisch", 9, 0, 2, 2),
            ("Schrank", 0, 7, 12, 2),
        ),
    ),
}


def next_service(last):
    try:
        return last.replace(year=last.year + 2)
    except ValueError:
        return last.replace(year=last.year + 2, day=28)


@dataclass
class State:
    name: str = "Demo"
    room: str = "Wohnzimmer"
    battery: float = 90.0
    cycles: float = 0.0
    detergent: int = 4
    last_service: str = field(default_factory=lambda: date.today().isoformat())
    completed: dict = field(default_factory=lambda: {name: [] for name in ROOMS})


class Simulation:
    def __init__(self, state=None):
        self.state = state or State()
        self.position = ROOMS[self.state.room].entry
        self.route = deque()
        self.visited = set()
        self.action = None
        self.total = 0
        self.done = 0
        self.cost_per_step = 0

    @property
    def busy(self):
        return self.action is not None

    def switch_room(self, name):
        if self.busy:
            raise ValueError("Bitte zuerst den laufenden Auftrag stoppen.")
        if name not in ROOMS:
            raise ValueError("Diesen Raum gibt es nicht.")
        self.state.room = name
        self.position = ROOMS[name].entry
        self.visited.clear()
        self.done = self.total = 0

    def plan(self):
        """Depth-first coverage walk; every step stays adjacent on accessible floor."""
        floor = ROOMS[self.state.room].floor
        start = self.position
        seen = {start}
        route = [start]
        stack = [(start, iter(self.neighbors(start)))]
        while stack:
            point, choices = stack[-1]
            target = next(choices, None)
            if target is None:
                stack.pop()
                if stack:
                    route.append(stack[-1][0])
            elif target in floor and target not in seen:
                seen.add(target)
                route.append(target)
                stack.append((target, iter(self.neighbors(target))))
        if seen != floor:
            raise ValueError("Der Raum enthält unerreichbare Flächen.")
        return route

    @staticmethod
    def neighbors(point):
        x, y = point
        return ((x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1))

    def start(self, action, today=None):
        if self.busy:
            raise ValueError("Es läuft bereits ein Auftrag.")
        if action not in ACTIONS:
            raise ValueError("Erlaubt sind Saugen, Wischen und Spülen.")
        if next_service(date.fromisoformat(self.state.last_service)) <= (
            today or date.today()
        ):
            raise ValueError("Wartung fällig. Bitte Wartung durchführen.")
        if action == "Spülen" and self.state.room != "Küche":
            raise ValueError("Spülen ist nur in der Küche möglich.")
        cost = {"Saugen": 15, "Wischen": 20, "Spülen": 10}[action]
        if self.state.battery < max(20, cost):
            raise ValueError("Akku zu niedrig. Bitte zuerst laden (mindestens 20 %).")
        if action in ("Wischen", "Spülen") and self.state.detergent < 1:
            raise ValueError("Kein Spülmittel vorhanden. Bitte nachfüllen.")
        if action in self.state.completed[self.state.room]:
            raise ValueError(
                "Dieser Auftrag ist hier schon erledigt. Neue Runde starten."
            )
        route = self.plan() if action != "Spülen" else [self.position] * 30
        self.route = deque(route)
        self.total = len(route)
        self.done = 0
        self.visited.clear()
        self.cost_per_step = cost / self.total
        self.action = action
        if action in ("Wischen", "Spülen"):
            self.state.detergent -= 1

    def tick(self):
        if not self.busy:
            return None
        self.position = self.route.popleft()
        if self.action != "Spülen":
            self.visited.add(self.position)
        self.done += 1
        self.state.battery = max(0, round(self.state.battery - self.cost_per_step, 8))
        if not self.route:
            finished = self.action
            self.state.completed[self.state.room].append(finished)
            self.action = None
            return f"{finished} in {self.state.room} abgeschlossen."
        return None

    def stop(self):
        self.route.clear()
        self.action = None

    def maintenance_action(self, command):
        if self.busy:
            raise ValueError("Bitte zuerst den laufenden Auftrag stoppen.")
        if command == "laden":
            self.state.cycles += (100 - self.state.battery) / 100
            self.state.battery = 100
            return "Akku geladen. Ladezyklen aktualisiert."
        if command == "nachfüllen":
            self.state.detergent = 4
            return "Spülmittel auf 4 Einheiten aufgefüllt."
        if command == "wartung":
            self.state.last_service = date.today().isoformat()
            return "Wartung durchgeführt. Roboter wieder einsatzbereit."
        if command == "neustart":
            self.state.completed = {name: [] for name in ROOMS}
            self.visited.clear()
            self.done = self.total = 0
            return "Neue Reinigungsrunde gestartet."
        raise ValueError("Unbekannter Servicebefehl.")


class Store:
    def __init__(self, path):
        self.path = Path(path)

    @staticmethod
    def validate(data):
        if not isinstance(data, dict):
            raise ValueError("Ungültiges Profil.")
        state = State(**data)
        if (
            not isinstance(state.name, str)
            or not state.name.strip()
            or len(state.name) > 40
        ):
            raise ValueError("Ungültiger Profilname.")
        if state.room not in ROOMS:
            raise ValueError("Ungültiger gespeicherter Raum.")
        for value, maximum in ((state.battery, 100), (state.cycles, 1000000)):
            if type(value) not in (float, int) or not 0 <= value <= maximum:
                raise ValueError("Ungültige Akkuwerte.")
        if type(state.detergent) is not int or not 0 <= state.detergent <= 4:
            raise ValueError("Ungültiger Materialbestand.")
        date.fromisoformat(state.last_service)
        if not isinstance(state.completed, dict) or set(state.completed) != set(ROOMS):
            raise ValueError("Ungültiger Raumzustand.")
        for actions in state.completed.values():
            if not isinstance(actions, list) or any(a not in ACTIONS for a in actions):
                raise ValueError("Ungültige gespeicherte Aufträge.")
        return state

    def read(self):
        if not self.path.exists():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("version") != 1:
                raise ValueError("Unbekanntes Speicherformat.")
            profiles = data["profiles"]
            if not isinstance(profiles, dict):
                raise ValueError("Ungültige Profilliste.")
            for name, raw in profiles.items():
                if self.validate(raw).name != name:
                    raise ValueError("Profilname stimmt nicht überein.")
            return profiles
        except (ValueError, TypeError, KeyError) as exc:
            raise ValueError(
                "Profildatei beschädigt. Sie wird nicht überschrieben."
            ) from exc

    def save(self, state):
        profiles = self.read()
        profiles[state.name] = asdict(self.validate(asdict(state)))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(
                {"version": 1, "profiles": profiles}, ensure_ascii=False, indent=2
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def load(self, name):
        name = name.strip()
        if not name or len(name) > 40:
            raise ValueError("Bitte einen Namen mit 1 bis 40 Zeichen eingeben.")
        profiles = self.read()
        return self.validate(profiles[name]) if name in profiles else State(name=name)
