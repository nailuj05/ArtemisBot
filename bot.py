import time
import argparse
import configparser
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
driver.get(args.artemis_url)

wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.current_url != "https://artemis.ase.in.tum.de")

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

print(driver.title)

# Wait for redirect back to exercise page
wait = WebDriverWait(driver, 10)
wait.until_not(lambda driver: driver.title == "Welcome to Artemis")

def main_loop():
    while(True):
        try:
            result_score = driver.find_element(By.ID, "result-score")
            percentage = result_score.find_element(By.TAG_NAME, "span")
            p = int(percentage.text.replace("%", ""))

            if(p >= int(args.percentage)):
                print(f"Target percentage reached!")
                break
            
            # Git push here

        finally:
            # sleep and wait
            time.sleep(5)

try:
    main_loop()
finally:
    driver.close()


'''
# Close the browser
while True:
    key = input("Press a key (q to quit): ")
    if key.lower() == 'q':
        driver.quit()
        break
'''
