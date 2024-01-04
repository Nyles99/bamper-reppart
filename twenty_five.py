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
black_list = []
black_mark = []
black_model = []

file1 = open("black-list.txt", "r")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_list.append(line)
#print(black_list)
# закрываем файл
file1.close

file1 = open("black-mark.txt", "r", encoding="utf-8")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_mark.append(line)
#print(black_list)

# закрываем файл
file1.close

file1 = open("black-model.txt", "r", encoding="utf-8")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_model.append(line)
#print(black_list)

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


all_mark_models = soup.find_all("h3", class_="title-2")
#print(all_mark_models)
for item in all_mark_models:
    item = str(item)
    item_text = item[item.find("gray")+6 : item.find("/h3")-6]
    item_href_marka = "https://bamper.by"+item[item.find("href=")+6 : item.find("style") - 2]
    #print(item_href_marka, item_text)
    marka_need_list[item_text] = item_href_marka

model_need_list = {}
for item_text_marka, item_href_marka in marka_need_list.items():
    #print(item_text_marka)
    if item_text_marka not in black_mark:
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

with open("modelu.json", "a", encoding="utf-8") as file:
    json.dump(model_need_list, file, indent=4, ensure_ascii=False)        

with open('modelu.json', encoding="utf-8") as file:
    model_need_list = json.load(file)

zapchast00_400 = {}
zapchast400_500 = {}
zapchast500_600 = {}
zapchast600_760 = {}
zapchast760_900 = {}
zapchast2400_5000 = {}
zapchast5000_6000 = {}
zapchast6000_7000 = {}
zapchast7000_7700 = {}
zapchast7700_8500 = {}
zapchast8500_9000 = {}
zapchast9000_10100 = {}
zapchast10100_11000 = {}
zapchast11000_11800 = {}
zapchast11800_12500 = {}
zapchast12500_13000 = {}
zapchast13000_14000 = {}
zapchast14000 = {}
zapchast900_1050 = {}
zapchast1050_1200 = {}
zapchast1200_1600 = {}
zapchast1600_1700 = {}
zapchast1700_1900 = {}
zapchast1900_2000 = {}
zapchast2000_2200 = {}
zapchast2200_2400 = {}
n=1
for item_text_model, item_href_model in model_need_list.items():
    if item_text_model not in black_model:
        item_text_model = item_text_model.replace("/","_")
        item_href_model = str(item_href_model)
        item_href_model = item_href_model[item_href_model.find("catalog/")+8 : len(item_href_model) -1]
        print(item_href_model)
        markah = item_href_model[: item_href_model.find("-")]
        modelh = item_href_model[item_href_model.find("-") + 1 :]
        
        url_zapchast = f"https://bamper.by/zchbu/marka_{markah}/model_{modelh}/god_2012-2023/price-ot_70/store_Y/?more=Y"
        #print(url_zapchast)
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
                if num_page > 0 and num_page < 401:
                    page = int(num_page / 20) + 1
                    zapchast00_400[url_zapchast] = page
                elif num_page > 400 and num_page < 501:
                    page = int(num_page / 20) + 1
                    zapchast400_500[url_zapchast] = page
                elif num_page > 500 and num_page < 601:
                    page = int(num_page / 20) + 1
                    zapchast500_600[url_zapchast] = page
                elif num_page > 600 and num_page < 761:
                    page = int(num_page / 20) + 1
                    zapchast600_760[url_zapchast] = page
                elif num_page > 760 and num_page < 901:
                    page = int(num_page / 20) + 1
                    zapchast760_900[url_zapchast] = page
                elif num_page > 900 and num_page < 1051:
                    page = int(num_page / 20) + 1
                    zapchast900_1050[url_zapchast] = page
                elif num_page > 1050 and num_page < 1201:
                    page = int(num_page / 20) + 1
                    zapchast1050_1200[url_zapchast] = page
                elif num_page > 1200 and num_page < 1601:
                    page = int(num_page / 20) + 1
                    zapchast1200_1600[url_zapchast] = page
                elif num_page > 1600 and num_page < 1701:
                    page = int(num_page / 20) + 1
                    zapchast1600_1700[url_zapchast] = page
                elif num_page > 1700 and num_page < 1901:
                    page = int(num_page / 20) + 1
                    zapchast1700_1900[url_zapchast] = page
                elif num_page > 1900 and num_page < 2001:
                    page = int(num_page / 20) + 1
                    zapchast1900_2000[url_zapchast] = page
                elif num_page > 2000 and num_page < 2201:
                    page = int(num_page / 20) + 1
                    zapchast2000_2200[url_zapchast] = page
                elif num_page > 2200 and num_page < 2401:
                    page = int(num_page / 20) + 1
                    zapchast2200_2400[url_zapchast] = page      
                elif num_page > 2400 and num_page < 5001:
                    page = int(num_page / 20) + 1
                    zapchast2400_5000[markah] = modelh
                elif num_page > 5000 and num_page < 6001:
                    page = int(num_page / 20) + 1
                    zapchast5000_6000[markah] = modelh
                elif num_page > 6000 and num_page < 7001:
                    page = int(num_page / 20) + 1
                    zapchast6000_7000[markah] = modelh
                elif num_page > 7000 and num_page < 7701:
                    page = int(num_page / 20) + 1
                    zapchast7000_7700[markah] = modelh
                elif num_page > 7700 and num_page < 8501:
                    page = int(num_page / 20) + 1
                    zapchast7700_8500[markah] = modelh
                elif num_page > 8500 and num_page < 9001:
                    page = int(num_page / 20) + 1
                    zapchast8500_9000[markah] = modelh
                elif num_page > 9000 and num_page < 10101:
                    page = int(num_page / 20) + 1
                    zapchast9000_10100[markah] = modelh
                elif num_page > 10100 and num_page < 11001:
                    page = int(num_page / 20) + 1
                    zapchast10100_11000[markah] = modelh
                elif num_page > 11000 and num_page < 11801:
                    page = int(num_page / 20) + 1
                    zapchast11000_11800[markah] = modelh
                elif num_page > 11800 and num_page < 12501:
                    page = int(num_page / 20) + 1
                    zapchast11800_12500[markah] = modelh
                elif num_page > 12500 and num_page < 13001:
                    page = int(num_page / 20) + 1
                    zapchast12500_13000[markah] = modelh
                elif num_page > 13000 and num_page < 14001:
                    page = int(num_page / 20) + 1
                    zapchast13000_14000[markah] = modelh
                elif num_page > 14000:
                    page = int(num_page / 20) + 1
                    zapchast14000[markah] = modelh
        os.remove(f"{item_text_model}.html") 

with open("zapchast00_400.json", "a", encoding="utf-8") as file:
    json.dump(zapchast00_400, file, indent=4, ensure_ascii=False)

with open("zapchast400_500.json", "a", encoding="utf-8") as file:
    json.dump(zapchast400_500, file, indent=4, ensure_ascii=False)

with open("zapchast500_600.json", "a", encoding="utf-8") as file:
    json.dump(zapchast500_600, file, indent=4, ensure_ascii=False)

with open("zapchast600_760.json", "a", encoding="utf-8") as file:
    json.dump(zapchast600_760, file, indent=4, ensure_ascii=False)

with open("zapchast760_900.json", "a", encoding="utf-8") as file:
    json.dump(zapchast760_900, file, indent=4, ensure_ascii=False)

with open("zapchast900_1050.json", "a", encoding="utf-8") as file:
    json.dump(zapchast900_1050, file, indent=4, ensure_ascii=False)

with open("zapchast1050_1200.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1050_1200, file, indent=4, ensure_ascii=False)

with open("zapchast1200_1600.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1200_1600, file, indent=4, ensure_ascii=False)

with open("zapchast1600_1700.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1600_1700, file, indent=4, ensure_ascii=False)

with open("zapchast1700_1900.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1700_1900, file, indent=4, ensure_ascii=False)

with open("zapchast1900_2000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1900_2000, file, indent=4, ensure_ascii=False)

with open("zapchast2000_2200.json", "a", encoding="utf-8") as file:
    json.dump(zapchast2000_2200, file, indent=4, ensure_ascii=False)

with open("zapchast2200_2400.json", "a", encoding="utf-8") as file:
    json.dump(zapchast2200_2400, file, indent=4, ensure_ascii=False)

with open("zapchast2400_5000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast2400_5000, file, indent=4, ensure_ascii=False)

with open("zapchast5000_6000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast5000_6000, file, indent=4, ensure_ascii=False)

with open("zapchast6000_7000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast6000_7000, file, indent=4, ensure_ascii=False)

with open("zapchast7000_7700.json", "a", encoding="utf-8") as file:
    json.dump(zapchast7000_7700, file, indent=4, ensure_ascii=False)

with open("zapchast7700_8500.json", "a", encoding="utf-8") as file:
    json.dump(zapchast7700_8500, file, indent=4, ensure_ascii=False)

with open("zapchast8500_9000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast8500_9000, file, indent=4, ensure_ascii=False)

with open("zapchast9000_10100.json", "a", encoding="utf-8") as file:
    json.dump(zapchast9000_10100, file, indent=4, ensure_ascii=False)

with open("zapchast10100_11000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast10100_11000, file, indent=4, ensure_ascii=False)

with open("zapchast11000_11800.json", "a", encoding="utf-8") as file:
    json.dump(zapchast11000_11800, file, indent=4, ensure_ascii=False)

with open("zapchast11800_12500.json", "a", encoding="utf-8") as file:
    json.dump(zapchast11800_12500, file, indent=4, ensure_ascii=False)

with open("zapchast12500_13000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast12500_13000, file, indent=4, ensure_ascii=False)

with open("zapchast13000_14000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast13000_14000, file, indent=4, ensure_ascii=False)

with open("zapchast14000.json", "a", encoding="utf-8") as file:
    json.dump(zapchast14000, file, indent=4, ensure_ascii=False)

print(summa)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие")