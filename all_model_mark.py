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

options.add_argument("--proxy-server=146.185.223.77:11061")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})


url = "https://bamper.by/catalog/modeli/"

req = requests.get(url, headers=headers)
src = req.text
#print(src)
#with open("index.html", "w", encoding="utf-8") as file:
#    file.write(src)
#with open("index.html", encoding="utf-8") as file:
#    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
#print(soup)
marka_need_list = {}
model_need_list = {}

driver.get(url=url)
time.sleep(30)


with open(f"for_Artem.csv", "w", encoding="utf-8") as file_data:
    writer = csv.writer(file_data)

    writer.writerow(
        (
            "МАРКА",
            "МОДЕЛЬ",
            "ГОД",
            "КОЛИЧЕСТВО",
        )
    )



all_mark_models = soup.find_all("h3", class_="title-2")
#print(all_mark_models)
for item in all_mark_models:
    item = str(item)
    item_text = item[item.find("gray")+6 : item.find("/h3")-6]
    item_href_marka = "https://bamper.by"+item[item.find("href=")+6 : item.find("style") - 2]
    #print(item_href_marka, item_text)
    marka_need_list[item_text] = item_href_marka

model_need_list = {}
for marka, item_href_marka in marka_need_list.items():
    #print(item_text_marka)
    
    print(item_href_marka)
    req = requests.get(url=item_href_marka, headers=headers)
    src = req.text
    #print(src)

    soup = BeautifulSoup(src, 'html.parser')

    count = soup.find_all("a")
    for item in count:
        item = str(item)
        if "запчасти для <b>" in item:
            item_text = item[item.find("запчасти для <b>")+16 : item.find("</b> </a>")]
            #print(item_text)
            #if item_text not in black_model:
            item_href_model = "https://bamper.by"+item[item.find("href=")+6 : item.find(">запчасти") - 1]
            model_need_list[item_text] = item_href_model
            #print(item_href_model)
            #print(item_text, item_href_model)

            model = item_href_model[item_href_model.find("catalog/")+8 : -1]
            print(model)
            for year in range(2000, 2025):
                url_str = f"https://bamper.by/zchbu/marka_{marka}/model_{model}/god_{year}-{year}/"
                try:
                    driver.get(url=url_str)
                    time.sleep(1)

                    with open(f"{1}.html", "w", encoding="utf-8") as file:
                        file.write(driver.page_source)

                    with open(f"{1}.html", encoding="utf-8") as file:
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
                            file = open(f"for_Artem.csv", "a", encoding="utf-8", newline='')
                            writer = csv.writer(file)

                            writer.writerow(
                                (
                                    marka,
                                    model,
                                    year,
                                    num_page
                                )
                            )
                            file.close()
                except Exception:
                    print("не загрузилась")


#https://bamper.by/zchbu/marka_alfaromeo/model_33/god_2000-2000/




#with open("all_modelu_and_mark.json", "a", encoding="utf-8") as file:
#    json.dump(model_need_list, file, indent=4, ensure_ascii=False)        



a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие")