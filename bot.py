import sys
import time
import argparse
import subprocess
import configparser
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ----------- ARGS -------------
def parse_arguments():
    parser = argparse.ArgumentParser(description='Artemis Commit Bot Help')
    parser.add_argument('repo_path', type=str, help='Path to the repository (locally)')
    parser.add_argument('artemis_url', type=str, help='URL of the Artemis server')
    parser.add_argument('-p', '--percentage', type=int, default=100, help='Desired percentage (default: 100)')
    return parser.parse_args()

args = parse_arguments()

# ---------- CONFIG ------------

config = configparser.ConfigParser()
config.read("config.ini")

print(f"Login: {config["Auth"]["Username"]}")

webdriver_path = config["Browser"]["PathToDriver"]

browser = config["Browser"]["Browser"]

def CreateWebDriver(browser):
    if browser == "Chrome":
        return webdriver.Chrome()
    elif browser == "Firefox":
        return webdriver.Firefox()
    elif browser == "Safari":
        return webdriver.Safari()
    else:
        raise ValueError("Unsupported Browser Name")

driver = CreateWebDriver(browser)

# ----------- ARTEMIS LOGIN -----------
driver.get(args.artemis_url)

wait = WebDriverWait(driver, 20)
wait.until(lambda driver: driver.current_url != "https://artemis.ase.in.tum.de")

username = driver.find_element(By.ID, 'username')
username.send_keys(config["Auth"]["Username"])

password = driver.find_element(By.ID, 'password')
password.send_keys(config["Auth"]["Password"])

remember = driver.find_element(By.ID, "rememberMe")
remember.click()

login = driver.find_element(By.ID, "login-button")
login.click()

driver.implicitly_wait(1000)

print(driver.title)

# Wait for redirect back to exercise page
wait = WebDriverWait(driver, 20)
wait.until_not(lambda driver: driver.title == "Welcome to Artemis")

# -----------------------------------------------------------

# Just for selenium debugging (hightlights the element in the browser)
def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(3)
    apply_style(original_style)

def get_remote_url():
    command = 'git remote -v'

    result = subprocess.run(command, cwd=args.repo_path, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        return(result.stdout.split('\n')[0].split('\t')[1].split(' ')[0])
    else:
        print("Something's wrong with your git:")
        print(result.stderr)
        raise TimeoutError("git remote -v failed")


def commit_and_push_empty(remote_url):
    command = f'git commit --allow-empty -am "Build" \
        && git push {remote_url.replace("@", f':{quote(config["Auth"]["Password"])}@')} main'

    result = subprocess.run(command, cwd=args.repo_path, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("Committed successfully")
        # print("Output:")
        # print(result.stdout)
    else:
        print("Command failed")
        print(result.stderr)

def main_loop(remote_url):
    while(True):
        try:
            result_score = driver.find_element(By.CLASS_NAME, "tab-bar-exercise-details")
            percentage = result_score.find_element(By.XPATH, ".//span[contains(text(), '%')]")
            p = int(percentage.text.replace("%", ""))
            
            highlight(percentage)

            if p >= int(args.percentage):
                print(f"Target percentage reached!")
                break
            
            commit_and_push_empty(remote_url)

        finally:
            # sleep and wait
            time.sleep(10)


# ------------ MAIN LOOP ------------------

remote_url = get_remote_url()
print(f"Remote URL: {remote_url}")

try:
    main_loop(remote_url)
finally:
    driver.close()
