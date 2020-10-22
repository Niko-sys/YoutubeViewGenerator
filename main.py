from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Thread
import time

max_wait = 20

# insert url of playlist or video down below
playlist_url = ""

# insert length of video / playlist in seconds (+ take 1 min margin)
length_playlist = 7 * 3 * 60 # for example: playlist contained 7 songs of 3 minutes

# Amount of simultanious 'viewers' you want to have
amount_browsers = 5


def operateBrowser():
    try:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browsers.append(browser)
        browser.get(playlist_url)
    except:
        return

    # dismiss overlays
    try:
        xpath_deny = '//*[@id="dismiss-button"]'
        WebDriverWait(browser, max_wait).until(EC.presence_of_element_located((By.XPATH, xpath_deny)))
        btn_deny = browser.find_element_by_xpath(xpath_deny)
        btn_deny.click()
    except:
        pass

    try:
        xpath_iframe = '//*[@id="dialog"]/iframe'
        WebDriverWait(browser, max_wait).until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
        browser.switch_to.frame(browser.find_element_by_xpath(xpath_iframe))

        xpath_acceptcookies = '//*[@id="introAgreeButton"]'
        WebDriverWait(browser, max_wait).until(EC.presence_of_element_located((By.XPATH, xpath_acceptcookies)))
        btn_accept = browser.find_element_by_xpath(xpath_acceptcookies)
        btn_accept.click()
    except:
        pass

    time.sleep(length_playlist)

    browser.quit()
    return


while True:
    browsers = []

    for index in range(amount_browsers):
        Thread(target=operateBrowser).start()

    time.sleep(length_playlist)
