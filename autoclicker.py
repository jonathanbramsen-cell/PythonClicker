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
import argparse
from pynput import mouse, keyboard
import tkinter as tk
from threading import Thread

try:
    from plyer import notification
    _HAS_PLYER = True
except Exception:
    _HAS_PLYER = False


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
        self._dry_run = False

    def _click_loop(self):
        while not self._stop_event.wait(self.interval):
            if self.running:
                if self._dry_run:
                    print(f"[dry-run] Click at {time.time():.3f}")
                else:
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

    def set_dry_run(self, dry: bool):
        """If dry_run is True, don't perform real clicks — just print simulated clicks."""
        self._dry_run = bool(dry)


def main():
    parser = argparse.ArgumentParser(description="Simple autoclicker")
    parser.add_argument("--interval", "-i", type=float, default=0.1, help="Interval between clicks in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Don't perform real clicks; print actions instead")
    parser.add_argument("--start", action="store_true", help="Start clicking immediately")
    parser.add_argument("--duration", type=float, default=None, help="If provided, stop after this many seconds")
    args = parser.parse_args()

    clicker = AutoClicker(interval=args.interval)
    clicker.set_dry_run(args.dry_run)
    clicker.start()

    print("AutoClicker running. Press F6 to toggle clicking, ESC to exit.")

    if args.start:
        clicker.toggle()
        print("Clicking:", "ON" if clicker.running else "OFF")

    # If a duration was provided, run for that long then exit
    if args.duration is not None:
        end_time = time.time() + float(args.duration)
        try:
            while time.time() < end_time:
                time.sleep(0.1)
        finally:
            clicker.stop()
        return

    # GUI mode: create a small Tkinter window with a toggle button and status
    if args.gui:
        def notify(title, msg):
            if _HAS_PLYER:
                notification.notify(title=title, message=msg)
            else:
                print(f"[notify] {title}: {msg}")

        root = tk.Tk()
        root.title("AutoClicker")

        status_var = tk.StringVar(value="OFF")

        def update_status_label():
            status_var.set("ON" if clicker.running else "OFF")

        def on_toggle():
            clicker.toggle()
            update_status_label()
            notify("AutoClicker", f"Clicking {'ON' if clicker.running else 'OFF'}")

        status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 16))
        status_label.pack(padx=10, pady=10)

        toggle_btn = tk.Button(root, text="Toggle", command=on_toggle)
        toggle_btn.pack(padx=10, pady=5)

        # Run Tkinter in the main thread; but ensure the click loop runs on background thread
        try:
            root.mainloop()
        finally:
            clicker.stop()
        return

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
