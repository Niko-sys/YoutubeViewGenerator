from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from threading import Thread
import threading
import time, random
'''
 pip installs
    - selenium
    - webdriver
'''

playlist_url = ""
# 10 songs of 3min average
length_playlist = 16 * 3 * 60
amount_browsers = 7

class YouTube:

    delay = 3

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.browser.get("https://www.youtube.com")
        time.sleep(3)
        threading.Timer(10.0, self.dismissOverlays).start()

    def openPlayList(self, url):
        self.browser.get(url)

    def search(self, query):
        words = query.split(" ")
        true_query = ""
        for word in words:
            true_query += "+{}".format(word)

        url = "https://www.youtube.com/results?search_query={}".format(true_query[1:])
        self.browser.get(url)
        time.sleep(3)

    def openVideo(self):
        print("opening video")
        xpath = '//*[@id="video-title"]'
        WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = self.browser.find_elements_by_xpath(xpath)
        random.shuffle(elements)
        for element in elements:
            label = element.get_attribute("aria-label")
            print(label)
            if 'Teeti' in label:
                element.click()

                return self.openVideo()

        print("Ending videos")
        return

    def dismissOverlays(self):
        try:
            xpath_deny = '//*[@id="dismiss-button"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath_deny)))
            btn_deny = self.browser.find_element_by_xpath(xpath_deny)
            btn_deny.click()
        except Exception as e:
            pass

        try:
            xpath_iframe = '//*[@id="dialog"]/iframe'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
            self.browser.switch_to.frame(self.browser.find_element_by_xpath(xpath_iframe))

            xpath_acceptcookies = '//*[@id="introAgreeButton"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath_acceptcookies)))
            btn_accept = self.browser.find_element_by_xpath(xpath_acceptcookies)
            btn_accept.click()
        except Exception as e:
            pass

        # Continue watching popup
        try:
            xpath = '//*[@id="confirm-button"]'
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            btn_accept = self.browser.find_element_by_xpath(xpath)
            btn_accept.click()
        except:
            pass

def handler():
    session = YouTube()
    session.openPlayList(playlist_url)
    time.sleep(length_playlist)
    session.browser.quit()
    return Thread(target=handler).start()


if __name__ == '__main__':
    for index in range(amount_browsers):
        Thread(target=handler).start()
        time.sleep(30)

    #session.search("blzbla")
    #session.openVideo()
