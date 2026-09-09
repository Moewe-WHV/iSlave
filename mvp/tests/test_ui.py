import tkinter as tk

import pytest

from mvp.app import App
from mvp.core import Store


@pytest.fixture(scope="module")
def root():
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        pytest.skip(f"Tk display unavailable: {exc}")
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def app(tmp_path, root):
    app = App(root, Store(tmp_path / "profiles.json"), auto_tick=False)
    root.update()
    yield app
    if app.timer:
        root.after_cancel(app.timer)
    for child in root.winfo_children():
        child.destroy()


def test_terminal_drives_full_job_and_profile_reload(app):
    for command in ("nutzer Testnutzer", "raum Küche", "spülen"):
        app.command.insert(0, command)
        app.submit()
    assert app.sim.busy
    app.execute("raum Bad")
    assert app.sim.state.room == "Küche"
    while app.sim.busy:
        app.step()
    assert app.sim.state.completed["Küche"] == ["Spülen"]
    assert app.progress["value"] == 100
    saved = app.store.load("Testnutzer")
    assert saved.detergent == 3
    app.execute("nutzer Andere Person")
    assert app.sim.state.room == "Wohnzimmer"
    app.execute("nutzer Testnutzer")
    assert app.sim.state.completed["Küche"] == ["Spülen"]


def test_invalid_command_recovers_and_stop_works(app):
    for text in ("nonsense", "raum Bad", "wischen"):
        app.command.insert(0, text)
        app.submit()
    assert app.sim.state.room == "Bad"
    assert app.sim.busy
    app.step()
    app.execute("stopp")
    assert not app.sim.busy
    assert "Unbekannter Befehl" in app.history.get("1.0", "end")


def test_after_loop_animates_and_remains_responsive(app):
    app.start("Saugen")
    app.schedule()
    app.root.update()
    assert app.sim.done >= 1
    assert app.timer is not None
    app.root.after_cancel(app.timer)
    app.timer = None


def test_window_layout_keeps_controls_inside_window(app):
    app.root.deiconify()
    for geometry in ["1220x840", "980x760"]:
        app.root.geometry(geometry)
        app.root.update()
        app.root.after(100, app.root.quit)
        app.root.mainloop()
        assert app.canvas.winfo_width() >= 380
        assert app.canvas.winfo_height() >= 280
        for widget in [
            app.command,
            app.history,
            app.details,
        ]:
            right = widget.winfo_rootx() - app.root.winfo_rootx() + widget.winfo_width()
            bottom = (
                widget.winfo_rooty() - app.root.winfo_rooty() + widget.winfo_height()
            )
            assert right <= app.root.winfo_width(), (str(widget), right)
            assert bottom <= app.root.winfo_height(), (str(widget), bottom)
    app.root.withdraw()


def test_all_rooms_stay_visible_and_robot_changes_room(app):
    from mvp.core import ROOMS

    for name in ROOMS:
        app.execute("raum " + name)
        labels = app.canvas.find_withtag("room-label")
        assert {app.canvas.itemcget(item, "text") for item in labels} == set(ROOMS)
        robot = app.canvas.find_withtag("robot")
        assert len(robot) == 1
        assert "room:" + name in app.canvas.gettags(robot[0])


def test_external_terminal_queue_uses_same_controller(app):
    app.inbox.put("raum Bad")
    app.inbox.put("saugen")
    app.schedule()
    assert app.sim.state.room == "Bad"
    assert app.sim.busy
    assert app.sim.done == 1
