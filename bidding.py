from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import csv

#date = '191220212359'
SUBMITTED_BIDS_FNAME = 'submitted_bids.pkl'

tab_dict = {'3 days': 2, '7 days': 3, 'month': 4}


def get_new_bids(fname):
    # csv must not have headers, have URLS in column A and amounts in ETH in columnm B
    f = open(fname)
    csv_f = csv.reader(f)

    urls = []
    amounts = []

    for row in csv_f:
        urls.append(row[0])
        amounts.append(row[1])
    return urls, amounts


def place_bid(driver, url, bid, expiry='3 days'):
    if expiry not in tab_dict.keys():
        print(f'Invalid expiry date: {expiry}')
        return
    print(f'Placing a bid of {bid} on {url}')
    driver.get(url)

    # Wait for wallet to connect
    try:
        clickmetamask = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//img[@class="Image--image"]'))
        )
    except:
        print("Error: Wallet did not connect in time: " + url)
        return False

    try:
        makeoffer = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Make offer")]'))
        )
    except:
        print("Error: Make offer did not load in time: " + url)
        return False
    new_scroll = makeoffer.location['y']
    driver.execute_script(f"window.scrollTo(0, {new_scroll-200});")
    time.sleep(1)
    makeoffer.click()

    try:
        amountinput = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder = "Amount"]'))
        )
    except:
        print("Error: Amount box did not load: " + url)
        return False

    time.sleep(0.5)

    for character in bid:
        actions = ActionChains(driver)
        actions.send_keys(character)
        actions.perform()
        time.sleep(0.1)

    # Set expiry date
    for x in range(tab_dict[expiry]):
        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.1)

    ActionChains(driver).send_keys(Keys.RETURN).perform()

    # for character in date:
    # 	actions = ActionChains(driver)
    # 	actions.send_keys(character)
    # 	actions.perform()
    # 	time.sleep(0.1)

    for x in range(9):
        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.1)

    ActionChains(driver).send_keys(Keys.RETURN).perform()

    try:
        makeyouroffer = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Make your offer')]"))
        )
    except:
        print("Error: Sign button did not load: " + url)
        return False

    for y in range(3):
        ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(0.1)

    ActionChains(driver).send_keys(Keys.RETURN).perform()

    time.sleep(2)
    if len(driver.window_handles)<2:
        print('Error: metamask sign page did not load')
        return False

    main_page = driver.current_window_handle

    for handle in driver.window_handles:
        if handle != main_page:
            metamasksignpage = handle

    driver.switch_to.window(metamasksignpage)

    # wait for sign button to load:
    try:
        sign = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Sign')]"))
        )
        sign.click()
    except:
        # If confirmation not received in timeframe, the url is printed
        print("Error: Metammask Sign Button didn't load:" + url)
        return False

    # driver.switch_to.window(driver.window_handles[4])

    for window in driver.window_handles:
        driver.switch_to.window(window)
        if re.search(url, driver.current_url):
            break

    # wait for confirmation of signature with opensea:
    try:
        confirmation = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Your offer was submitted successfully!')]"))
        )
    except:
        # If confirmation not received in timeframe, the url is printed
        print("Error: No confirmation" + url)
        return False
    print('SUCCESSFULLY PLACED BID ON '+url)
    return True