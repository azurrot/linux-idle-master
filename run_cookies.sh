

# This script activates a Python virtual environment and sets required GUI environment variables
# to simulate a graphical desktop session (as used in PyCharm).
# It then runs the Python script that updates Steam cookies using Firefox and Selenium.
# Venv aktivieren
source /path/to/.venv/bin/activate

# GUI-Umgebungsvariablen wie in PyCharm setzen
# export DISPLAY=:0
# export XAUTHORITY=/run/user/1000/.mutter-Xwaylandauth.6HWV62
# export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
# export WAYLAND_DISPLAY=wayland-0

# Script ausführen
python3 path/to/update_cookies.py
