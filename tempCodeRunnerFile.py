def login():
    print("🔃 Logging in....")

    username = '770125562'
    password = 'thebag'

    try:
        parent_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'v-text-field__slot'))
        )
        username_field = parent_element.find_element(By.XPATH, '//input[@placeholder="Mobile Number" and @type="number"]')
        print("username found!")
        password_field = parent_element.find_element(By.XPATH, '//input[@placeholder="Password" and @type="password"]')
        print("password found!")
        
        login_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class,"mx-1") and contains(@class,"rounded-lg") and contains(@class,"v-btn") and contains(@class,"v-btn--text") and contains(@class,"theme--light") and contains(@class,"v-size--default") and contains(@class,"white--text") and contains(@class,"primary")]'))
        )
        print("button found!")


        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("✅ Logged in successfully!")

    except Exception as e:
        print(f"❌ Unable to login: {e}")
        time.sleep(30)
        driver.quit()