from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

desired_caps = dict (
    platformName = 'android',
    automationName = 'uiautomator2',
    appPackage = 'com.appiumpro.the_app',
    appActivity = 'com.appiumpro.the_app.MainActivity',
    deviceName = 'Pixel 2',
    udid = 'HT84G1A02727',
    headspinCapture = True
)

capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)
driver = webdriver.Remote(
    'https://dev-us-pao-3.headspin.io:7003/v0/f4f20572809b4dc1855a6bd1ef05e861/wd/hub',
    options=capabilities_options
)
try:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, 'Login Screen'))).click()
    username_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, 'username')))
    password_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'password')
    login_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'loginBtn')
    username_field.send_keys('wrongname')
    password_field.send_keys('wrongpw')
    login_button.click()
    saved_text = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/message"]')
    )).text
    assert 'Invalid login credentials' in saved_text, 'Login alert pop up not found.'
    driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@resource-id="android:id/button1"]').click()
    username_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, 'username')))
    password_field = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'password')
    login_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, 'loginBtn')
    username_field.send_keys('alice')
    password_field.send_keys('mypassword')
    login_button.click()
    logged_in_text = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.TextView[@text="You are logged in as alice"]')
    )).text
    assert 'alice' in logged_in_text, 'User is not logged in.'
    driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.Button').click()
    username_field = wait.until(EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, 'username')))
    assert username_field.is_displayed()
finally:
    driver.quit()
