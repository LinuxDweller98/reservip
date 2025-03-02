# Description: This script reserves a static local IP adress for a given MAC address.
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import argparse
import logging

# Defines how we want our logs to look like.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Function to get better control over the messages. You can easily change logging.info to logging.error or logging.warning to get different log levels.
def log_message(message):
    """
    Logs a message to the console.
    
    Parameters:
    message: As string: The message to log.
    """
    logging.info(message)

# Function to find an html element by XPATH, NAME or ID
# The reasoning behind this function is to make the code more readable and to avoid code duplication.
# The problems this function solved for me is not having to worry about if the element is interactive or not.
# If its not yet interactive it waits for it to become interactive, like a failsafe.
def find_element(driver, element_search_data, by_type):
    """
    Finds an element on the webpage.

    Parameters:
    driver: The WebDriver instance controlling the browser.
    by_type: The method to locate the element. Must be the full selenium "By" class attribute such as By.XPATH, By.NAME, or By.ID
    element_search_data: The value corresponding to the by_type used for locating the element.

    Returns:
    The WebElement found using the specified method and value.
    """

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((by_type, element_search_data)) # presence_of_element_located is used to ensure the element is present in the DOM
        )
        if element.is_enabled() and element.is_displayed(): # is_enabled() and is_displayed() are used to check if the element is interactive
            log_message(f"Element with {by_type} {element_search_data} found and interactive.")
            return element
        else:
            log_message(f"Element with {by_type} {element_search_data} found but not yet interactive.")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((by_type, element_search_data)) # element_to_be_clickable is used to ensure the element is visible and enabled so it can be interacted with
            )
            log_message(f"Element with {by_type} {element_search_data} is now interactive.")
            return element  
    except Exception as e:
        log_message(f"Element with {by_type} {element_search_data} was not found or did not become interactive within timeout. ERROR: {e}")
        return None

# Function to attempt login
def attempt_login(driver, username_value, password_value):
    """
    Attempts to login to the routers web interface.

    Parameters:
    driver: The WebDriver instance controlling the browser.
    username_value: as string: The username to login with.
    password_value: as string: The password to login with.

    username_field_id: local, as string: The html ID of the username field.
    password_field_id: local, as string: The html ID of the password field.
    login_button_id: local, as string: The html ID of the login button.
    """  
    username_field_id = "user"
    password_field_id = "password"
    login_button_id = "button-blue"

    # Find the username field and enter the username
    username_field = find_element(driver, username_field_id, By.ID)
    if username_field is None:
        log_message("Username field was not returned. Login will fail.")
        raise # raises exception to main()
    else:
        username_field.clear() # clears the field before sending keys
        username_field.send_keys(username_value)
        log_message("keys sent to username field.")

    # Find the password field and enter the password
    password_field = find_element(driver, password_field_id, By.ID)
    if password_field is None:
        log_message("Password field was not returned. Login will fail.")
        raise # raises exception to main()
    else:
        password_field.send_keys(password_value)
        log_message("keys sent to password field")

    # Find the login button and click it
    login_button = find_element(driver, login_button_id, By.ID)
    if login_button is None:
        log_message("Login button was not returned. Login will fail.")
        raise # raises exception to main()
    else:
        login_button.click()
        log_message("Login button clicked.")

def set_arg_parser():
    description = """Reserves a static IP address for a given MAC address through your routers web interface.
    DISCLAIMER: This script will only work if you have a tele2 wifi hub C2 router, unless you wanna change the code to work for your specific model :).
    USAGE: reserveip <mac_address> <ip_address>"""
    parser = argparse.ArgumentParser(description)
    parser.add_argument('mac', type=str, help='Mac address in format xx:xx:xx:xx:xx:xx')
    parser.add_argument('ip', type=str, help='IP address in format xxx.xxx.xxx.xxx')
    args = parser.parse_args()
    return args

# Function to add an IP reservation
def add_ip_reservation(driver, mac_value, ip_value):
    """
    Adds an IP reservation to the routers DHCP settings.
    
    mac_value: as string: The MAC address to reserve the IP for.
    ip_value: as string: The IP address to reserve for the MAC address.

    add_button_id: local, as string: The html ID of the add button.
    mac_field_xpath: local, as string: The xpath of the MAC field.
    ip_field_name: local, as string: The name of the IP field.
    save_button_id: local, as string: The html ID of the save button.
    """

    add_button_id = "dhcpTip9"
    mac_field_xpath = "//input[@list-mac-index='0']"
    ip_field_name = "reservedIp"
    save_button_id = "dhcpTip14"

    # Find the IP Reservation button and click it
    add_button = find_element(driver, add_button_id, By.ID)
    if add_button is None:
        log_message("Add button was not returned. Adding IP will fail.")
        raise # raises exception to main()
    else:
        add_button.click()
        log_message("Add button clicked.")

    # Find the MAC field and enter the MAC address
    mac_field = find_element(driver, mac_field_xpath, By.XPATH)
    if mac_field is None:
        log_message("MAC Field was not returned. Adding IP will fail.")   
        raise # raises exception to main()
    else:
        mac_field.send_keys(f"{mac_value}")
        log_message("keys sent to MAC field.")

    # Find the IP field and enter the IP address
    ip_field = find_element(driver, ip_field_name, By.NAME)
    if ip_field is None:
        log_message("IP Field was not returned. Adding IP will fail.")
        raise # raises exception to main()
    else:
        ip_field.send_keys(f"{ip_value}")
        log_message("keys sent to IP field.")
    
    # Find the save button and click it
    save_button = find_element(driver, save_button_id, By.ID)
    if save_button is None:
        log_message("Save Button was not returned. Adding IP will fail.")
        raise # raises exception to main()
    else:
        save_button.click()
        log_message("Save button clicked.")

# Function to locate the save successful message
def locate_save_successful(driver):
    save_message_xpath = "//span[contains(text(), 'Data successfully saved.')]"

    if find_element(driver, save_message_xpath, By.XPATH) != None:
        log_message("IP Reservation found - IP Reservation was successful.")
        return
    else:
        log_message(f"IP reservation not found - IP Reservation was not successful.")
        raise # raises exception to main()

# Function to initialize the driver
def initialize_driver():
    # Set the path to the chromedriver executable if needed. I have chromedriver in .venv/scripts folder which also works.
    # driver_path = "C:/Users/andre/Downloads/chromedriver_win32/chromedriver.exe"
    # service = Service(driver_path)
    # If you decide to set the executable path, replace driver = webdriver.Chrome(options=options) with driver = webdriver.Chrome(service=service, options=options)
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# Function to go to a webpage
def go_to_webpage(driver, url):
    try:
        driver.get(url)
        log_message(f"Attempting to access webpage: {url}")
    except Exception as e:
        log_message(f"Could not access webpage: {url} - ERROR: {e}.")
        raise # raises exception to main()

# Main function
def main():
    
    # Set the argument parser
    args = set_arg_parser()

    # Set URL's, get MAC address, IP address as arguments and password from user input
    mac_address = args.mac
    ip_address = args.ip
    username_value = "admin" # default username
    password_value = getpass.getpass("Enter the password of your routers web interface: ")
    web_interface_url = "http://192.168.0.1"
    dhcp_settings_url = "http://192.168.0.1/#/mybox/DHCP"

    # Main logic of code
    try:
        driver = initialize_driver()
        go_to_webpage(driver, web_interface_url)
        attempt_login(driver, username_value, password_value)
        go_to_webpage(driver, dhcp_settings_url)
        add_ip_reservation(driver, mac_address, ip_address)
        locate_save_successful(driver)
    except Exception as e:
        log_message(f"A critical error occurred: {e}. Exiting...")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()



