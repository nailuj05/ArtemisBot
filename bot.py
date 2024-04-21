import configparser
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ----------- ARGS -------------
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments')
    parser.add_argument('repo_path', type=str, help='Path to the repository (locally)')
    parser.add_argument('artemis_url', type=str, help='URL of the Artemis server')
    parser.add_argument('-p', type=int, default=100, help='Desired percentage (default: 100%)')
    return parser.parse_args()

args = parse_arguments()

# ---------- CONFIG ------------

config = configparser.ConfigParser()
config.read("config.ini")

print(f"Login: {config["Auth"]["Username"]}")

webdriver_path = config["Browser"]["PathToDriver"]

browser = config["Browser"]["Browser"]

def CreateWebDriver(browser):
    if(browser == "Chrome"):
        return webdriver.Chrome()
    elif(browser == "Firefox"):
        return webdriver.Firefox()
    elif(browser == "Safari"):
        return webdriver.Safari()
    else:
        raise ValueError("Unsupported Browser Name")

driver = CreateWebDriver(browser)

# Open Artemis for Login
driver.get('https://artemis.cit.tum.de')

username = driver.find_element(By.ID, 'username')
username.send_keys(config["Auth"]["Username"])

password = driver.find_element(By.ID, 'password')
password.send_keys(config["Auth"]["Password"])

remember = driver.find_element(By.ID, "rememberMe")
remember.click()

login = driver.find_element(By.ID, "login-button")
login.click()

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(1000)

# Print the page title
print(driver.title)

# Close the browser
while True:
    key = input("Press a key (q to quit): ")
    if key.lower() == 'q':
        driver.quit()
        break
