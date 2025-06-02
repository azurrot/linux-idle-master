import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This script launches Firefox (optionally headless) using a specific profile to access Steam.
# It tries to extract the 'sessionid' and 'steamLoginSecure' cookies required for authentication.
# If cookies are not initially available, it attempts to click the "Login" button and retry.
# As a fallback, it switches to a visible browser window for manual login if needed.
# Once valid cookies are obtained, they are saved to a settings.txt file for later use.



FIREFOX_BINARY = "/path/to/firefox/firefox"
GECKODRIVER_PATH = "/usr/local/bin/geckodriver"
PROFILE_PATH = "/home/xxxx/.mozilla/firefox/p0cqet3q.default"
OUTPUT_FILE = "/path/to/linux-steam-idle/settings.txt"


def build_driver(headless=True):
    options = Options()
    options.binary_location = FIREFOX_BINARY
    if headless:
        options.add_argument("--headless")
    options.add_argument("-profile")
    options.add_argument(PROFILE_PATH)
    service = Service(executable_path=GECKODRIVER_PATH)
    return webdriver.Firefox(service=service, options=options)

def extract_relevant_cookies(driver):
    settings = {"sessionid": "", "steamLoginSecure": "", "steamparental": "", "sort": ""}
    for cookie in driver.get_cookies():
        if cookie['name'] in settings:
            settings[cookie['name']] = cookie['value']
    return settings

def click_login_button(driver):
    try:
        print("🖱️ Suche Anmelden-Link...")
        login_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='global_action_link' and contains(text(), 'Anmelden')]"))
        )
        print("🖱️ Klicke auf 'Anmelden'...")
        login_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("login"))
        time.sleep(15)
    except Exception as e:
        print("⚠️ Fehler beim Klick auf 'Anmelden':", e)


def write_settings_to_file(settings, output_file):
    with open(output_file, "w") as f:
        for key, value in settings.items():
            f.write(f'{key} = "{value}"\n')
    print(f"💾 Cookies gespeichert in: {output_file}")

def get_steam_cookies():
    print("🕶️ Starte Headless...")
    driver = build_driver(headless=True)
    driver.get("https://steamcommunity.com/")
    time.sleep(5)
    cookies = extract_relevant_cookies(driver)

    if cookies["sessionid"] and cookies["steamLoginSecure"]:
        print("✅ Cookies im Headless-Modus gefunden.")
        driver.quit()
        return cookies

    click_login_button(driver)
    cookies = extract_relevant_cookies(driver)
    driver.quit()

    if cookies["sessionid"] and cookies["steamLoginSecure"]:
        print("✅ Cookies nach Headless-Login gefunden.")
        return cookies

    print("🔄 Immer noch keine Cookies – wechsle zu sichtbarem Modus.")
    driver = build_driver(headless=False)
    driver.get("https://steamcommunity.com/")
    time.sleep(10)
    cookies = extract_relevant_cookies(driver)
    driver.quit()

    if cookies["sessionid"] and cookies["steamLoginSecure"]:
        print("✅ Cookies im sichtbaren Modus gefunden.")
    else:
        print("❌ Auch sichtbar keine Cookies – evtl. Login fehlgeschlagen.")

    return cookies

if __name__ == "__main__":
    cookies = get_steam_cookies()
    if cookies["sessionid"] and cookies["steamLoginSecure"]:
        write_settings_to_file(cookies, OUTPUT_FILE)
    else:
        print("⚠️ Cookies nicht gespeichert – Login unvollständig.")

