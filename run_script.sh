# This script stops any running instance of the target Python script,
# then activates the specified virtual environment and starts the script.
# It's used to ensure only one instance of the application runs at a time.


# Pfade
VENV_PATH="/path/to/myenv"
SCRIPT_PATH="/path/to/linux-steam-idle/start.py"

# Alte Instanz beenden (falls läuft)
PID=$(pgrep -f "$SCRIPT_PATH")
if [ -n "$PID" ]; then
    echo "Killing old instance with PID $PID"
    kill "$PID"
fi

# Aktivieren des virtuellen Environments und starten des Scripts
source "$VENV_PATH/bin/activate"
python3 "$SCRIPT_PATH"
