import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import StaleElementReferenceException

# ----------------------------------------------------------------

#-------------------------- PRE-REQUISITES -----------------------
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

def login():
    print("🔃 logging in....")

    username = '770125562'
    password = 'thebag'

    try:
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'login-mobile'))
        )
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'login-password'))
        )
        login_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class,"whitespace-nowrap") and contains(@class,"bg-identity") and contains(@class,"w-full")]'))
        )

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("✅ Logged in successfully!")

    except Exception as e:
        print(f"unable to login{e}")
        time.sleep(30)
        driver.quit()

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


def get_multiplier_data():
    # Get all multiplier elements
    elements = driver.find_elements(By.XPATH, '//app-bubble-multiplier[contains(@class, "payout") and contains(@class, "ng-star-inserted")]')
    multipliers = [element.text for element in elements]
    return multipliers


def convert_to_float(value):
    try:
        return float(value.replace('x',''))
    except ValueError:
        print("Invalid input, unable to convert!")
        return None
# ------------------------- START --------------------------

#login function
login()

print("⏱️ Loading...")
time.sleep(10)

# ------------------------- TESTS ---------------------------

successful_tests = 0
# Check for iframes
try:
    iframe = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )
    driver.switch_to.frame(iframe)
    print("🛞 Switched to iframe!")
    successful_tests+=1
except Exception as e:
    print("❌No iframe found.")

try:
    #print("🔃 trying to find bet button")
    bet_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]'))
        )
    print("✅ bet button found")
    successful_tests+=1
except:
    print("❌ could not find the bet button")

try:
    #print("🔃 trying to find auto button")
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

# ------------------------- MAIN --------------------------

def main_game_loop():
    global cashout_value
    global bet_value

    cashout_value = 3.2
    bet_value = 0.1

    click_auto_button()
    time.sleep(2)
    trigger_auto()

    global last_three_bets
    initial_multipliers = get_multiplier_data()
    last_three_bets = [convert_to_float(multiplier) for multiplier in initial_multipliers[:3]]


    print(f"initial multipliers: {initial_multipliers}")

    while True:
        if len(last_three_bets) == 3 and all(float(bet) < 5.0 for bet in last_three_bets):
            print("🚨 Last 3 bets were below 5.0, betting 1 with cashout value of 1.2")
            bet_value = 1
            cashout_value = 1.2

            if place_bets():
                print("✅ Bet successfully cashed out after 3 low bets")
                time.sleep(10)
                driver.quit()
                break
            else:
                print("❌ didnt cash out!, stopping the program")
                driver.quit()
                break


def place_bets():
    global bet_value
    global cashout_value
    global last_three_bets

    print(f"last 3 bets: {last_three_bets}")

    insert_auto_value(cashout_value)
    insert_amount(bet_value)

    # random click
    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_element.click()

    time.sleep(2)
    click_bet_button()
    print(f"🎰 Bet placed successfully!")
    locked_indicator = WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and contains(@class, "locked")]'))
    )
    print("🔒 LOCKED!!!!")
    takeoff_indicator = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and not(contains(@class, "locked"))]'))
    )

    print("✈️ --PLANE HAS TAKEN OFF--")

    initial_multipliers = get_multiplier_data()
    seen_multipliers = list(initial_multipliers[:1])

    while True:
        if check_cashout_success():
            print(f"💵 Cashed out at {cashout_value}")
            last_three_bets.append(cashout_value)
            if len(last_three_bets) > 3:
                last_three_bets.pop(0)
            return True
        else:
            # Check for a new multiplier to determine if the plane has flown away
            try:
                new_multipliers = get_multiplier_data()
                second_multiplier = new_multipliers[1]
                new_multipliers = new_multipliers[:1]
                new_values = [value for value in new_multipliers if value not in seen_multipliers]

                if new_values:
                    print(f"💔 Plane flew away at {new_values[0]}")
                    last_three_bets.append(float(new_values[0]))
                    if len(last_three_bets) > 3:
                        last_three_bets.pop(0)
                    return False

                if second_multiplier == new_multipliers[0]:
                    print(f"💔 Plane flown away at {new_multipliers[0]}")
                    last_three_bets.append(float(new_multipliers[0]))
                    if len(last_three_bets) > 3:
                        last_three_bets.pop(0)
                    return False

            except StaleElementReferenceException:
                print("StaleElementReferenceException encountered. Re-locating elements.")
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                break

try:
    main_game_loop()
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()

# Close the driver
driver.quit()
