 from selenium import webdriver
 from selenium.webdriver.common.by import By
 from selenium.webdriver.support.wait import WebDriverWait
 from selenium.webdriver.support import expected_conditions as EC
 from selenium.webdriver.firefox.options import Options as FirefoxOptions
 
 options = FirefoxOptions()
 options.browser_version = '79.0'
 options.platform_name = 'HS Remote'
 cloud_options = {
     "build": "",
     "name": "",
     "headspin:capture": True,
     "headspin:initialScreenSize": {
         "width": 1920,
         "height": 1080
     },
 }
 options.set_capability('cloud:options', cloud_options)
 
 driver = webdriver.Remote('https://dev-id-jk-0.headspin.io:9095/v0/f4f20572809b4dc1855a6bd1ef05e861/wd/hub', options=options)
 try:
     wait = WebDriverWait(driver, 10)
     driver.get('https://the-internet.herokuapp.com')
     add_remove_link = wait.until(EC.presence_of_element_located(
         (By.LINK_TEXT, 'Add/Remove Elements')
     ))
     add_remove_link.click()
     page_header = wait.until(EC.presence_of_element_located(
         (By.TAG_NAME, 'h3')
     ))
     assert 'Add/Remove Elements' in page_header.text
 
     newDeleteEl = driver.find_elements(By.CLASS_NAME, 'added-manually')
     assert len(newDeleteEl) == 0, 'Unexpected number of new Delete buttons have been found after adding an element'
 
     addElButton = driver.find_element(By.XPATH, '//*[@id="content"]/div/button')
     addElButton.click()
     newDeleteEl = driver.find_elements(By.CLASS_NAME, 'added-manually')
     assert len(newDeleteEl) == 1, 'Unexpected number of new Delete buttons have been found after adding an element'
 
     addElButton.click()
     newDeleteEl = driver.find_elements(By.CLASS_NAME, 'added-manually')
     assert len(newDeleteEl) == 2, 'Unexpected number of new Delete buttons have been found after adding an element'
 
     removeEl = driver.find_element(By.CLASS_NAME, 'added-manually')
     removeEl.click()
     newDeleteEl = driver.find_elements(By.CLASS_NAME, 'added-manually')
     assert len(newDeleteEl) == 1, 'Unexpected number of new Delete buttons have been found after adding an element'
 
     removeEl = driver.find_element(By.CLASS_NAME, 'added-manually')
     removeEl.click()
     newDeleteEl = driver.find_elements(By.CLASS_NAME, 'added-manually')
     assert len(newDeleteEl) == 0, 'Unexpected number of new Delete buttons have been found after adding an element'
 
     driver.get('https://the-internet.herokuapp.com')
 
     dynamic_link = wait.until(EC.presence_of_element_located(
         (By.LINK_TEXT, 'Dynamic Loading')
     ))
     dynamic_link.click()
     page_header = driver.find_element(By.TAG_NAME, 'h3').text
     assert 'Dynamically Loaded Page Elements' in page_header
 
     example2_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Example 2')
     example2_link.click()
     page_header = driver.find_element(By.TAG_NAME, 'h4').text
     assert 'Example 2: Element rendered after the fact' in page_header
 
     start_button = driver.find_element(By.XPATH, '//*[@id="start"]/button')
     start_button.click()
     dynamically_loaded_element = wait.until(EC.presence_of_element_located(
         (By.XPATH, '//*[@id="finish"]/h4')
     ))
     assert 'Hello World!' in dynamically_loaded_element.text
 
     driver.get('https://the-internet.herokuapp.com')
 
     frames_link = wait.until(EC.presence_of_element_located(
         (By.LINK_TEXT, 'Frames')
     ))
     frames_link.click()
     page_header = driver.find_element(By.TAG_NAME, 'h3').text
     assert 'Frames' in page_header
 
     iframe_link = driver.find_element(By.LINK_TEXT, 'iFrame')
     iframe_link.click()
     page_header = driver.find_element(By.TAG_NAME, 'h3').text
     assert 'TinyMCE WYSIWYG' in page_header
 
     file_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div[1]/button[1]/span')
     file_button.click()
     iframe = driver.find_element(By.ID, 'mce_0_ifr')
     driver.switch_to.frame(iframe)
     body = wait.until(EC.presence_of_element_located(
         (By.TAG_NAME, 'body')
     ))
     body.clear()
     body.send_keys('Hello from automation!')
     assert 'Hello from automation!' in body.text
     driver.switch_to.default_content()
 
     driver.get('https://the-internet.herokuapp.com')
 
 finally:
     driver.quit()
