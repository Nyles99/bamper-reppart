import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time
import random

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument("start-maximized") # // https://stackoverflow.com/a/26283818/1689770
options.add_argument("enable-automation")#  // https://stackoverflow.com/a/43840128/1689770
#options.add_argument("--headless")#  // only if you are ACTUALLY running headless
options.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
options.add_argument("--enable-javascript")

#options.add_argument("--proxy-server=31.204.2.182:9142")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.implicitly_wait(20)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

url = "https://rrr.lt/ru"

req = requests.get(url, headers=headers)
src = req.text

soup = BeautifulSoup(src, 'html.parser')

marka_need_list = {}
model_need_list = {}


all_mark_models = soup.find_all("option")
#print(all_mark_models)
for item in all_mark_models:
    item = str(item)
    if "option-car-manufacturer" in item:
        marka = item[item.find('">')+3 : item.find('</option>')-1].replace("  ","").replace("\n","")
        href_marka = item[item.find("value=")+7 : item.find('">')]
        print(marka, href_marka)

        driver.get(url=url)
        time.sleep(5)
        marka_input = driver.find_element(By.CLASS_NAME, "select2-search__field")
        marka_input.clear()
        marka_input.send_keys(marka)
        marka_input.send_keys(Keys.ENTER)
        time.sleep(5)
#<input class="select2-search__field" type="search" tabindex="0" autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false" role="textbox">
driver.close()
driver.quit(0)
