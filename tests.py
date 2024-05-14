from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the driver variable globally
driver: WebDriver = None
app_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


def initialize_browser():
    global driver
    chrome_driver_path = "./drivers/chromedriver.exe"
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()


def navigate_to_url(app_url):
    driver.get(app_url)


def login(user_name, password):
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


def navigate_to_PIM_module():
    web_driver_wait = WebDriverWait(driver, 10)
    web_driver_wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='PIM']"))
    ).click()


# TC_Login_01
def login_using_creds(user_name, password):
    initiate()
    login(user_name, password)
    web_driver_wait = WebDriverWait(driver, 10)
    dashboard_element = web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
    )
    assert dashboard_element.is_displayed() == True
    tearDown()


# TC_Login_02
def login_using_invalid_creds(user_name, password):
    initiate()
    login(user_name, password)
    web_driver_wait = WebDriverWait(driver, 10)
    web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()='Invalid credentials']"))
    )
    tearDown()


# TC_PIM_02
def edit_existing_employee():
    initiate()
    login("Admin", "admin123")
    navigate_to_PIM_module()
    web_driver_wait = WebDriverWait(driver, 10)
    web_driver_wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "oxd-table-card"))
    )
    # Click on first employee in PIM
    driver.find_elements(By.CLASS_NAME, "oxd-table-card")[0].click()
    employee_name = web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='First Name']"))
    )
    employee_name.clear()
    employee_name.send_keys("New employee name")
    driver.find_elements(By.XPATH, "//*[@type='submit']")[0].click()
    web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()='Successfully Updated']"))
    )
    tearDown()


# TC_PIM_03
def delete_existing_employee():
    initiate()
    login("Admin", "admin123")
    navigate_to_PIM_module()
    web_driver_wait = WebDriverWait(driver, 10)
    # Deleting first employee
    web_driver_wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".bi-trash"))
    )[0].click()
    web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()='Are you Sure?']"))
    )
    driver.find_element(By.XPATH, "//*[text()=' Yes, Delete ']").click()
    web_driver_wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[text()='Successfully Deleted']"))
    )
    tearDown()


def initiate():
    initialize_browser()
    navigate_to_url(app_url)


def tearDown():
    driver.quit()


login_using_creds("Admin", "admin123")
login_using_invalid_creds("asfsad", "adsfsdfs")
edit_existing_employee()
delete_existing_employee()
