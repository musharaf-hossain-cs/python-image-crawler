from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
import os
from pathlib import Path
import requests as rq
# from bs4 import *
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import base64

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver = webdriver.Chrome(service=Service("C:\\PythonSeleniumDrivers\\chromedriver_win32\\chromedriver.exe"))

def make_url(actor):
    return 'https://www.google.com/search?q=' + actor + '+front+facing' + '&source=lnms&tbm=isch'

def find_links_from_google(driver, url, delay, max_images):
    def scroll_down(driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(delay) 
    
    driver.get(url)

    image_urls = []

    start = 0

    while len(image_urls) < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for thumbnail in thumbnails[start:]:
            try:
                thumbnail.click()
                time.sleep(delay)
            except:
                continue

            actual_images = driver.find_elements(By.CLASS_NAME, 'n3VNCb')

            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.append(actual_image.get_attribute('src'))
                    print(f'Found {len(image_urls)} images')
                start += 1
            
            if len(image_urls) >= max_images:
                break
    
    return image_urls


def downloadImages(links, directory, name):
    path = Path(directory)
    if not os.path.exists(directory):
        path.mkdir(parents=True, exist_ok=True)
    for link in links:
        try:
            r2 = rq.get(link)
        except:
            print(link)
            continue
        with open(directory + '/' + name + '_' + str(links.index(link)) + '.jpg', 'wb') as f:
            f.write(r2.content)

# actor = 'Shah Rukh Khan'
actors = [
            'Shah Rukh Khan', 
            'Salman Khan', 
            'Amitabh Bacchan', 
            'Priyangka Chopra', 
            'Deepika Padukone', 
            'Ranbir Kapoor', 
            'Katrina Kaif', 
            'Anushka Sharma'
        ]

for actor in actors:
    url = make_url(actor)
    image_urls = find_links_from_google(driver, url, 2, 10)
    # print(image_urls)
    downloadImages(image_urls, './images/' + actor.replace(' ', '_'), actor.replace(' ', '_'))
