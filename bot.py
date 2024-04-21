from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Path to the WebDriver executable (e.g., chromedriver)
webdriver_path = '/home/julian/.cargo/bin/geckodriver'

# Initialize the WebDriver (in this example, using Chrome)
driver = webdriver.Firefox()

# Open a website
driver.get('https://artemis.cit.tum.de/courses/329/exercises/13369')

# Find an element by its ID and type text into an input field
input_element = driver.find_element(By.ID, 'search')
input_element.send_keys('BOTTED')

# Submit the form
# input_element.send_keys(Keys.ENTER)

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(1000)

# Print the page title
print(driver.title)

# Close the browser
while True:
    key = input("Press a key (q to quit): ")
    if key.lower() == 'q':
        driver.quit()
