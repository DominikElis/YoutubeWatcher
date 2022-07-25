import time
from random import randint
from threading import Thread

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver import ActionChains
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
    #driver.implicitly_wait(10)
    # play all uploads
    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "ALLE "))).click()
    #continue_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'ALLE').click()
    driver.implicitly_wait(10)

    while True:
        # disable autopause (mute and unmute every x seconds)
        randi = randint(10, 30)
        time.sleep(randi)
        actions = ActionChains(driver)
        actions.send_keys('m')
        actions.perform()

        randi = randint(15, 35)
        time.sleep(randi)
        actions = ActionChains(driver)
        actions.send_keys('m')
        actions.perform()


        # autopause_button = driver.find_element(By.XPATH, "//yt-formatted-string[]")
        # if autopause_button.get_attribute('innerHTML')== "Video angehalten. Wiedergabe fortsetzen?":
        #     autopause_button = driver.find_element(By.XPATH, "//tp-yt-paper-button[@aria-label='JA']")
        #     autopause_button.click()
        # get current playlist counter + playlist count

        playlist_counters = None
        playlist_counter = driver.find_elements(By.XPATH,"//span[contains(@class, 'index-message style-scope ytd-playlist-panel-renderer')]")
        for playlist in playlist_counter:
            if playlist.get_attribute('innerHTML') != "":
                playlist_counters = playlist.get_attribute('innerHTML').split(" / ")
        #print(playlist_counter)


        # get current time
        current_time_counter = None
        current_times = driver.find_elements(By.XPATH,"//span[contains(@class, 'ytp-time-current')]")#[1].get_attribute('innerHTML')
        for current_time in current_times:
            if current_time.get_attribute('innerHTML') != "":
                current_time_counter = current_time.get_attribute('innerHTML')#.split(" / ")


        # get time duration
        time_duration_counter = None
        time_durations = driver.find_elements(By.XPATH, "//span[contains(@class, 'ytp-time-duration')]")#[1].get_attribute('innerHTML')
        for time_duration in time_durations:
            if time_duration.get_attribute('innerHTML') != "":
                time_duration_counter = time_duration.get_attribute('innerHTML')#.split(" / ")


        time_counter = current_time_counter+" / "+time_duration_counter
        #print(time_counter)
        if  playlist_counters[0] ==  playlist_counters[1] and playlist_counters[0] != "NaN" and playlist_counters[1] != "NaN":   # last video
            # disable autoplay if exists
            driver.implicitly_wait(5)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Autoplay aktiviert']"))).click()

            if  time_counter != "NaN / NaN" and current_time == time_duration: # video ends
                print("end")
                break







