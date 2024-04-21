from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Path to the WebDriver executable (e.g., chromedriver)
webdriver_path = '/path/to/chromedriver'

# Initialize the WebDriver (in this example, using Chrome)
driver = webdriver.Chrome(executable_path=webdriver_path)

# Open a website
driver.get('https://fill.dev/form/login-simple')

# Find an element by its ID and type text into an input field
input_element = driver.find_element_by_id('username')
input_element.send_keys('Python')

# Submit the form
input_element.send_keys(Keys.ENTER)

# Wait for the page to load (you may need to adjust the wait time)
driver.implicitly_wait(10)

# Print the page title
print(driver.title)

# Close the browser
driver.quit()
