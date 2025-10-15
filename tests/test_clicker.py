import time
import threading

import pytest


from autoclicker import AutoClicker


class DummyMouse:
    def __init__(self):
        self.clicked = 0

    def click(self, button, count):
        self.clicked += 1


def test_toggle_runs_without_clicking_forever():
    # Use a longer interval so the thread can run a couple iterations in the test
    c = AutoClicker(interval=0.01)
    dummy = DummyMouse()
    c.mouse_controller = dummy

    c.start()
    # toggling on
    c.toggle()
    assert c.running is True

    # allow a few intervals to pass
    time.sleep(0.05)

    # we should have clicked some times
    assert dummy.clicked >= 1

    # toggle off and ensure no more clicks after
    c.toggle()
    clicked_at_toggle_off = dummy.clicked
    assert c.running is False

    time.sleep(0.03)
    # clicked shouldn't increase further after stopping clicking
    assert dummy.clicked == clicked_at_toggle_off

    # clean stop
    c.stop()
