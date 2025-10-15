# Python AutoClicker

Simple autoclicker that clicks where your cursor is placed. Uses `pynput` to synthesize mouse events.

Usage
1. Create a virtual environment (recommended).
   python -m venv .venv
   source .venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   python autoclicker.py

Controls
- F6: toggle auto-clicking on/off
- ESC: exit the program

macOS notes
- macOS requires Accessibility permissions for the Terminal or Python interpreter to allow synthetic mouse events.
  Grant this in System Settings -> Privacy & Security -> Accessibility, add your Terminal or Python app.

Safety
- Use with care. This script sends real mouse clicks. Don't run it while important unsaved work is open.
