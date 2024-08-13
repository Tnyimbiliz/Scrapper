from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, timedelta

#-------------------------- PRE-REQUISITES -----------------------
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Email settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "asventuresx@outlook.com"
EMAIL_PASSWORD = "Instacred@2024"

# Recipients
#RECIPIENTS = ["dwinansong52@gmail.com", "siamechaila@gmail.com", "jortiatisthomas@gmail.com"]
RECIPIENTS = ["jortiatisthomas@gmail.com"]

# Path to your ChromeDriver
chromedriver_path = 'C:/Users/LENOVO/Pictures/chromedriver-win64/chromedriver.exe'  # Replace with your actual path
print(f"Using ChromeDriver path: {chromedriver_path}")

# Set up the driver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.maximize_window()

# Open the website
url = "https://www.betway.co.zm/lobby/Casino/featured/Aviator/"
print(f"✈️ Navigating to {url}")
driver.get(url)


# --------------------------- FUNCTIONS ---------------------------------

def login():
    print("🔃 Logging in....")

    username = '978934162'
    password = 'Instacred'

    username_field = driver.find_element(By.ID, 'login-mobile')
    password_field = driver.find_element(By.ID, 'login-password')
    login_button = driver.find_element(By.XPATH, '*//button[@aria-label="Login" and @type="submit"]')

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button.click()
    print("✅ Logged in successfully!")
    driver.minimize_window()
    

    '''
    # Fail safe login


    try:
        parent_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'v-text-field__slot'))
        )
        username_field = parent_element.find_element(By.XPATH, '//input[@placeholder="Mobile Number" and @type="number"]')
        password_field = parent_element.find_element(By.XPATH, '//input[@placeholder="Password" and @type="password"]')
        
        parent_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'v-btn__content'))
        )
        cancel_button = parent_element.find_element(By.XPATH, '//button[@type="button" and @class="v-icon notranslate v-icon--link theme--light"]')

        cancel_button.click()
        login_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class,"mx-1") and contains(@class,"rounded-lg") and contains(@class,"v-btn") and contains(@class,"v-btn--text") and contains(@class,"theme--dark") and contains(@class,"v-size--default") and contains(@class,"white") and contains(@class,"font-weight-black")]'))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("✅ Logged in successfully!")
        driver.minimize_window()

    except Exception as e:
        print(f"❌ Unable to login: {e}")
        time.sleep(30)
        driver.quit()
    '''

def click_bet_button():
    try:
        parent_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "first-row") and contains(@class, "auto-game-feature")]'))
        )
        bet_button = parent_element.find_element(By.XPATH, './/button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]')
        bet_button.click()
        print("🎰 Bet button pressed!")
    except Exception as e:
        print(f"❌ unable to find bet button: {e}")

def click_auto_button():
    try:
        auto_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="tab ng-star-inserted" and text()=" Auto "]'))
        )
        auto_button.click()
        print("🤖 auto button pressed!")
    except Exception as e:
        print(f"❌ unable to find auto button")

def trigger_auto():
    try:
        # Wait until the toggle switch is present
        toggle_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]/span[@class="oval"]'))
        )
        # Click the toggle switch
        driver.execute_script("arguments[0].click();", toggle_div)
        print("✅ Auto bet triggered!")
    except Exception as e:
        print(f"❌ unable to trigger auto bet")

def insert_auto_value(number):
    try:
        # Find the specific parent element
        parent_element = driver.find_element(By.XPATH, '//div[contains(@class, "spinner") and contains(@class, "small")]')

        # Find the input element within the parent element
        input_element = parent_element.find_element(By.XPATH, './/input[@class="font-weight-bold" and @type="text" and @inputmode="decimal"]')

        # Send the desired value
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", input_element, number)

        action_chains = ActionChains(driver)

        action_chains.move_to_element(input_element).click().perform()

        input_element = parent_element.find_element(By.XPATH, './/input[@class="font-weight-bold" and @type="text" and @inputmode="decimal"]')

        # Verify the value was set
        value_set = input_element.get_attribute('value')
        if value_set == str(number):
            print(f"✅ Value {number} inserted successfully!")
        else:
            print(f"❌ Failed to set value. Current value: {value_set}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

def click_cash_out_button():

    try:
        cash_out_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btn") and contains(@class, "btn-warning") and contains(@class, "cashout") and contains(@class, "ng-star-inserted")]'))
        )
        cash_out_button.click()
        print("💵 cash out button pressed!")
        return True
    except Exception as e:
        return False
    
def insert_amount(amount):
    try:
        # Find the specific parent element
        parent_element = driver.find_element(By.XPATH, '//div[contains(@class, "spinner") and contains(@class, "big")]')

        # Find the input element within the parent element
        input_element = parent_element.find_element(By.XPATH, './/input[@class="font-weight-bold" and @type="text" and @inputmode="decimal"]')

        # Send the desired value
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", input_element, amount)

        action_chains = ActionChains(driver)

        action_chains.move_to_element(input_element).click().perform()

        input_element = parent_element.find_element(By.XPATH, './/input[@class="font-weight-bold" and @type="text" and @inputmode="decimal"]')

        # Verify the value was set
        value_set = input_element.get_attribute('value')
        if value_set == str(amount):
            print(f"✅ Value {amount} inserted successfully!")
        else:
            print(f"❌ Failed to set value. Current value: {value_set}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

def check_cashout_success():
    try:
        cashout_message = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "label") and contains(text(), "You have cashed out!")]'))
        )
        return True
    except Exception as e:
        return False

def convert_to_float(value):
    try:
        return float(value.replace('x',''))
    except ValueError:
        print("Invalid input, unable to convert!")
        return None
    
def send_email(subject, body):
        
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENTS, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def get_total_bets():
    try:
        # Find the specific parent element
        parent_element = driver.find_element(By.XPATH, '//div[contains(@class, "all-bets-block") and contains(@class, "d-flex") and contains(@class, "justify-content-between") and contains(@class, "align-items-center") and contains(@class, "px-2") and contains(@class, "pb-1")]')

        # Find the value element within the parent element
        value_element = parent_element.find_element(By.XPATH, './/div[@class="text-uppercase"]/following-sibling::div')

        return value_element.text.strip()
    except Exception as e:
        print(f"❌ Failed to retrieve total bets value: {e}")
        return None

def get_multiplier_data(n):
    multipliers = []
    for i in range(1, n + 1):
        # Get the nth child multiplier element within the 'payouts-block' div using a CSS selector
        element = driver.find_element(By.CSS_SELECTOR, f'div.payouts-block > app-bubble-multiplier.payout.ng-star-inserted:nth-child({i})')
        multipliers.append(element.text)
    return multipliers

def get_first_multiplier_data():
    # Get the first child multiplier element within the 'payouts-block' div using a CSS selector
    element = driver.find_element(By.CSS_SELECTOR, 'div.payouts-block > app-bubble-multiplier.payout.ng-star-inserted:first-child')
    multiplier = element.text
    return multiplier

def get_second_multiplier_data():
    # Get the second child multiplier element within the 'payouts-block' div using a CSS selector
    element = driver.find_element(By.CSS_SELECTOR, 'div.payouts-block > app-bubble-multiplier.payout.ng-star-inserted:nth-child(2)')
    multiplier = element.text
    return multiplier

# ------------------------- START --------------------------

#login function
login()

print("⏱️ Loading...")
time.sleep(10)

# ------------------------- TESTS ---------------------------
successful_tests = 0
# Check for iframes
try:
    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )
    driver.switch_to.frame(iframe)
    print("🛞 Switched to iframe!")
    successful_tests+=1
except Exception as e:
    print("❌No iframe found.")

try:
    bet_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]'))
        )
    print("✅ bet button found")
    successful_tests+=1
except:
    print("❌ could not find the bet button")

try:
    auto_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="tab ng-star-inserted" and @style="width: 100px;" and text()=" Auto "]'))
        )
    print("✅ auto button found")
    successful_tests+=1
except:
    print("❌ could not find the auto button")
    
if successful_tests == 3:
    print("✅ ALL TESTS SUCCESSFUL ✅")
else:
    print("❌ TESTS UNSUCESSFUL!")
    print("please try again later....")
    time.sleep(5)
    driver.quit()
    exit()

# ------------- ❌ Pressures -----------------------------
#  1️⃣ after bet, the data isnt scrapped 
#  1️⃣ the bet value, is not reset after a win ✅

# ------------------------- MAIN --------------------------

def main_game_loop():
    global cashout_value
    global bet_value
    global increment_factor

    multipliers = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, '//app-bubble-multiplier[contains(@class, "payout") and contains(@class, "ng-star-inserted")]'))
    )

    print("starting...")

    # ------------------ USER DEFINED VARIABLES ---------------- 

    cashout_value = 2
    bet_value = 0.1
    
    if bet_value <= 0:
        print("bet value is invalid")
        #send_email("Error","Invalid bet value: cannot be less than 0!")
        time.sleep(5)
        driver.quit()
        exit(0)

    increment_factor = 1

    if increment_factor <= 0:
        print("increment value is invalid")
        #send_email("Error","Invalid increment value: cannot be less than 0!")
        time.sleep(5)
        driver.quit()
        exit(0)

    last_bet_count = 2
    maximum_multiplier_value = 3

    attempts = 3

    # -----------------------------------------------------------

    click_auto_button()
    trigger_auto()

    while True:

        initial_multipliers = get_multiplier_data(last_bet_count)
        last_bets = [convert_to_float(multiplier) for multiplier in initial_multipliers[:last_bet_count]]
        
        if len(last_bets) == last_bet_count and all(bet < maximum_multiplier_value for bet in last_bets):

            print(f"🚨 Last {last_bet_count} bets were below {maximum_multiplier_value}, betting {bet_value} with cashout value of {cashout_value} and increment factor of {increment_factor}")

            original_bet_value = bet_value
            if activate_bot(attempts):
                print("✅ Bet successfully cashed out after 3 low bets")

                time.sleep(10)
            else:
                print("❌ didnt cash out!, stopping the program")
                time.sleep(10)
                driver.quit()
                exit(0)
            
            bet_value = original_bet_value

def activate_bot(attempts):
    global bet_value
    global cashout_value
    global count


    print("bot activated!!!")
    #send_email("Bot actived!","The bot has been triggered and has now begun betting." )

    success_trigger = 0

    for attempt in range(attempts):

        if success_trigger == 1:
            return True

        if attempt == 0:
            pass
        else:
            bet_value = bet_value * increment_factor

        print(f"bet value: {bet_value}")

        if insert_amount(bet_value):
            continue
        
        if insert_auto_value(cashout_value):
            continue

        time.sleep(2)
        if click_bet_button():
            continue

        print(f"🎰 Bet placed successfully! - attempt {attempt+1}")

        locked_indicator = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and contains(@class, "locked")]'))
        )
        print("🔒 LOCKED!!!!")

        takeoff_indicator = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and not(contains(@class, "locked"))]'))
        )
        print("✈️ --PLANE HAS TAKEN OFF--")

        seen_multipliers = [get_first_multiplier_data()]
        trigger = 0

        while True:
            if check_cashout_success():
                print(f"💵 Cashed out at {cashout_value}")
                success_trigger = 1
                return True
            else:
                # Check for a new multiplier to determine if the plane has flown away
                try:
                    second_multiplier = get_second_multiplier_data()
                    new_multipliers = [get_first_multiplier_data()]
                    new_values = [value for value in new_multipliers if value not in seen_multipliers]

                    if trigger == 0:
                        if second_multiplier == new_multipliers[0]:
                            print("repeated value!!!!!!!!!!!!!")
                            new_values = [new_multipliers[0]]
                            trigger = 1 #trigger it not to look for a second value anymore

                        if new_values:
                            print(f"💔 Plane has flown away at {new_values[0]}")
                            seen_multipliers = (seen_multipliers + new_values)[-1:]
                            break
                    else:
                        if new_values:
                            print(f"💔 Plane has flown away at {new_values[0]}")
                            seen_multipliers = (seen_multipliers + new_values)[-1:]
                            trigger = 0
                            break

                except StaleElementReferenceException:
                    print("StaleElementReferenceException encountered. Re-locating elements.")
                except Exception as e:
                    print(f"❌ An error occurred: {e}")
                    break
    return False

try:
    main_game_loop()
except Exception as e:
    print(f"An error occurred: {e}")
    #send_email("Error", "An unexpected error occured : "+ str(e))
    driver.quit()

# Close the driver
driver.quit()
