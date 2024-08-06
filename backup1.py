#service = Service('C:/Program Files/Google/Chrome/Application/Chrome.exe')
import math
import numpy as np
import sounddevice as sd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to generate a test sound

#-------------------------- PRE-REQUISITES -----------------------

# Replace with your actual login credentials
username = '978934162'
password = 'Instacred'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to your ChromeDriver
chromedriver_path = 'C:/Users/LENOVO/Pictures/chromedriver-win64/chromedriver.exe'  # Replace with your actual path
print(f"Using ChromeDriver path: {chromedriver_path}")

# Set up the driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the website
url = "https://www.betway.co.zm/lobby/Casino/featured/Aviator/"
print(f"✈️ Navigating to {url}")
driver.get(url)


# --------------------------- FUNCTIONS ---------------------------------

def generate_test_sound():
    duration = 2.0  # seconds
    frequency = 440.0  # Hz
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_signal = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(audio_signal, sample_rate)
    sd.wait()

def login():

    print("🔃 logging in....")
    # Find and fill the username and password fields, then submit
    try:
        time.sleep(5)

        username_field = driver.find_element(By.ID, 'input-145')  # Use the correct attribute (e.g., NAME, ID, CLASS_NAME)
        password_field = driver.find_element(By.ID, 'input-146')  # Use the correct attribute (e.g., NAME, ID, CLASS_NAME)

        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "mx-1") and contains(@class, "rounded-lg") and contains(@class, "v-btn") and contains(@class, "v-btn--text") and contains(@class, "theme--light") and contains(@class, "v-size--default") and contains(@class, "white--text") and contains(@class, "primary") and contains(@class, "mt-2") and contains(@class, "mb-2")]'))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("✅ Logged in successfully!")

    except Exception as e:
        try:
            username_field = driver.find_element(By.ID, 'input-157')
            password_field = driver.find_element(By.ID, 'input-158')

            login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "mx-1") and contains(@class, "rounded-lg") and contains(@class, "v-btn") and contains(@class, "v-btn--text") and contains(@class, "theme--light") and contains(@class, "v-size--default") and contains(@class, "white--text") and contains(@class, "primary") and contains(@class, "mt-2") and contains(@class, "mb-2")]'))
            )

            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            print("✅ Logged in successfully! --SECOND ATTEMPT--")
        except:
            try:
                username_field = driver.find_element(By.ID, 'input-166')
                password_field = driver.find_element(By.ID, 'input-167')

                login_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "mx-1") and contains(@class, "rounded-lg") and contains(@class, "v-btn") and contains(@class, "v-btn--text") and contains(@class, "theme--light") and contains(@class, "v-size--default") and contains(@class, "white--text") and contains(@class, "primary") and contains(@class, "mt-2") and contains(@class, "mb-2")]'))
                )

                username_field.send_keys(username)
                password_field.send_keys(password)
                login_button.click()
                print("✅ Logged in successfully! --THIRD ATTEMPT--")
            except:
                print("❌ Username and password fields not found.")
                print("please try again later...")
                time.sleep(30)
                driver.refresh()

def click_bet_button():

    try:
        bet_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]'))
        )
        bet_button.click()
        print("🎰 Bet button pressed!")
    except Exception as e:
        print(f"❌ unable to find bet button")

def click_cash_out_button():

    try:
        cash_out_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btn") and contains(@class, "btn-warning") and contains(@class, "cashout") and contains(@class, "ng-star-inserted")]'))
        )
        cash_out_button.click()
        return True
    except Exception as e:
        return False

def click_add_button():

    try:
        add_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "plus") and contains(@class, "ng-star-inserted")]'))
        )
        add_button.click()
        print("➕ add button pressed!")

    except Exception as e:
        print("❌ could not find add button")

def click_minus_button():

    try:
        add_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "minus") and contains(@class, "ng-star-inserted")]'))
        )
        add_button.click()
        print("➖ minus button pressed!")

    except Exception as e:
        print("❌ could not find add button")

def estimate_multiplier(start_time):
    elapsed_time = time.time() - start_time
    #adjust the growth rate here
    growth_rate = 0.09;
    return 1 + (math.exp(elapsed_time*growth_rate)-1)  # Slightly exponential growth


# ------------------------- START --------------------------

#login function
login()

print("⏱️ Loading...")
time.sleep(10)

# ------------------------- TESTS ---------------------------

# Check for iframes
try:
    iframe = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )
    driver.switch_to.frame(iframe)
    print("🛞 Switched to iframe!")
except Exception as e:
    print("❌No iframe found.")

# Find the add button and click it
try:
    print("🔃 trying to find add button")
    add_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "plus") and contains(@class, "ng-star-inserted")]'))
    )
    print("✅ add button found")

except Exception as e:
    print("❌ could not find the add button")

# Find the add button and click it
try:
    print("🔃 trying to find minus button")
    minus_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "minus") and contains(@class, "ng-star-inserted")]'))
    )
    print("✅ minus button found")

except Exception as e:
    print("❌ could not find the minus button")


try:
    print("🔃 trying to find bet button")
    bet_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]'))
        )
    print("✅ bet button found")
except:
    print("❌ could not find the bet button")
    
# ------------------------- MAIN --------------------------


# Main game loop with added algorithm
successful_cash_outs = 0;
try:
    while True:
        for attempt in range(3):
            #click_add_button()

            takeoff_indicator = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and not(contains(@class, "locked"))]'))
            )
            click_bet_button()
            print(f"🎰 Bet placed successfully! -- Attempt {attempt+1}")    
            locked_indicator = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and contains(@class, "locked")]'))
            )
            print("🔒 LOCKED!!!!")
            takeoff_indicator = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and not(contains(@class, "locked"))]'))
            )

            print("✈️ --PLANE HAS TAKEN OFF--")
            start_time = time.time()

            # Monitor the multipliers to detect when a new one is added
            existing_multipliers = driver.find_elements(By.XPATH, '//app-bubble-multiplier[contains(@class, "payout") and contains(@class, "ng-star-inserted")]')

            while True:
                current_multiplier = estimate_multiplier(start_time)
                print(f"Current Multiplier: {current_multiplier:.2f}")
                
                # Check if the estimated multiplier has reached the desired level
                desired_multiplier = 1.5  # Replace with your desired multiplier
                if current_multiplier >= desired_multiplier:
                    if click_cash_out_button():
                        print(f"💵 Cashed out at {current_multiplier:.2f}x")
                        successful_cash_outs +=1
                        break
                    else:
                        print("💔 unable to cash out!")
                        break

                # Check for a new multiplier to determine if the plane has flown away
                new_multipliers = driver.find_elements(By.XPATH, '//app-bubble-multiplier[contains(@class, "payout") and contains(@class, "ng-star-inserted")]')
                if len(new_multipliers) > len(existing_multipliers):
                    # Extract the value of the last added multiplier
                    last_multiplier_element = new_multipliers[0]
                    last_multiplier_value = last_multiplier_element.text
                    print(f"💔 --PLANE HAS FLOWN AWAY-- at multiplier element text: {last_multiplier_value}")
                    break

                time.sleep(0.1)
            
            if successful_cash_outs>0:
                break
        else:
            print("❌ All bets failed, stopping the program")
            driver.quit()
            break
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()


# Close the driver
driver.quit()

#plus ng-star-inserted