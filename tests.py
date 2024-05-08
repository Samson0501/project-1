from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the driver variable globally
driver: WebDriver = None


def initialize_browser():
    global driver
    chrome_driver_path = "./drivers/chromedriver.exe"
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)


def navigate_to_url(app_url):
    driver.get(app_url)


def login_using_creds(user_name, password):
    web_driver_wait = WebDriverWait(driver, 10)
    user_name_element = web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='username' and @placeholder='Username']"))
    )
    user_name_element.send_keys(user_name)

    password_element = web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='password' and @placeholder='Password']"))
    )
    password_element.send_keys(password)

    submit_button = web_driver_wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    submit_button.click()

    dashboard_element = web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
    )
    assert dashboard_element.is_displayed() == True


initialize_browser()
navigate_to_url("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
login_using_creds("Admin", "admin123")

# Close the browser
driver.quit()
