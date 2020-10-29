from selenium import webdriver
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
        self.dismissOverlays(start_delay=15)
        thread = threading.Timer(10.0, self.dismissOverlays)
        thread.daemon = True
        thread.start()


    def search(self, query):
        words = query.split(" ")
        true_query = ""
        for word in words:
            true_query += "+{}".format(word)

        url = "https://www.youtube.com/results?search_query={}".format(true_query[1:])
        self.browser.get(url)
        time.sleep(3)

    def openVideo(self, value, sleep):
        print("opening video")
        xpath = '//*[@id="video-title"]'
        WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = self.browser.find_elements_by_xpath(xpath)[1:]
        #random.shuffle(elements)
        for element in elements:
            label = element.get_attribute("aria-label")
            if not label:
                continue

            print(label)
            if value in label:
                time.sleep(sleep)
                try:
                    element.click()
                except:
                    return self.openVideo(value, 0)

                parts = label.split(' ')
                minutes, seconds = 0, 0
                for index, part in enumerate(parts):
                    try:
                        if 'sec' in part:
                            seconds += int(part[index-1])
                        if 'min' in part:
                            minutes += int(part[index-1])
                    except Exception as e:
                        print(e)

                # Sleep length of video
                new_sleep = (minutes*60) + seconds

                return self.openVideo(value, new_sleep)

        print("Ending videos")
        return

    def dismissOverlays(self, start_delay=3):
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

if __name__ == '__main__':
    playlist_url = ""
    length_playlist = 11 * 3 * 60
    amount_browsers = 7

    sessions = []

    for index in range(amount_browsers):
        session = YouTube()
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



    '''
    session = YouTube()
    session.search("short video")
    session.openVideo(value='', sleep=0)
    '''



