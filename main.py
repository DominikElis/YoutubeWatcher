import threading
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

on = True
actions = None


def anti_autopause():
    while on:
        randi = randint(30, 500)
        time.sleep(randi)

        actions.send_keys('m')
        actions.perform()
        actions.reset_actions()


if __name__ == '__main__':
    # random start
    # time.sleep(randint(500, 1000))

    # mute sounds
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")
    # load drivers
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.set_window_size(1920,1090)
    actions = ActionChains(driver)
    # call YT Channel url
    driver.get("https://www.youtube.com/channel/UCxowImwR27S6dUPkzxaijWw")
    # accept cookies
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Alle akzeptieren']"))).click()
    # driver.implicitly_wait(10)
    # play all uploads
    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "ALLE "))).click()
    # continue_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'ALLE').click()
    driver.implicitly_wait(10)

    # disable autopause (mute and unmute every x seconds)
    thread = threading.Thread(target=anti_autopause)
    thread.start()

    while True:
        # skip ad
        try:
            ad_text = driver.find_element(By.XPATH, "//div[@class='ytp-ad-text ytp-ad-skip-button-text']")
            if ad_text.get_attribute('innerHTML') != "":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='ytp-ad-skip-button ytp-button']"))).click()
        except:
            pass

        playlist_counters = None
        playlist_counter = driver.find_elements(By.XPATH,
                                                "//span[contains(@class, 'index-message style-scope ytd-playlist-panel-renderer')]")
        for playlist in playlist_counter:
            if playlist.get_attribute('innerHTML') != "":
                playlist_counters = playlist.get_attribute('innerHTML').split(" / ")
        # print(playlist_counter)

        # select low quality
        # time.sleep(5)  # you can adjust this time
        # driver.find_element(By.CSS_SELECTOR,'button.ytp-button.ytp-settings-button').click()
        # driver.find_element(By.XPATH,"//div[contains(text(),'Quality')]").click()
        #
        # time.sleep(2)  # you can adjust this time
        # quality = driver.find_element_by_xpath("//span[contains(string(),'144p')]")
        # quality.click()

        # get current time
        current_time_counter = None
        current_times = driver.find_elements(By.XPATH,
                                             "//span[contains(@class, 'ytp-time-current')]")  # [1].get_attribute('innerHTML')
        for current_time in current_times:
            if current_time.get_attribute('innerHTML') != "":
                current_time_counter = current_time.get_attribute('innerHTML')  # .split(" / ")

        # get time duration
        time_duration_counter = None
        time_durations = driver.find_elements(By.XPATH,
                                              "//span[contains(@class, 'ytp-time-duration')]")  # [1].get_attribute('innerHTML')
        for time_duration in time_durations:
            if time_duration.get_attribute('innerHTML') != "":
                time_duration_counter = time_duration.get_attribute('innerHTML')  # .split(" / ")

        time_counter = current_time_counter + " / " + time_duration_counter
        # print(time_counter)
        if playlist_counters[0] == playlist_counters[1] and playlist_counters[0] != "NaN" and playlist_counters[
            1] != "NaN":  # last video
            # disable autoplay if exists
            try:
                driver.find_element(By.XPATH, "//button[@aria-label='Autoplay aktiviert']")
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Autoplay aktiviert']"))).click()
            except:
                pass

            if time_counter != "NaN / NaN" and current_time_counter == time_duration_counter:  # video ends
                print("end")
                on = False
                driver.quit()
                break
