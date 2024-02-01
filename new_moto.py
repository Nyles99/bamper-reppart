import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

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

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

summa = 0
moto = {}


file1 = open("black-list.txt", "r")
while True:
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    url = f"https://bamper.by/zchbu/moto/marka_{line}/"
    moto[line] = url
    # прерываем цикл, если строка пустая
    if not line:
        break
file1.close

with open("moto.json", "a", encoding="utf-8") as file:
    json.dump(moto, file, indent=4, ensure_ascii=False)      

with open('modelubaks.json', encoding="utf-8") as file:
    model_need_list = json.load(file)

moto00_1200 = {}
moto1200 = {}
n=1

for item_text_model, item_href_model in model_need_list.items():
    
    markah = item_text_model
    
    url_zapchast = item_href_model
    driver.get(url=url_zapchast)
    time.sleep(1)

    with open(f"{item_text_model}.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open(f"{item_text_model}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')

    count = soup.find_all("h5", class_="list-title js-var_iCount")
    #print(count)
    for item in count:
        item = str(item)
        if "<b>" in item:
            #print(item)
            num_page = item[item.find("<b>")+3: item.find("</b>")]
            num_page = int(num_page.replace(" ",""))
            summa = summa + num_page
            if num_page > 0 and num_page < 1201:
                page = int(num_page / 20) + 1
                moto00_1200[url_zapchast] = page
            elif num_page > 1200:
                page = int(num_page / 20) + 1
                moto1200[url_zapchast] = page

    os.remove(f"{item_text_model}.html") 

with open("moto00_1200.json", "a", encoding="utf-8") as file:
    json.dump(moto00_1200, file, indent=4, ensure_ascii=False)

with open("moto1200.json", "a", encoding="utf-8") as file:
    json.dump(moto1200, file, indent=4, ensure_ascii=False)


print(summa)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие")