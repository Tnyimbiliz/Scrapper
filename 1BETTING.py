import asyncio
import threading
import smtplib
import time
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, timedelta


# -------------------------- SETUP -------------------------------
# Set up Firefox options
firefox_options = FirefoxOptions()
firefox_options.add_argument("--no-sandbox")
#firefox_options.add_argument("--headless")  # Run without a GUI
firefox_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
firefox_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
firefox_options.add_argument("--single-process")  # Run Firefox in a single process mode
firefox_options.add_argument("--disable-extensions")  # Disable all extensions
firefox_options.add_argument("--disable-logging")  # Disable logging
firefox_options.add_argument("--disable-infobars")  # Disable the "Chrome is being controlled" info bar
firefox_options.add_argument("--disable-browser-side-navigation")  # Disable browser side navigation
firefox_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
firefox_options.add_argument("--disable-notifications")  # Disable notifications
firefox_options.add_argument("--mute-audio")  # Mute audio
firefox_options.add_argument("--no-zygote")  # Disable zygote process for less overhead
firefox_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid being detected as a bot
firefox_options.add_argument("--disable-background-timer-throttling")  # Disable throttling of background timers
firefox_options.add_argument("--disable-backgrounding-occluded-windows")  # Reduce resource usage for occluded windows
firefox_options.add_argument("--disable-renderer-backgrounding")  # Disable renderer backgrounding to reduce CPU load
firefox_options.add_argument("--disable-features=VizDisplayCompositor")  # Reduces CPU usage by disabling VizDisplayCompositor
firefox_options.add_argument("--disable-site-isolation-trials")  # Disable site isolation to reduce CPU load

# Email settings
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "asventuresx@outlook.com"
EMAIL_PASSWORD = "Instacred@2024"
RECIPIENTS = ["jortiatisthomas@gmail.com"]

# Path to your GeckoDriver
geckodriver_path = 'geckodriver-v0.35.0-win64/geckodriver.exe'  # Replace with your actual path if needed
print(f"Using GeckoDriver path: {geckodriver_path}")

# Set up the driver
service = FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)


# Open the website
url = "https://betting.co.zm/spribe/8200" 
print(f"✈️ Navigating to {url}")
driver.get(url)

# -------------------------- ASYNC FUNCTIONS ----------------------------

async def perform_tests():
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
        print("❌ could not find the auto button");
        
    if successful_tests == 3:
        print("✅ ALL TESTS SUCCESSFUL ✅")
    else:
        print("❌ TESTS UNSUCESSFUL!")
        print("please try again later....")
        time.sleep(5)
        driver.quit()
        exit()

async def login():
    print("🔃 Logging in....")
    await asyncio.sleep(5)

    username = '0978934162'
    password = 'Instacred@1'

    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.ID, 'login-form-submit-button')
    #login_button = driver.find_element(By.XPATH, '*//button[@class ="btn SB-btnSecondary active SB-btnLarge"]')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    print("✅ Logged in successfully!")
    #driver.minimize_window()
    await asyncio.sleep(1)  # Simulate async work

async def switch_to_iframe():
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
        driver.switch_to.frame(iframe)
        print("🛞 Switched to iframe!")

    except Exception as e:
        print("❌No iframe found.")

async def send_email(subject, body):
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

async def click_bet_button():
    try:
        takeoff_indicator = await asyncio.to_thread(
            WebDriverWait(driver, 60).until,
            EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and not(contains(@class, "locked"))]'))
        )

        parent_element = await asyncio.to_thread(
            WebDriverWait(driver, 30).until,
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "first-row") and contains(@class, "auto-game-feature")]'))
        )
        bet_button = parent_element.find_element(By.XPATH, './/button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]')
        bet_button.click()
        print("🎰 Bet button pressed!")
    except Exception as e:
        print(f"❌ Unable to find bet button: {e}")

async def click_auto_button():
    try:
        auto_button = await asyncio.to_thread(
            WebDriverWait(driver, 30).until,
            EC.presence_of_element_located((By.XPATH, '//button[@class="tab ng-star-inserted" and text()=" Auto "]'))
        )
        auto_button.click()
        print("🤖 Auto button pressed!")
    except Exception as e:
        print(f"❌ Unable to find auto button: {e}")

async def trigger_auto():
    try:
        toggle_div = await asyncio.to_thread(
            WebDriverWait(driver, 30).until,
            EC.presence_of_element_located((By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]/span[@class="oval"]'))
        )
        driver.execute_script("arguments[0].click();", toggle_div)
        print("✅ Auto bet triggered!")
    except Exception as e:
        print(f"❌ Unable to trigger auto bet: {e}")

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
            return True
        else:
            print(f"❌ Failed to set value. Current value: {value_set}")
            return False

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
            return True
        else:
            print(f"❌ Failed to set value. Current value: {value_set}")
            return False

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
    
async def get_multiplier_data(n):
    try:
        multipliers = []
        for i in range(1, n + 1):
            # Get the nth child multiplier element within the 'payouts-block' div using a CSS selector
            element = driver.find_element(By.CSS_SELECTOR, f'div.payouts-block > app-bubble-multiplier.payout.ng-star-inserted:nth-child({i})')
            multipliers.append(element.text)
        return multipliers
    except Exception as e:
        print(f"❌ Failed to get multiplier data: {e}")
        return None
    
async def get_first_multiplier_data():
    # Get the first child multiplier element within the 'payouts-block' div using a CSS selector
    element = driver.find_element(By.CSS_SELECTOR, 'div.payouts-block > app-bubble-multiplier.payout.ng-star-inserted:first-child')
    multiplier = element.text
    return multiplier

async def get_second_multiplier_data():
    # Get the second child multiplier element within the 'payouts-block' div using a CSS selector
    element = driver.find_element(By.CSS_SELECTOR, 'div.payouts-block > app-bubble-multiplier.payout.ng-star-inserted:nth-child(2)')
    multiplier = element.text
    return multiplier

async def convert_to_float(value):
    try:
        return float(value.replace('x', ''))
    except ValueError:
        print("Invalid input, unable to convert!")
        return None

async def check_cashout_success():
    try:
        cashout_message = await asyncio.to_thread(
            WebDriverWait(driver, 1).until,
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "label") and contains(text(), "You have cashed out!")]'))
        )
        return True
    except Exception:
        return False

async def save_data(data):
    # Create the "multipliers" directory if it doesn't exist
    folder_path = os.path.join(os.getcwd(), 'multipliers')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save to betway_multipliers.txt in the "multipliers" folder
    text_file_path = os.path.join(folder_path, 'betting_multipliers.txt')
    with open(text_file_path, 'a') as file:
        file.write(f"{data}\n")

    # Convert data to DataFrame and save to betway_multipliers.xlsx in the "multipliers" folder
    df = pd.DataFrame(data, columns=['Value', 'Timestamp', 'Total Bets'])
    excel_file_path = os.path.join(folder_path, 'betting_multipliers.xlsx')
    try:
        existing_df = pd.read_excel(excel_file_path)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_excel(excel_file_path, index=False)
    # ------------

async def get_total_bets():
    try:
        parent_element = driver.find_element(By.XPATH, '//div[contains(@class, "all-bets-block") and contains(@class, "d-flex") and contains(@class, "justify-content-between") and contains(@class, "align-items-center") and contains(@class, "px-2") and contains(@class, "pb-1")]')
        value_element = parent_element.find_element(By.XPATH, './/div[@class="text-uppercase"]/following-sibling::div')
        return value_element.text.strip()
    except Exception as e:
        print(f"❌ Failed to retrieve total bets value: {e}")
        return None

# The async version of the main loop
async def main_game_loop():
    global SIGNAL

    global cashout_value
    global bet_value
    global increment_factor
    global last_bet_count
    global maximum_multiplier_value
    global attempts

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//app-bubble-multiplier[contains(@class, "payout") and contains(@class, "ng-star-inserted")]'))
    )
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="tab ng-star-inserted" and text()=" Auto "]'))
    )

    print("Starting main game loop...")

    # ------------------ USER DEFINED VARIABLES ---------------- 
    cashout_value = 3
    bet_value = 0.1
    increment_factor = 4
    last_bet_count = 3
    maximum_multiplier_value = 5
    attempts = 2

    if bet_value <= 0 or increment_factor <= 0:
        print("Invalid bet or increment value")
        await send_email("Error", "Invalid bet or increment value!")
        await asyncio.sleep(5)
        driver.quit()
        exit(0)

    await click_auto_button()
    time.sleep(1)
    await trigger_auto()

    SIGNAL = 0
    while True:
        initial_multipliers = await get_multiplier_data(last_bet_count)
        last_bets = [await convert_to_float(multiplier) for multiplier in initial_multipliers]

        if SIGNAL == 1: 
            SIGNAL = 0;
            if all(bet < maximum_multiplier_value for bet in last_bets):
                print(f"🚨 Last {last_bet_count} bets were below {maximum_multiplier_value}, betting {bet_value} with cashout value of {cashout_value} and increment factor of {increment_factor}")
                print(f"last {last_bet_count}: {last_bets}")
                
                original_bet_value = bet_value

                success = await activate_bot(attempts)
                
                if success:
                    print("✅ Bet successfully cashed out after 3 low bets")
                    SIGNAL = 0
                else:
                    print("❌ All attempts failed. Stopping the bot but continuing to scrape.")
                    break  # Stop the betting loop, but scraping continues

                # Reset bet value after success or failure
                bet_value = original_bet_value

        time.sleep(1)

# The async version of the bot activation function
async def activate_bot(attempts):
    global SIGNAL
    global bet_value
    global cashout_value

    print("Bot activated!!!")
    #await send_email("Bot activated!", "The bot has been triggered and has now begun betting.")

    insert_auto_value(cashout_value)

    for attempt in range(attempts):
        print(f"Bet attempt {attempt + 1} out of {attempts}")

        if attempt > 0:
            bet_value *= increment_factor
                    
        insert_amount(bet_value)

        await asyncio.sleep(1)
        await click_bet_button()

        print(f"🎰 Bet placed successfully! - attempt {attempt + 1}")

        await asyncio.to_thread(
            WebDriverWait(driver, 180).until,
            EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and contains(@class, "locked")]'))
        )
        print("🔒 LOCKED!!!!")

        await asyncio.to_thread(
            WebDriverWait(driver, 60).until,
            EC.presence_of_element_located((By.XPATH, '//app-bet-control[contains(@class, "bet-control") and contains(@class, "double-bet") and not(contains(@class, "locked"))]'))
        )
        print("✈️ --PLANE HAS TAKEN OFF--")
        SIGNAL = 0

        try:
            parent_element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "first-row") and contains(@class, "auto-game-feature")]'))
            )
            if parent_element.find_element(By.XPATH, './/button[contains(@class, "btn-success") and contains(@class, "bet") and contains(@class, "ng-star-inserted")]'):
                print("value was staged out!")
        except:
            pass

        while True:
            if await check_cashout_success():
                print(f"💵 Cashed out at {cashout_value}")
                return True  # Return True to indicate success 
            
            time.sleep(1)
            if SIGNAL == 1:
                print("💔 The Plane has flown away!!")
                break
    return False

# Asynchronous multiplier scraping function
async def scrape_multipliers():
    global SIGNAL
    print("scrapper started...")
    seen_multipliers = [await get_first_multiplier_data()]
    count = 1
    trigger = 0
    last_saved_time = datetime.now()

    while True:
        try:
            total_bets = await get_total_bets()
            second_multiplier = await get_second_multiplier_data()
            new_multipliers = [await get_first_multiplier_data()]
            new_values = [value for value in new_multipliers if value not in seen_multipliers]

            if trigger == 0:
                if second_multiplier == new_multipliers[0]:
                    print("Repeated value!!!!!!!!!!!!!")
                    new_values = [new_multipliers[0]]
                    trigger = 1

                if new_values:
                    SIGNAL = 1
                    print(f"✅ {count} = {new_values[0]}")
                    data = [(value.rstrip('x'), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_bets) for value in new_values]
                    await save_data(data)
                    seen_multipliers = (seen_multipliers + new_values)[-1:]
                    count += 1
                    last_saved_time = datetime.now()


            else:
                if new_values:
                    SIGNAL = 1
                    print(f"✅ {count} = {new_values[0]}")
                    data = [(value.rstrip('x'), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_bets) for value in new_values]
                    await save_data(data)
                    seen_multipliers = (seen_multipliers + new_values)[-1:]
                    count += 1
                    last_saved_time = datetime.now()
                    trigger = 0

            time.sleep(1)
                    
            if datetime.now() - last_saved_time > timedelta(minutes=3):
                print("Timeout!")
                await send_email("Timeout", "It's been 3 minutes without a new value.")
                driver.quit()
                exit(0)

        except StaleElementReferenceException:
            print("StaleElementReferenceException encountered. Re-locating elements.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            break

# Asynchronous function to run the bot
async def run_bot():
    try:
        # Start the tasks with debug prints
        task_betting = asyncio.create_task(main_game_loop())
        task_scraper = asyncio.create_task(scrape_multipliers())

        # Run both tasks concurrently until they finish or an exception is raised
        print("Running both tasks concurrently...")
        await asyncio.gather(task_betting, task_scraper)

    except Exception as e:
        print(f"An error occurred during bot operation: {e}")
    finally:
        driver.quit()

def run_bot_loop():
    asyncio.run(main_game_loop())

def run_scrapper_loop():
    asyncio.run(scrape_multipliers())

# -------------------------- ENTRY POINT --------------------------

if __name__ == "__main__":
    try:
        # Run login first, then start the bot
        asyncio.run(login())
        print("⏱️ Loading...")
        asyncio.run(asyncio.sleep(5))

        asyncio.run(perform_tests())

        global SIGNAL
        SIGNAL = 0

        bot_thread = threading.Thread(target=run_bot_loop)
        scraper_thread = threading.Thread(target=run_scrapper_loop)

        bot_thread.start()
        scraper_thread.start()

        bot_thread.join()
        scraper_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
