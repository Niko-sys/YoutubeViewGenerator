from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import threading
import time, random
'''
 pip installs
    - selenium
    - webdriver
'''

class YouTube:

    delay = 3

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        #self.browser = webdriver.Firefox()

    def openPlayList(self, url):
        self.browser.get(url)
        thread = threading.Timer(10.0, self.dismissOverlays)
        thread.start()

    def search(self, query):
        words = query.split(" ")
        true_query = ""
        for word in words:
            true_query += "+{}".format(word)

        url = "https://www.youtube.com/results?search_query={}".format(true_query[1:])
        self.browser.get(url)
        time.sleep(3)
        threading.Timer(10.0, self.dismissOverlays).start()

    first_run = True

    def openVideo(self, value, sleep):
        xpath = '//*[@id="video-title"]'
        if self.first_run:
            elements = self.browser.find_elements_by_xpath(xpath)
            self.first_run = False
        else:
            elements = self.browser.find_elements_by_xpath(xpath)[2:]

        for _ in range(4):
            print(len(elements))
            if len(elements) == 0:
                time.sleep(10)
                elements = self.browser.find_elements_by_xpath(xpath)

        random.shuffle(elements)
        for element in elements:

            label = element.get_attribute("aria-label")

            if not label:
                print("No label")
                continue

            if value in label:
                location = element.location
                size = element.size
                if location["x"] == 0:
                    print("Location 0")
                    continue

                print(location)
                print(size)

                try:
                    sleep -= 20
                    if sleep < 0:
                        sleep = 0
                    print("sleeping for {}".format(sleep))
                    time.sleep(sleep)
                    print("Will click " + label)
                    try:
                        element.click()
                    except:
                        # there is some kind of popup
                        time.sleep(12)
                        try:
                            element.click()
                        except ElementClickInterceptedException:
                            continue

                except Exception as e:
                    print(e)
                    exit(1)

                sleep = 0

                try:
                    minute_text = label.split(' minute')[-2].split(' ')[-1]
                    sleep += int(minute_text) * 60
                except:
                    pass

                try:
                    second_text = label.split(' second')[-2].split(' ')[-1]
                    sleep += int(second_text)
                except:
                    pass

                return True, sleep

        return False, sleep

    def dismissOverlays(self, start_delay=3):
        print("Dismissing")

        try:
            xpath_deny = '//*[@id="dismiss-button"]'
            WebDriverWait(self.browser, start_delay).until(EC.presence_of_element_located((By.XPATH, xpath_deny)))
            btn_deny = self.browser.find_element_by_xpath(xpath_deny)
            btn_deny.click()
        except Exception as e:
            pass

        try:
            xpath_iframe = '//*[@id="dialog"]/iframe'
            WebDriverWait(self.browser, start_delay).until(EC.presence_of_element_located((By.XPATH, xpath_iframe)))
            self.browser.switch_to.frame(self.browser.find_element_by_xpath(xpath_iframe))

            xpath_acceptcookies = '//*[@id="introAgreeButton"]'
            WebDriverWait(self.browser, start_delay).until(EC.presence_of_element_located((By.XPATH, xpath_acceptcookies)))
            btn_accept = self.browser.find_element_by_xpath(xpath_acceptcookies)
            btn_accept.click()
            self.browser.switch_to.default_content()

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

def startSearch():
    while True:
        search_query = ""

        session = YouTube()
        session.search(search_query)

        start = time.time()
        max_duration = 25 * 60  # 25 minuten

        sleep = 0

        while True:
            try:
                boolean, sleep = session.openVideo(value='Teeti', sleep=sleep)
                time.sleep(5)
                if not boolean:
                    print("Session openvideo returned false")
                    # so wait till video hs been watched before going away
                    time.sleep(sleep)
                    break
                print("Succesfully watched a video")
                now = time.time()
                # check if longer online than necessary
                if int(now - start) > max_duration:
                    print("time exceeded")
                    break
            except:
                break

        session.browser.quit()
        print("Need a new stream")


if __name__ == '__main__':

    '''amount_browsers = 7

    for _ in range(amount_browsers):
        threading.Thread(target=startSearch).start()
        time.sleep(35)

    while True:
        pass

    exit(0)'''

    playlist_url = "" #or videourl"
    length_playlist = 3 * 60 # 3 minutes
    amount_browsers = 8

    while True:
        sessions = []

        try:
            for index in range(amount_browsers):
                try:
                    # sometimes crashes when connection to internet is lost
                    session = YouTube()
                except:
                    continue
                session.openPlayList(playlist_url)
                sessions.append(session)
                time.sleep(20)

            while True:

                time.sleep(length_playlist)

                sessions_copy = sessions.copy()

                for session in sessions_copy:
                    sessions.remove(session)
                    try:
                        session.browser.quit()
                    except:
                        pass
                    session = YouTube()
                    session.openPlayList(playlist_url)
                    sessions.append(session)
                    time.sleep(20)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            time.sleep(60)



