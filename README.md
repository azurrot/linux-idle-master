# General description
These scripts were developed to automate the extraction of Steam login cookies (sessionid and steamLoginSecure) using Firefox and Selenium. Since Steam requires authenticated sessions for certain operations, the cookies are necessary for tools like linux-steam-idle to function properly.

However, due to limitations in how Firefox handles profiles—especially when using Snap packages or running scripts outside a full desktop session—it was necessary to simulate a proper graphical environment. This includes exporting display-related environment variables and supporting Wayland/X11 sessions.

# Overview of the scripts:
update_cookies.py: A Python script that launches Firefox (headless or visible), checks if the user is logged in, and extracts the necessary cookies. If the user is not logged in, it automatically clicks the "Login" button and retries. If still unsuccessful, it re-launches Firefox in visible mode for manual login.

run_cookies.sh: A shell script that sets up the required GUI environment variables (DISPLAY, XAUTHORITY, DBUS_SESSION_BUS_ADDRESS, etc.) and then runs update_cookies.py. This allows the script to behave like it would when launched from a graphical environment such as PyCharm.

restart_instance.sh: A helper script to ensure that only one instance of the main tool (e.g. start.py) runs at a time. It kills any previous instance and starts the new one within the correct virtual environment.

# Required path adjustments:
The user must manually update the following paths in the scripts:

FIREFOX_BINARY – the full path to your Firefox binary (e.g. /home/user/firefox/firefox)

GECKODRIVER_PATH – path to your geckodriver binary (e.g. /usr/local/bin/geckodriver)

PROFILE_PATH – the path to your Firefox profile folder (e.g. /home/user/.mozilla/firefox/xyz.default-release)

OUTPUT_FILE – the destination path where the cookie settings should be saved (e.g. /home/user/linux-steam-idle/settings.txt)

VENV_PATH – path to your Python virtual environment (e.g. /home/user/venv)

SCRIPT_PATH – path to the Python script you want to launch (e.g. start.py)

GUI-related variables in run_cookies.sh (XAUTHORITY, DISPLAY, etc.) may also need to be updated depending on your desktop session

# CRONTAB:
Make sure both scripts (run_cookies.sh and run_script.sh) have execute permissions (chmod +x script.sh).

To edit the crontab for your current user, use:
crontab -e

Runs the cookie update script every hour at a specific minute
21 * * * * bash /path/to/run_cookies.sh >> /path/to/run_cookies.log 2>&1

Runs the main script every 6 hours, at the start of the hour
0 */6 * * * /path/to/run_script.sh >> /path/to/run_script.log 2>&1
