import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    #mute sounds
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    # load drivers
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(service=Service(),options=chrome_options)
    # call YT Channel url
    driver.get("https://www.youtube.com/channel/UCxowImwR27S6dUPkzxaijWw")
    # accept cookies
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Alle akzeptieren']"))).click()
    # play all uploads
    continue_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'ALLE')
    continue_link.click()

    while True:
        # disable autoplay if exists
        driver.implicitly_wait(15)
        # get current playlist counter + playlist count
        playlist_counter = driver.find_elements(By.XPATH,"//span[contains(@class, 'index-message style-scope ytd-playlist-panel-renderer')]")[1].get_attribute('innerHTML')
        #print(playlist_counter)
        playlist_counters = playlist_counter.split(" / ")

        # get current time
        current_time = driver.find_elements(By.XPATH,"//span[contains(@class, 'ytp-time-current')]")[1].get_attribute('innerHTML')

        # get time duration
        time_duration = driver.find_elements(By.XPATH, "//span[contains(@class, 'ytp-time-duration')]")[1].get_attribute('innerHTML')

        time_counter = current_time+" / "+time_duration

        if  playlist_counters[0] ==  playlist_counters[1] and playlist_counter != "NaN / NaN":   # last video
            # disable autoplay if exists
            driver.implicitly_wait(15)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Autoplay aktiviert']"))).click()

            if  time_counter != "NaN / NaN" and current_time == time_duration: # video ends
                print("end")
                break







