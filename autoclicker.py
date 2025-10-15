"""Simple autoclicker that clicks where the cursor is placed.

Usage:
  - Run: python autoclicker.py
  - Press F6 to toggle auto-clicking on/off.
  - Press ESC to exit the program.

Notes:
  - On macOS you must grant Accessibility permissions to the terminal or Python interpreter
    to allow synthetic mouse events (System Settings -> Privacy & Security -> Accessibility).
"""
import threading
import time
from pynput import mouse, keyboard


class AutoClicker:
    """AutoClicker clicks the current mouse position at a given interval.

    Controls:
      - F6: toggle running
      - ESC: exit
    """

    def __init__(self, interval=0.1):
        self.interval = float(interval)
        self.running = False
        self._thread = None
        self._stop_event = threading.Event()
        self.mouse_controller = mouse.Controller()

    def _click_loop(self):
        while not self._stop_event.wait(self.interval):
            if self.running:
                # click at current position
                self.mouse_controller.click(mouse.Button.left, 1)

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._click_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()

    def toggle(self):
        self.running = not self.running


def main():
    clicker = AutoClicker(interval=0.1)
    clicker.start()

    print("AutoClicker running. Press F6 to toggle clicking, ESC to exit.")

    def on_press(key):
        try:
            if key == keyboard.Key.f6:
                clicker.toggle()
                print("Clicking:", "ON" if clicker.running else "OFF")
            elif key == keyboard.Key.esc:
                # stop everything
                clicker.stop()
                print("Exiting...")
                return False
        except Exception as e:
            print("Key handler error:", e)

    # listen to keyboard events until ESC pressed
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
