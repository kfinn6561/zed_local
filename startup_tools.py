import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver_path=os.environ['CHROMEDRIVER_PATH']
mnemonic = os.environ['METAMASK_PHRASE']
metamask_extension_path=os.environ['METAMASK_EXTENSION_PATH']
metamask_password=os.environ['METAMASK_PASSWORD']

def initilise_driver():
    chrome_options = Options()
    chrome_options.add_argument(f'load-extension={metamask_extension_path}')
    chrome_options.add_argument("window-size=1000,800")
    print('starting driver')
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options) #launch browser
    
    while len(driver.window_handles)<2:
        time.sleep(1)

    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return driver

def login_metamask(driver):
    driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/create-password/import-with-seed-phrase")

    #This waits for the element of interest to load, and quits the browser if it doesn't load within 10 seconds.
    try:
        recoveryphrase = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Paste Secret Recovery Phrase from clipboard"]'))
        )
    except:
        print("recoveryphrase error")

    #Complete the login form
    recoveryphrase.send_keys(mnemonic)

    newpassword = driver.find_element_by_id("password")
    newpassword.send_keys(metamask_password)

    confirmpassword = driver.find_element_by_id("confirm-password")
    confirmpassword.send_keys(metamask_password)

    tandcs = driver.find_element_by_class_name("first-time-flow__terms")
    tandcs.click()

    importbtn = driver.find_element_by_class_name("first-time-flow__button")
    importbtn.click()
    time.sleep(5)

def connect_to_opensea(driver):
    driver.get("https://opensea.io/")
    time.sleep(5)
    try:
        burger_menu = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/nav/ul/li/button/i')
        burger_menu.click()
        wallet=driver.find_element_by_xpath('//*[contains(text(), "Connect wallet")]')
    except:
        wallet=driver.find_element_by_xpath('//*[contains(text(), "account_balance_wallet")]')
    

    try:
        wallet = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Connect wallet")]'))
        )
    except:
        driver.quit()
        print("Error: wallet button did not load")

    wallet.click()

    try:
        clickmetamask = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "MetaMask")]'))
        )
    except:
        driver.quit()
        print("Error: MetaMask option did not load")

    time.sleep(1)
    clickmetamask.click()

    time.sleep(5) #Give time for the metamask page to load
    driver.switch_to.window(driver.window_handles[-1])

    try:
        nextbtn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Next")]'))
            )
        nextbtn.click()
    except:
        print("Error: nextbtn did not load")

    try:
        connectbtn = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-primary'))
        )
    except:
        print("Error: connectbtn did not load")

    connectbtn.click()

    time.sleep(10)
    driver.switch_to.window(driver.window_handles[0])