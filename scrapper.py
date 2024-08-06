
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import pandas as pd

# Set the path to the chromedriver executable
CHROMEDRIVER_PATH = r'C:\Users\USER\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Set the path to the Chrome executable
CHROME_BINARY_PATH = r'C:\Users\USER\Downloads\chrome-win64\chrome-win64\chrome.exe'

# Set the download directory
DOWNLOAD_DIR = r'C:\Users\USER\Downloads\scrapper'
TRIAL_EXCEL_FILE = os.path.join(DOWNLOAD_DIR, 'trial1.xlsx')

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Initialize the Chrome driver with download preferences
chrome_options = Options()
chrome_options.binary_location = CHROME_BINARY_PATH
chrome_options.add_argument(r"user-data-dir=C:\Users\USER\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

# Set download preferences
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

previous_final_multipliers_path = None

def save_page():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mhtml_save_path = os.path.join(DOWNLOAD_DIR, f"page_{timestamp}.mhtml")
        txt_save_path = os.path.join(DOWNLOAD_DIR, f"page_{timestamp}.txt")
        final_multipliers_path = os.path.join(DOWNLOAD_DIR, f"final_multipliers_{timestamp}.txt")
        round_history_output_path = os.path.join(DOWNLOAD_DIR, f"round_history_{timestamp}.txt")

        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": DOWNLOAD_DIR
        })
        response = driver.execute_cdp_cmd("Page.captureSnapshot", {"format": "mhtml"})
        mhtml_content = response.get('data', '')
        with open(mhtml_save_path, "w", encoding="utf-8") as file:
            file.write(mhtml_content)

        with open(txt_save_path, "w", encoding="utf-8") as file:
            file.write(mhtml_content)

        process_html_content(mhtml_content, final_multipliers_path, round_history_output_path, timestamp)

        global previous_final_multipliers_path
        if previous_final_multipliers_path:
            compare_and_update_trial(final_multipliers_path, previous_final_multipliers_path)
        previous_final_multipliers_path = final_multipliers_path

    except Exception as e:
        print(f"An error occurred while saving the page: {e}")

def process_html_content(html_content, final_multipliers_path, round_history_output_path, timestamp):
    soup = BeautifulSoup(html_content, 'html.parser')

    with open(round_history_output_path, 'w', encoding='utf-8') as round_history_file:
        for element in soup.find_all():
            multiplier_value = element.get_text(strip=True)

            if "Round history" in multiplier_value:
                round_history_values = multiplier_value.split('Round history')[1].replace('=', '')
                round_history_file.write(f'{round_history_values}\n')

    with open(round_history_output_path, 'r', encoding='utf-8') as round_history_file:
        first_line = round_history_file.readline().strip()

    first_line = first_line.replace('\n', '').replace(' ', '')

    multipliers = re.findall(r'\d+\.\d+(?=x)', first_line)

    if multipliers:
        with open(final_multipliers_path, 'w', encoding='utf-8') as final_multipliers_file:
            final_multipliers_file.write(" ".join(multipliers) + "\n")

def compare_and_update_trial(new_final_multipliers_path, previous_final_multipliers_path):
    with open(previous_final_multipliers_path, 'r', encoding='utf-8') as file:
        previous_multipliers = file.read().strip().split()

    with open(new_final_multipliers_path, 'r', encoding='utf-8') as file:
        new_multipliers = file.read().strip().split()

    print(f"Newest multipliers: {new_multipliers}")
    print(f"Previous multipliers: {previous_multipliers}")

    first_common_index = None
    for i in range(len(new_multipliers)):
        if new_multipliers[i] in previous_multipliers:
            first_common_index = i
            break

    new_multipliers_to_add = []
    if first_common_index is not None:
        new_multipliers_to_add = new_multipliers[:first_common_index]
        if first_common_index + 1 < len(new_multipliers) and new_multipliers[first_common_index] == new_multipliers[first_common_index + 1]:
            new_multipliers_to_add.append(new_multipliers[first_common_index])
    else:
        new_multipliers_to_add = new_multipliers

    print(f"Numbers to the left of the common number: {new_multipliers_to_add}")

    if new_multipliers_to_add:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_entries = {
            'Timestamp': [timestamp] * len(new_multipliers_to_add),
            'Multiplier': new_multipliers_to_add
        }
        df_new_entries = pd.DataFrame(new_entries)

        if os.path.exists(TRIAL_EXCEL_FILE):
            df_existing = pd.read_excel(TRIAL_EXCEL_FILE)
        else:
            df_existing = pd.DataFrame(columns=['Timestamp', 'Multiplier'])

        df_final = pd.concat([df_new_entries, df_existing], ignore_index=True)

        df_final.to_excel(TRIAL_EXCEL_FILE, index=False)
        print(f"Numbers added to trial1 Excel sheet: {new_multipliers_to_add}")
    else:
        print("No new multipliers to add to the trial Excel file.")

betting_url = 'https://22bet.co.zm/casino/game/spribe/aviator'

try:
    print(f"Opening betting site: {betting_url}")
    driver.get(betting_url)

    interval = input("Enter the interval in seconds for saving the page as an MHTML file: ")
    interval = float(interval)

    input("Press Enter to start saving the page...")

    while True:
        time.sleep(interval)

        save_page()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()