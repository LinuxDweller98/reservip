# Description: This script reserves a static local IP adress for a given MAC address.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import getpass
import argparse

def attempt_login(driver, username_value, password_value):
    username_field_id = "user"
    password_field_id = "password"
    login_button_id = "button-blue"

    # Find the username field and enter the username
    try:
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, username_field_id))
        )
        print("Username field found.")
        username_field.clear()    
        username_field.send_keys(username_value)
        print("keys sent")
    except Exception as e:
        print("User Field not found. Error message: {e}")

    # Find the password field and enter the password
    try:
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, password_field_id))
        )
        print("Password field found.")
        password_field.send_keys(f"{password_value}")
        print("keys sent")
        password_value = None # clear the password from memory
    except Exception as e:
        print("Password Field not found. Error message: {e}")

    # Find the login button and click it
    try:
        login_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, login_button_id))
        )
        print("Login button found.")
        login_button.click()
        print("Login button clicked.")
    except Exception as e:
        print("Login Button not found. Error message: {e}")

def set_arg_parser():
    parser = argparse.ArgumentParser(description="Reserves a static IP address for a given MAC address through your routers web interface.")
    parser.add_argument('mac', type=str, help='Mac address in format xx:xx:xx:xx:xx:xx')
    parser.add_argument('ip', type=str, help='IP address in format xxx.xxx.xxx.xxx')
    args = parser.parse_args()
    return args

def add_ip_reservation(driver, mac_value, ip_value):
    add_button_id = "dhcpTip9"
    mac_field_xpath = "//input[@list-mac-index='0']"
    ip_field_name = "reservedIp"
    save_button_id = "dhcpTip14"
    # Find the IP Reservation button and click it
    try:
        add_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, add_button_id))
        )
        print("Add Reservation Button found.")
        add_button.click()
        print("Add Reservation Button clicked.")
    except Exception as e:
        print(f"Add Button not found. Error message: {e}")

    # Find the MAC field and enter the MAC address
    try:
        mac_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, mac_field_xpath))
        )
        print("MAC Field found.")
        mac_field.send_keys(f"{mac_value}")
        print("keys sent.")
    except Exception as e:
        print(f"MAC Field not found. Error message: {e}")

    # Find the IP field and enter the IP address
    try:
        ip_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, ip_field_name))
        )
        print("IP Field found.")
        ip_field.send_keys(f"{ip_value}")
        print("keys sent.")
    except Exception as e:
        print(f"IP Field not found. Error message: {e}")

    # Find the save button and click it
    try:
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, save_button_id))
        )
        print("Save Button found.")
        save_button.click()
        print("Save Button clicked.")
    except Exception as e:
        print(f"Save Button not found. Error message: {e}")   

def locate_save_successful(driver):
    save_message_xpath = "//span[contains(text(), 'Data successfully saved.')]"

    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, save_message_xpath))
        )
        print("IP Reservation found - IP Reservation was successful.")
    except Exception as e:
        print(f"IP reservation not found - IP Reservation was not successful. Error message: {e}")


def main():
    
    # Set the argument parser
    args = set_arg_parser()

    # Get MAC address, IP address as arguments and password from user input
    mac_address = args.mac
    ip_address = args.ip
    username_value = "admin" # default username
    password_value = getpass.getpass("Enter the password of your routers web interface: ")

    try:
        driver = webdriver.Chrome()
        driver.get("http://192.168.0.1")
        attempt_login(driver, username_value, password_value)
        driver.get("http://192.168.0.1/#/mybox/DHCP")
        add_ip_reservation(driver, mac_address, ip_address)
        locate_save_successful(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()



