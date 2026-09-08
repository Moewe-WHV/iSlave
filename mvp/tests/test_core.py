from dataclasses import asdict
from datetime import date
import json

import pytest

from mvp.core import ROOMS, Simulation, State, Store, next_service


@pytest.mark.parametrize("room", ROOMS)
def test_coverage_stays_on_floor_and_finishes(room):
    sim = Simulation()
    sim.switch_room(room)
    sim.start("Saugen")
    route = list(sim.route)
    assert set(route) == ROOMS[room].floor
    for first, second in zip(route, route[1:]):
        assert abs(first[0] - second[0]) + abs(first[1] - second[1]) == 1
    while sim.busy:
        sim.tick()
    assert sim.state.battery == pytest.approx(75)
    assert sim.state.completed[room] == ["Saugen"]


@pytest.mark.parametrize(
    "state,action",
    [
        (State(battery=19), "Saugen"),
        (State(detergent=0), "Wischen"),
        (State(last_service="2020-01-01"), "Saugen"),
        (State(), "Spülen"),
        (State(), "Unbekannt"),
    ],
)
def test_rejected_job_does_not_mutate(state, action):
    sim = Simulation(state)
    before = asdict(state)
    with pytest.raises(ValueError):
        sim.start(action)
    assert asdict(state) == before
    assert not sim.busy


def test_stop_retains_usage_but_does_not_complete():
    sim = Simulation()
    sim.start("Wischen")
    sim.tick()
    sim.stop()
    assert 89 < sim.state.battery < 90
    assert sim.state.detergent == 3
    assert sim.state.completed[sim.state.room] == []
    assert sim.tick() is None


def test_charge_cycles_and_leap_day():
    sim = Simulation(State(battery=95, cycles=2))
    sim.maintenance_action("laden")
    assert sim.state.cycles == pytest.approx(2.05)
    sim.maintenance_action("laden")
    assert sim.state.cycles == pytest.approx(2.05)
    assert next_service(date(2024, 2, 29)) == date(2026, 2, 28)


def test_maintenance_blocks_on_due_day_and_service_unblocks():
    sim = Simulation(State(last_service="2024-02-29"))
    with pytest.raises(ValueError):
        sim.start("Saugen", today=date(2026, 2, 28))
    sim.maintenance_action("wartung")
    sim.start("Saugen")
    assert sim.busy


def test_active_job_prevents_state_changes():
    sim = Simulation()
    sim.start("Saugen")
    for action in (
        lambda: sim.switch_room("Bad"),
        lambda: sim.start("Wischen"),
        lambda: sim.maintenance_action("laden"),
    ):
        with pytest.raises(ValueError):
            action()


def test_profile_round_trip_and_isolation(tmp_path):
    store = Store(tmp_path / "profiles.json")
    sim = Simulation(store.load("Alice"))
    sim.switch_room("Küche")
    sim.start("Spülen")
    while sim.busy:
        sim.tick()
    store.save(sim.state)
    store.save(store.load("Bob"))
    restored = store.load("Alice")
    assert asdict(restored) == asdict(sim.state)
    assert restored.battery == pytest.approx(80)
    assert restored.detergent == 3
    assert store.load("Bob").completed["Küche"] == []


@pytest.mark.parametrize(
    "content",
    [
        "{bad json",
        "[]",
        '{"version":2}',
        json.dumps({"version": 1, "profiles": {"bad": {"name": "bad", "battery": -1}}}),
    ],
)
def test_corrupt_storage_is_not_overwritten(tmp_path, content):
    path = tmp_path / "profiles.json"
    path.write_text(content, encoding="utf-8")
    store = Store(path)
    with pytest.raises(ValueError):
        store.save(State())
    assert path.read_text(encoding="utf-8") == content


def test_new_round_preserves_resources():
    sim = Simulation()
    sim.start("Saugen")
    while sim.busy:
        sim.tick()
    with pytest.raises(ValueError):
        sim.start("Saugen")
    sim.maintenance_action("neustart")
    assert sim.state.battery == pytest.approx(75)
    assert not any(sim.state.completed.values())
    sim.start("Saugen")
