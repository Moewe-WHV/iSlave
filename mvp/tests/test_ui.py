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


def test_buttons_drive_full_job_and_profile_reload(app):
    app.profile.set("Testnutzer")
    app.load_button.invoke()
    app.room_buttons["Küche"].invoke()
    app.action_buttons["Spülen"].invoke()
    assert app.sim.busy
    assert str(app.room_buttons["Bad"]["state"]) == "disabled"
    while app.sim.busy:
        app.step()
    assert app.sim.state.completed["Küche"] == ["Spülen"]
    assert app.progress["value"] == 100
    saved = app.store.load("Testnutzer")
    assert saved.detergent == 3
    app.profile.set("Andere Person")
    app.load_button.invoke()
    assert app.sim.state.room == "Wohnzimmer"
    app.profile.set("Testnutzer")
    app.load_button.invoke()
    assert app.sim.state.completed["Küche"] == ["Spülen"]


def test_invalid_command_recovers_and_stop_works(app):
    for text in ("nonsense", "raum Bad", "wischen"):
        app.command.insert(0, text)
        app.submit()
    assert app.sim.state.room == "Bad"
    assert app.sim.busy
    app.step()
    app.stop_button.invoke()
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
            *app.services,
            *app.room_buttons.values(),
            app.profile,
        ]:
            right = widget.winfo_rootx() - app.root.winfo_rootx() + widget.winfo_width()
            bottom = (
                widget.winfo_rooty() - app.root.winfo_rooty() + widget.winfo_height()
            )
            assert right <= app.root.winfo_width(), (str(widget), right)
            assert bottom <= app.root.winfo_height(), (str(widget), bottom)
    app.root.withdraw()
