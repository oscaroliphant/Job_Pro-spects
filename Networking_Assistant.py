from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException

# Input your LinkedIn username and password
linkedin_username = 'username@example.com'
linkedin_password = 'password'
company_name = input('Input company name: ')

# Initialize the WebDriver for Microsoft Edge
# Make sure you have the appropriate WebDriver for Edge and its path
driver = webdriver.Chrome()

# Open LinkedIn
driver.get('https://www.linkedin.com/')

# Wait for the login page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.NAME, 'session_key')))

# Log in with your username and password
email_field = driver.find_element(By.NAME, 'session_key')
password_field = driver.find_element(By.NAME, 'session_password')
login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

email_field.send_keys(linkedin_username)
password_field.send_keys(linkedin_password)
login_button.click()

# Wait for the page to load after login
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.search-global-typeahead__input')))

# Find the search box and enter the company name
#search_box = driver.find_element(By.CSS_SELECTOR, 'input.search-global-typeahead__input')
#search_box.send_keys(company_name)

# Press Enter to perform the search
#search_box.send_keys(Keys.RETURN)

# Shortcut to people section on the company's page by getting WebDriver to run URL
driver.get(f"https://www.linkedin.com/company/{company_name}/people/?facetGeoRegion=101165590&keywords=recruitment")

sleep(2)

# Find all buttons on the page
all_buttons = driver.find_elements(By.TAG_NAME, "button")

# Loop through each button and perform an action
for button in all_buttons:
    if button.text == "Connect":
        action = ActionChains(driver)
        action.move_to_element(button)
        action.perform()
        button.click()

        try:
            # Check if 'Learn why' link is present
            # If present, connection/message request not allowed without their email
            learn_why_link = driver.find_element(By.XPATH, "//a[contains(@href, 'linkedin/suggested/1239/email-address-needed-for-an-invitation')]")
            # If found, close the dialogue
            close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            close_button.click()
            sleep(2)
        except NoSuchElementException:
            # If 'Learn why' link is not found, handle the 'Add a note' functionality
            try:
                add_note_button = driver.find_element(By.XPATH, "//button[@aria-label='Add a note']")
                add_note_button.click()
                sleep(2)
                textarea = driver.find_element(By.XPATH, "//textarea[@name='message']")
                custom_message = "Hi there, I wonder if you’d be happy to connect me to your recruiting team?"
                "I’m a Masters Chem Eng (Class I) graduate from UoB keen to get involved in the FinTech industry."
                f"I’d be really interested to see what opportunities there might be with {company_name}!\n\nKind regards,\n\nOscar Oliphant"
                textarea.send_keys(custom_message)
                # Practice run so don't send message and dismiss instead
                close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                close_button.click()
            except NoSuchElementException:
                # If 'Add a note' button or text area not found, handle the error or add further steps here
                # However, this is unlikely since I've not come across a situation when you can neither message or not message
                print("Add note functionality elements not found")
