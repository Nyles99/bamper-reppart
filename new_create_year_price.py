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


proxy = input("Введи прокси в формате логин:пароль@46.8.158.109:54376 - ")
ip = proxy[proxy.find("@")+1 : ]
print(ip)

proxies = {
    'http': f'{proxy}',
    'https': f'{proxy}'
}

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

options.add_argument(f"--proxy-server={ip}")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})
url = "https://bamper.by/catalog/modeli/"
driver.get(url=url)
time.sleep(30)

#http://dmUq5yXN:gwR4xvLA@85.142.145.101:63178
summa = 0



zapchast00_1200_year_price = {}
zapchast1200_year_price = {}
n=1

with open("zapchast1200_year.json", encoding="utf-8") as file:
    srazy_parsim = json.load(file)

for item_href_categories, count_page in srazy_parsim.items():
    href_zapchast = []
    item_href_categories = str(item_href_categories)
    """markah = item_href_categories[item_href_categories.find("marka")+6:item_href_categories.find("/model_")]
    #print(markah)
    modelh = item_href_categories[item_href_categories.find("model")+6:item_href_categories.find("/god_")]
    print(markah, modelh)"""
    href_60_200 = item_href_categories[: item_href_categories.find("/store_Y")] + "/price-do_200/store_Y/?more=Y"
    href_200_500 = item_href_categories[: item_href_categories.find("/price-ot_60")] + "/price-ot_200/price-do_500/store_Y/?more=Y"
    href_500 = item_href_categories[: item_href_categories.find("/price-ot_60")] + "/price-ot_500/store_Y/?more=Y"
    href_zapchast.append(href_60_200)
    href_zapchast.append(href_200_500)
    href_zapchast.append(href_500)

    
    for url_zapchast in href_zapchast:
        print(url_zapchast)
    
        #print(url_zapchast)
        driver.get(url=url_zapchast)
        time.sleep(1)

        with open(f"{count_page}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{count_page}.html", encoding="utf-8") as file:
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
                print(num_page)
                summa = summa + num_page
                if num_page > 0 and num_page < 1201:
                    page = int(num_page / 20) + 1
                    zapchast00_1200_year_price[url_zapchast] = page
                else:
                    page = int(num_page / 20) + 1
                    zapchast1200_year_price[url_zapchast] = page

        os.remove(f"{count_page}.html") 

with open("zapchast00_1200_year_price.json", "a", encoding="utf-8") as file:
    json.dump(zapchast00_1200_year_price, file, indent=4, ensure_ascii=False)

with open("zapchast1200_year_price.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1200_year_price, file, indent=4, ensure_ascii=False)


print(summa)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие")